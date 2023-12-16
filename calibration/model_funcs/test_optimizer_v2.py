import random
import numpy as np
import shelve
import matplotlib.pyplot as plt
from calibration.deap import (
    algorithms,
    base,
    creator,
    tools
    )

import scipy.optimize as opt
import os
import pprint

from . import util_funcs
from . import Full_Model_stress

import pandas as pd


#Numpy presets
np.seterr(all='raise') #tell numpy to raise floating point errors. 

def data_input(fileName):
    #Read in data
    #Format = Temperature [C], Strain [mm/mm], Stress [MPa]
    data = np.loadtxt(fileName, dtype=float)
    
    #Convert temperature to Kelvin
    T = data[:,0] + 273.15
    
    #Grab strain
    eps = data[:,1]
    
    #Shift strain to be zeroed - THIS IS SKETCHY. NEED TO FIX LATER
    eps = eps# - eps.min()
    
    #Grab stress
    sigma = data[:,2]
    
    
    #Commented out right now.
    #Re-organize data to go from cold to hot
    min_T = T.min()
    I = np.argmin(T)
    
    T = np.concatenate((T[I:],T[0:I+1]))
    sigma = np.concatenate((sigma[I:],sigma[0:I+1]))*1e6
    eps = np.concatenate((eps[I:],eps[0:I+1]))
    
    #transform into pascals
    #sigma = np.ones(shape=sigma.shape[0])*7e6
    
    return eps,T,sigma

def material_data(x):
    # MATERIAL PARAMETERS (Structure: P)
    P = {}
    # Young's Modulus for Austenite and Martensite 
    P['E_M'] = x[0]
    P['E_A'] = x[0] - x[1]
    #P['E_A'] = 119E9
    #P['E_M'] = P['E_A']
    # Transformation temperatures (M:Martensite, A:Austenite), (s:start,f:final)
    P['M_s'] = x[2]
    P['M_f'] = x[2] - x[3]
    P['A_s'] = x[4]
    P['A_f'] = x[5] + x[4]
    
    # P['M_s'] = 273.15-30.0
    # P['M_f'] = 273.15-45.0
    # P['A_s'] = 273.15-10.0
    # P['A_f'] = 273.15+15.0
    
    # Slopes of transformation boundarings into austenite [C_A] and
    # martensite [C_M] at Calibration Stress 
    P['C_M'] = x[6]
    P['C_A'] = x[7]
    
    # Maximum and minimum transformation strain
    #Changing H_min to 0
    P['H_min'] = x[8]
    P['H_sat'] = x[8] + x[9]
    
    
    P['k'] = x[10]
    P['sig_crit'] = 0.
    
    # Coefficient of thermal expansion
    P['alpha'] = 0.
    
    # Smoothn hardening parameters 
    # NOTE: smoothness parameters must be 1 for explicit integration scheme
    P['n_1'] = x[11]
    P['n_2'] = x[12]
    P['n_3'] = x[13]
    P['n_4'] = x[14]
    
    # Algorithmic delta for modified smooth hardening function
    P['delta']=1e-5
    
    # Calibration Stress
    P['sig_cal']=200E6
    
    # Tolerance for change in MVF during implicit iteration
    P['MVF_tolerance']=1e-8
    
    return P

def cxTwoPointCopy(ind1, ind2):
    """Execute a two points crossover with copy on the input individuals. The
    copy is required because the slicing in numpy returns a view of the data,
    which leads to a self overwritting in the swap operation. It prevents:
    ::

        >>> import numpy
        >>> a = numpy.array((1,2,3,4))
        >>> b = numpy.array((5.6.7.8))
        >>> a[1:3], b[1:3] = b[1:3], a[1:3]
        >>> print(a)
        [1 6 7 4]
        >>> print(b)
        [5 6 7 8]
    """
    size = len(ind1)
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = (
        ind2[cxpoint1:cxpoint2],
        ind1[cxpoint1:cxpoint2],
    )
    return ind1, ind2

def psh(popSize, genSize, toolbox):
    """Generates DEAP things.

    Parameters
    ----------
    popSize : int
        Population size for GA
    genSize : int
        Number of generations for GA
    toolbox : deap
        DEAP toolbox.

    Returns
    -------
    pop : [type]
        Population
    stats : [type]
        Statistics
    hof : [type]
        Hall of Fame
    """
    # random.seed(64)
    pop = toolbox.population(n=popSize)
    # Numpy equality function (operators.eq) between two arrays returns the
    # equality element wise, which raises an exception in the if similar()
    # check of the hall of fame. Using a different equality function like
    # numpy.array_equal or numpy.allclose solve this issue.
    hof = tools.HallOfFame(1, similar=np.array_equal)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    algorithms.eaSimple(
        pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=genSize, stats=stats, halloffame=hof
    )
    print(hof)
    return pop, stats, hof
    
