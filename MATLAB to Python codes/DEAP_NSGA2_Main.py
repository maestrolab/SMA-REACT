#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import array
import random
import os
import sys
import shelve
import numpy
from math import sqrt
# import pixelGenes
# reload(pixelGenes)

from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence
from deap import creator
from deap import tools

#Prepare the log file
try:
    os.remove('popLog.dat') 
except:
    print('No previous log file')
db=shelve.open('popLog')
db['runNum']=0.0
print(db.keys())
db.close()

#This is the objective function. It takes argument 'ind' and returns 'f1', 'f2'
#It is called in 'toolbox.register("evaluate", abqObjfun)' below
import simManagerPar_Truss
reload(simManagerPar_Truss)

#Following says 'minimize two objectives'...2 negative 1's
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
#This defines what an individual is; ours is rep. by a list of floats (inherited from numpy)
creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Problem definition
# L-system function (its genes) are defined on inputs bounded [-1...1]
BOUND_LOW, BOUND_UP = 0.0, 1.0

# Functions zdt4 has bounds x1 = [0, 1], xn = [-5, 5], with n = 2, ..., 10
# BOUND_LOW, BOUND_UP = [0.0] + [-5.0]*9, [1.0] + [5.0]*9

# Number of gene entries is:
#  2(axiom) +
#  12*4 (4 rules for 4 letters, 12 entry/rule) +
#  2 (angle, distance...when used)
NDIM = 2 + 18*4 + 6

def uniform(low, up, size=None):
    try:
        return [random.uniform(a, b) for a, b in zip(low, up)]
    except TypeError:
        return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]

#This is an 'attribute generator,' here generates NDIM random numbers between a and b
toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM)
print("Test print attr: ",toolbox.attr_float())

#These are 'structures initializers', initializing an individual and a population
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#toolbox.register("evaluate", simManager_CM.simManager)
toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0)
toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/52.)
toolbox.register("select", tools.selNSGA2)

def main(seed=None):
	random.seed(seed)
	failFlag = False

	NGEN = 10
	MU = 20 #Must be a multiple of 4 (?)
	CXPB = 0.9
	nGenSave = 20 #Best population will be saved every nGenSave

	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", numpy.mean)
	stats.register("std", numpy.std)
	stats.register("min", numpy.min)
	stats.register("max", numpy.max)

	logbook = tools.Logbook()
	logbook.header = "gen", "evals", "std", "min", "avg", "max"

	pop = toolbox.population(n=MU)

	# Evaluate the individuals with an invalid fitness (ind. that need to be updated)
	invalid_ind = [ind for ind in pop if not ind.fitness.valid]
	#HERE WE CAN ELIMINATE SERIAL MAPPING AND REPLACE WITH BATCH CALCULATION
	#WE IGNORE THE 'EVALUATE' DEVICE COMPLETELY, SINCE IT IS FOR A SINGLE DESIGN
	# fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
	arrayofGenes = []
	gen=0
	for ind in invalid_ind:
		arrayofGenes.append(ind)
	fitnesses,failFlag=simManagerPar_Truss.simManager(arrayofGenes,gen)
	if(failFlag):
		print "First population failed to run; not good. Killing process."
		sys.exit("First population failed to run; not good")
	#END BATCH
	for ind, fit in zip(invalid_ind, fitnesses):
		ind.fitness.values = fit

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
	while gen < NGEN+1:

		print ' '
		print '============================'
		print 'Starting generation ',gen
		print 'Total generations tried: ',totGen
		print '============================'
		print ' '		
		# Vary the population
		offspring = tools.selTournamentDCD(pop, len(pop))
		offspring = [toolbox.clone(ind) for ind in offspring]
		
		for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
			if random.random() <= CXPB:
				toolbox.mate(ind1, ind2)
			
			toolbox.mutate(ind1)
			toolbox.mutate(ind2)
			del ind1.fitness.values, ind2.fitness.values
		
		# Evaluate the individuals with an invalid fitness
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

		# HERE WE CAN ELIMINATE SERIAL MAPPING AND REPLACE WITH BATCH CALCULATION
		# WE IGNORE THE 'EVALUATE' DEVICE COMPLETELY, SINCE IT IS FOR A SINGLE DESIGN
		# fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
		arrayofGenes = []
		for ind in invalid_ind:
			arrayofGenes.append(ind)
		fitnesses,failFlag=simManagerPar_Truss.simManager(arrayofGenes,gen)
		# Failed runs are assigned bad values and the generation is repeated,
		# with new mutation(s) hopefully eliminating problems.
		if (failFlag):
			gen -= 1
			cntGenSave -= 1
		else:
			pixListPop = []
			for ind in pop:
				pixList,pixListPop,pixString,nActGenes = pixelGenes.pixelProc(ind,pixList,pixListPop,pixString) # Adds pixels for the current ind to the existing list
			pixList,pixString = pixelGenes.whiteLine(pixList,pixString,nActGenes)
			pixelGenes.fileMaker(pixList,pixListPop,pixString,nActGenes,gen,MU)
		#END BATCH
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit

		# Select the next generation population
		pop = toolbox.select(pop + offspring, MU)
		record = stats.compile(pop)
		logbook.record(gen=gen, evals=len(invalid_ind), **record)
		print(logbook.stream)
		print 'o'
		#pop.sort(key=lambda x: x.fitness.values)
		db=shelve.open('popLog')
		db['lastPop']=pop
		if cntGenSave == nGenSave:
			db[repr(gen)+'Pop']=pop	
			cntGenSave = 0
		db.close()
		print 'k'
		
		# Write a color map illustrating the genes of all the best population members
		# throughout the generations


		cntGenSave +=1
		gen += 1
		totGen += 1
		

	return pop, logbook
        
if __name__ == "__main__":
    
    pop, stats = main()
    pop.sort(key=lambda x: x.fitness.values)
    
    print(stats)
    
import numpy
front = numpy.array([ind.fitness.values for ind in pop])
print front

#Save the final front to the log file
db=shelve.open('popLog')
db['finalFront']=front
db['finalPop']=pop
db.close()
#NEED TO INSTALL MATPLOTLIB!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
# import matplotlib.pyplot as plt



# #optimal_front = numpy.array(optimal_front)
# #plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
# plt.scatter(front[:,0], front[:,1], c="b")
# plt.axis("tight")
# plt.show()
