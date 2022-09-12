import random
import numpy as np
import matplotlib.pyplot as plt
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import scipy.optimize as opt


from Full_Model_stress import Full_Model_stress
from util_funcs import minkowski_error, plot_settings


#Numpy presets
np.seterr(all='raise') #tell numpy to raise floating point errors. 

def plot_strain_temperature(T,eps,eps_model):
    plt.plot(T,eps,T,eps_model)
    
    return

def data_input():
    #Read in data
    #Format = Temperature [C], Strain [mm/mm], Stress [MPa]
    data = np.loadtxt("7 MPa Scootch.txt", dtype=float)
    
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
    P['n1'] = x[11]
    P['n2'] = x[12]
    P['n3'] = x[13]
    P['n4'] = x[14]
    
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

def applyBounds(x):
    """Transforms the individual (in [0,1]) to a bounded individual depending
    on the optimization-specific bounds.

    Parameters
    ----------
    individual : array
        Design vector for calibration. All entries are bounded between 0 and 1.
    bounds : list
        Bounds for the design vector, depending on the type of hardening.
    substructureParameters : dict
        Dictionary containing all important parameters (i.e., fixed values) pertaining to the substructure.
    hardeningFlag : int
        Flag to determine what type of hardening.

    Returns
    -------
    boundedIndividual : array
        Design vector for calibration, actually bounded for analysis.
    """
    bounds = []
    bounds.append([60E9,100E9]) #E^M
    bounds.append([-10E9,10E9]) #E^A
    bounds.append([273.15-60,273.15-20]) #M_s
    bounds.append([0,30]) #M_s-M_f
    bounds.append([273.15-30,273.15]) #A_s
    bounds.append([0,30]) #A_f - A_s
    bounds.append([4E6,12E6]) #C^M
    bounds.append([4E6,12E6]) #C^A
    bounds.append([0.0,0.05]) #H_min
    bounds.append([0.01,0.1]) #H_sat-H_min
    bounds.append([0.001E-6,0.1E-6]) #k
    bounds.append([0.2,1.0]) #n_1
    bounds.append([0.2,1.0]) #n_2
    bounds.append([0.2,1.0]) #n_3
    bounds.append([0.2,1.0]) #n_4
    
    boundedX = np.zeros(shape=len(x))
    for i in range(len(x)):
        boundedX[i] = resizeBounds(x[i], bounds=list(bounds[i]))
    return boundedX


def evaluate(x,plot_flag = False):
    # INPUT: stress/strain/temperature, material properties (P)
    eps,T,sigma = data_input()
    

    boundedX = applyBounds(x)    
    
    P = material_data(boundedX)
    #Solver options
    elastic_check = 'N'
    integration_scheme = 'I'
    
    
    try:
        eps_model, MVF, eps_t, E, MVF_r, eps_t_r = Full_Model_stress(T, sigma, P, elastic_check, integration_scheme)
        
        
        if plot_flag == True:
            plot_strain_temperature(T,eps,eps_model)
    
        error = minkowski_error(eps,eps_model,order=2)
    except:
        error = 1E5
    
    return error,


if __name__ == '__main__':
    plot_settings(format_flag="presentation")
    #Dummy design vector right now
    x = [93.7E9,93.7E9-119E9,273.15-45.0,20,273.15-20.0,25,
         6.65E6,13.9E6,0.0045,0.0386-0.0045,0.001E-5,1.0,1.0,1.0,1.0]
    
    x = np.ones(shape=len(x))*0.0
    
    popSize = 100  # Population size for GA
    genSize = 50 # Number of generations for GA
    maxIterGradient = 1000  # Maximum iterations for the gradient-based optimizer
    
    # DEAP
    creator.create(
        "FitnessMin", base.Fitness, weights=(-1.0,)
    )  # Create a single-objective minimization
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.random)
    toolbox.register(
        "individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=len(x)
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register(
        "evaluate",
        evaluate,
    )
    toolbox.register("mate", cxTwoPointCopy)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    # startTime = time.perf_counter()
    pop, stats, hof = psh(popSize, genSize, toolbox)
    
    res2 = opt.minimize(
        evaluate,
        pop[0],
        method="SLSQP",
        options={"maxiter": maxIterGradient,
                 "disp":True},
    )
    
    error = evaluate(res2.x,plot_flag=True)
    
    boundedX = applyBounds(res2.x)    
    
    P = material_data(boundedX)
    
    
    
    
    
    