def exponentialBounds(value, bounds=[1e3, 1e8]):
    """[summary]

    Parameters
    ----------
    value : [type]
        [description]
    bounds : list, optional
        [description], by default [1e3, 1e8]

    Returns
    -------
    [type]
        [description]
    """
    a = bounds[0]  # lower bound
    b = bounds[1] / a  # upper bound
    boundedValue = a * b ** (value / 1.0)  # tau (time constant) is one
    return boundedValue

    

def resizeBounds(value, bounds=[1e3, 1e8]):
    """Maps an entry of the design vector (bounds [0,1]) to the isotropic
    hardening modulus.

    Parameters
    ----------
    value : flt
        Entry in the design vector
    bounds : list, optional
        [description], by default [1e3, 1e8]

    Returns
    -------
    value : flt
        Isotropic hardening modulus
    """
    value = (bounds[1] - bounds[0]) * value + bounds[0]
    return value

# def applyBounds(x):
#     """Transforms the individual (in [0,1]) to a bounded individual depending
#     on the optimization-specific bounds.

#     Parameters
#     ----------
#     individual : array
#         Design vector for calibration. All entries are bounded between 0 and 1.
#     bounds : list
#         Bounds for the design vector, depending on the type of hardening.
#     substructureParameters : dict
#         Dictionary containing all important parameters (i.e., fixed values) pertaining to the substructure.
#     hardeningFlag : int
#         Flag to determine what type of hardening.

#     Returns
#     -------
#     boundedIndividual : array
#         Design vector for calibration, actually bounded for analysis.
#     """
#     bounds = []
#     bounds.append([60E9,100E9]) #E^M
#     bounds.append([-10E9,10E9]) #E^A
#     bounds.append([273.15-60,273.15-20]) #M_s
#     bounds.append([0,30]) #M_s-M_f
#     bounds.append([273.15-30,273.15]) #A_s
#     bounds.append([0,30]) #A_f - A_s
#     bounds.append([4E6,12E6]) #C^M
#     bounds.append([4E6,12E6]) #C^A
#     bounds.append([0.0,0.05]) #H_min
#     bounds.append([0.01,0.1]) #H_sat-H_min
#     bounds.append([0.001E-6,0.1E-6]) #k
#     bounds.append([0.2,1.0]) #n_1
#     bounds.append([0.2,1.0]) #n_2
#     bounds.append([0.2,1.0]) #n_3
#     bounds.append([0.2,1.0]) #n_4
    
    
#     boundedX = np.zeros(shape=len(x))
#     for i in range(len(x)):
#         boundedX[i] = resizeBounds(x[i], bounds=list(bounds[i]))
#     return boundedX


def evaluate(
        x,
        data,
        calWin,
        GA_data = False,
        plot_flag = False,
        gradient_flag=False,
        final_flag=False
        ):
    # INPUT: stress/strain/temperature, material properties (P)
    
    bounds = data['bounds']
    boundedX = np.zeros(shape=len(x))
    prop_count = 0 
    for j in range(len(x)):
        boundedX[j] = resizeBounds(x[j], bounds=list(bounds[j]))


    P = data['P']

    DV_order = ['E_M','E_A', 'M_s', 'M_f', 'A_s', 'A_f', 'C_M', 'C_A', 'H_min',
            'H_max - H_min', 'k', 'n_1', 'n_2', 'n_3', 'n_4', 'sig_crit', 'alpha']

    prop_count = 0
    DV_count = 0
    for DV in DV_order:
        if data['DV_flags'][prop_count] == True:
            #if DV == 'E_A':
            #    P['E_A'] = P['E_M'] - boundedX[DV_count]
            if DV == 'M_f':
                P['M_f'] = P['M_s'] - boundedX[DV_count]
            elif DV == 'A_f':
                P['A_f'] = P['A_s'] + boundedX[DV_count]
            elif DV == 'H_max - H_min':
                P['H_sat'] = P['H_min'] + boundedX[DV_count]
            else:
                P[DV] = boundedX[DV_count]
            DV_count +=1
        else:
            pass
        prop_count +=1
        
    if data['modulus_flag'] == True: #Set E_A = E_M
        P['E_A'] = P['E_M']
        
    if data['slope_flag'] == True: #Set C_A = C_M
        P['C_A'] = P['C_M']
        
    if data['smooth_hardening_flag'] == True: #Set n_1 = n_2 = n_3 = n_4
        P['n_2'] = P['n_1']
        P['n_3'] = P['n_1']
        P['n_4'] = P['n_1'] 
        
    #P['sig_crit'] = 0.
    
    # Coefficient of thermal expansion
    #P['alpha'] = 0.   
    
    # Algorithmic delta for modified smooth hardening function
    P['delta']=data['delta']
    
    # Calibration Stress
    P['sig_cal']=data['sigma_cal']
    
    # Tolerance for change in MVF during implicit iteration
    P['MVF_tolerance']=data['MVF_tol']
    
    
    i = 0 
    eps_model_total = []
    T_total = []
    num_experiments = data['num_experiments']
    errors = np.zeros(shape=num_experiments)
    for i in range(num_experiments):
        eps = data['exp_'+str(i)]['strain']
        T = data['exp_'+str(i)]['temperature']
        sigma = data['exp_'+str(i)]['stress']     
        

        
        #Solver options
        elastic_check = 'N'
        integration_scheme = 'I'
        
        error_flag = 'two_norm'
        try:
            eps_model, MVF, eps_t, E, MVF_r, eps_t_r = Full_Model_stress.Full_Model_stress(T, sigma, P, elastic_check, integration_scheme)
            eps_model_total.append(eps_model)
            T_total.append(T)
            if error_flag == 'two_norm':
                errors[i] = util_funcs.minkowski_error(eps,eps_model,order=2)
            elif error_flag == 'infinity_norm':
                errors[i] = util_funcs.minkowski_error(eps,eps_model,order=10)
            elif error_flag == 'hausdorff':
                errors[i] = util_funcs.symmetric_hausdorff(eps.to_numpy()[..., np.newaxis],eps_model[..., np.newaxis])
        except:
            errors[i] = 1E12
        i +=1
        
    
        
    if plot_flag == True:
        # plot_strain_temperature(T_total,eps_model_total,i,d)
        calWin.updateTempStrain(T_total, eps_model_total, i)
        calWin.updatePhaseDiagram(P, [0, 200E6])
        calWin.updateDVVals(x,data['DV_flags'])
        
    if gradient_flag == True:
        gens = GA_data[0]
        mins = GA_data[1]
        gens.append(max(gens)+1)
        if np.mean(errors) < mins[-1]:
            mins.append(np.mean(errors))
        else:
            mins.append(mins[-1])
        calWin.updateOptProgress(gens, mins,mins, 0.0)
        
    if final_flag == True:
        # pprint(x)
        pprint.pprint(P)

    if error_flag in ['two_norm','infinity_norm']:
        return np.mean(errors),
    elif error_flag == 'hausdorff':
        return np.max(errors),



def optimizer(toolbox,popSize,genSize,data, calWin, seed=None):
    random.seed(seed)
    failFlag = False

    CXPB = 0.9
    nGenSave = 20 #Best population will be saved every nGenSave
    i = 0 
    d = util_funcs.DynamicUpdate()

    num_experiments = data['num_experiments']
    for i in range(num_experiments):
        eps,T = data['exp_'+str(i)]['strain'],data['exp_'+str(i)]['temperature']
        #T = 

        
        if i == 0:
            total_strain = eps
            total_temperature = T
        else:
            total_strain = np.concatenate((total_strain,eps))
            total_temperature = np.concatenate((total_temperature,T))
        
        i +=1

    # d.on_launch(total_temperature,total_strain,i)
    calWin.plotExperimental(total_temperature, total_strain, i)



    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"

    pop = toolbox.population(n=popSize)

    # Evaluate the individuals with an invalid fitness (ind. that need to be updated)
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    #HERE WE CAN ELIMINATE SERIAL MAPPING AND REPLACE WITH BATCH CALCULATION
    #WE IGNORE THE 'EVALUATE' DEVICE COMPLETELY, SINCE IT IS FOR A SINGLE DESIGN
    # fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    arrayofGenes = []
    gen=0
    for ind in invalid_ind:
        arrayofGenes.append(ind)
        ind.fitness.values = evaluate(ind,data, calWin)
        
    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))

    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    # db=shelve.open('popLog.dat') Open in simManager
    pixList = []
    pixString = ''
    totGen = 1
    gen = 1
    cntGenSave = 1
    
    while gen < genSize+1:
        # Vary the population
        offspring = toolbox.select(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]
        
        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
            
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
            
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        
        arrayofGenes = []
        for ind in invalid_ind:
            arrayofGenes.append(ind)
            ind.fitness.values = evaluate(ind,data, calWin)
        
        # Select the next generation population
        pop = toolbox.select(pop + offspring, popSize)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)
        #pop.sort(key=lambda x: x.fitness.values)
        db=shelve.open('popLog')
        db['lastPop']=pop
        if cntGenSave == nGenSave:
            db[repr(gen)+'Pop']=pop    
            cntGenSave = 0
        db.close()

        
        # Write a color map illustrating the genes of all the best population members
        # throughout the generations
        generations = logbook.select('gen')
        min_func_val = logbook.select('min')
        
        avg = logbook.select('avg')
        std = logbook.select('std')
        calWin.updateOptProgress(generations, min_func_val, avg, std)
        #print(pop[0])
        calWin.updateDVVals(pop[0],data['DV_flags'])


        #pop[0] is the best current individual
        error = evaluate(pop[0],data,calWin,GA_data=False,
                         plot_flag=True,
                         gradient_flag = False,final_flag=False)
        cntGenSave +=1
        gen += 1
        totGen += 1
        
    return pop, logbook,d
        
    

#if __name__ == '__main__':
def main(bounds,calibration_class,data,calWin):
    util_funcs.plot_settings(format_flag="presentation")

    modulus_flag = calibration_class.flags['modulus_flag'] #flag to set both moduli (E_M and E_A) equal to each other
    slope_flag = calibration_class.flags['slope_flag'] #flag to set both stress-influence coefficients (C_M and C_A) equal to each other
    smooth_hardening_flag = calibration_class.flags['smooth_hardening_flag'] #flag to set all smooth hardening coefficients (n_1 -- n_4) equal
    DV_flags = calibration_class.DV_flags 
    known_values = calibration_class.known_values
    
    
    
    if modulus_flag == True:
        DV_flags[1] = False #If we want both moduli to be the same, just make the E_M - E_A DV inactive
        
    # Add in similar code for slope and hardening flags
        
    data['modulus_flag'] = modulus_flag
    data['slope_flag'] = slope_flag
    data['smooth_hardening_flag'] = smooth_hardening_flag
    
    data['delta'] = calibration_class.delta
    data['sigma_cal'] = calibration_class.sigma_cal
    data['MVF_tol'] = calibration_class.MVF_tol
    
    data['DV_flags'] = DV_flags 
    
    num_DVs = DV_flags.sum()
    
    ## Initialize bounds based on the DV_flags

    
    data['bounds'] = bounds 
    data['P'] = known_values

    popSize = int(calibration_class.pop_size)  # Population size for GA (must be divisible by 4)
    genSize = int(calibration_class.num_gens) # Number of generations for GA
    maxIterGradient = int(calibration_class.num_iters)  # Maximum iterations for the gradient-based optimizer
    # DEAP
    creator.create(
        "FitnessMin", base.Fitness, weights=(-1.0,)
    )  # Create a single-objective minimization
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.random)
    toolbox.register(
        "individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=num_DVs
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register(
        "evaluate",
        evaluate,
        data = data
    )
    toolbox.register("mate", cxTwoPointCopy)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    # startTime = time.perf_counter()
    pop, stats,d  = optimizer(toolbox,popSize,genSize,data, calWin)
    
    print('\n')
    print('Entering gradient-based optimizer')
    print('\n')
    generations = stats.select('gen')
    min_func_val = stats.select('min')
    GA_data = [generations,min_func_val]
    bounds = opt.Bounds(0,1)
    res2 = opt.minimize(
        evaluate,
        pop[0],
        method="SLSQP",
        options={"maxiter": maxIterGradient,
                  "disp":True},
        bounds = bounds,
        args=(
            data, calWin,GA_data,True,True
        ),
        #callback=calWin.updateDVVals,
    )
    
    error = evaluate(res2.x,data, calWin, 
                     GA_data = False,
                     plot_flag=True,
                     gradient_flag=False,
                     final_flag=True)
    
    return error
    

    
    
    
    
    
    