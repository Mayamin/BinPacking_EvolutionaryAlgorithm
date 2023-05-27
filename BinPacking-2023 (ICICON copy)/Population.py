
import Individual#initialize chromosome, mutate and an unknown function
import Evaluator #objective/fitness function and decode function

import random
import Utils #flip and random number generators within a range
import csv
from csv import writer

filename = "CHC_data.csv"
heading =[0, 0, 0, 0]
with open(filename,'w') as csvfile:
#csv writer object
	csvwriter = csv.writer(csvfile)
	#writing
	csvwriter.writerow(heading)
 
# # flag = 0

class Population(object):
    #defining what population object will have, population object will be made with options provided as parameter from GA class
	def	__init__(self, options):
		self.options = options;
		self.individuals = []
		self.min = -1
		self.max = -1
		self.avg = -1
		# initialize population with randomly generated Individuals
		

  		#creating an array of parent_pop*2 size and filling up all chromosomes with 0 0r 1
		for i in range(options.populationSize * options.chcLambda):
			#Individual class doesnot have a constructor of function where it takes only 1 parameter
			self.individuals.append(Individual.Individual(options))
			#now we have a double population size container with all chromosomes having some value
		#now we assign a fitness value to half of the container individuals.i.e. upto population size of container not population size*2
		self.evaluate()

	
	def evaluate(self):
		#pop_size is 2
		for i in range(self.options.populationSize): #ind in self.individuals:
			self.individuals[i].fitness = Evaluator.EvaluateX2(self.individuals[i])
			
	def printPop(self, start, end):
		i = 0
		for i in range(start, end, 1): #self.options.populationSize): #ind in self.individuals:
			# print(i, end=": ")
			ind = self.individuals[i]
			# print (ind.chromosome, " Fit: ", ind.fitness)#every individual has a chromosome
			i = i+1
		self.report("")
    
	def report(self, gen):
		info = [gen, self.min, self.avg, self.max]
     
		try:
			with open (filename,'a') as csvfile:
				csvwriter = writer(csvfile)
				csvwriter.writerow(info)
				csvwriter.close()
		except AttributeError:
				pass
		# print ("Generation number is ", gen, "min fitness is ", self.min, "Average fitness is ", self.avg, "Maximum fitness is ", self.max)
		
		
  
	def statistics(self):
		#calculates fitness min max and average per generation
		self.sumFitness = 0
		self.min = self.individuals[0].fitness
		self.max = self.individuals[0].fitness
		self.avg = 0
		for i in range(self.options.populationSize): #ind in self.individuals:
			ind = self.individuals[i]
			self.sumFitness += ind.fitness
			if ind.fitness < self.min:
				self.min = ind.fitness
			if ind.fitness > self.max:
				self.max = ind.fitness

		self.avg = self.sumFitness/self.options.populationSize #len(self.individuals)

	def select(self):
		randFraction = self.sumFitness * random.random()
		sum = 0
		i = 0
		for i in range(self.options.populationSize): #ind in self.individuals:
			ind = self.individuals[i]
			sum += ind.fitness
			if randFraction <= sum:
				return (i, ind)
		print("Selection failed")
		return (self.options.populationSize - 1, self.individuals[self.options.populationsSize - 1]) #return index and value
    
	#it will not be used in CHC
	def generation(self, child):
		for i in range(0, len(self.individuals), 2): #range(start,stop, increment) increment is 2 since 2 parents are selcted and 2 child space created simultaneously 
			#selecting 2 parent chromosome from parent population for slicing and mutation to produce 2 new child chromosome with different bit values & combinations
			x, p1 = self.select()
			x, p2 = self.select()
			#creating population slot for 2 children, 2 empty chromosomes in a child container
			c1 = child.individuals[i]
			c2 = child.individuals[i + 1]
            
            #crossover parents and store new result or combination in child chromosome
			self.xover1Pt(p1, p2, c1, c2)	

			#flip the bits of child chromosome for new combination or more diversity or exploration		
			c1.mutate(self.options)
			c2.mutate(self.options)
    
	#this is the only generation function for CHC selection
	def CHCGeneration(self, child):
		for i in range(0, self.options.populationSize, 2):
			#selecting 2 parent chromosome from parent population for slicing and mutation to produce 2 new child chromosome with different bit values & combinations
			x, p1 = self.select()
			x, p2 = self.select()
            
			#no new container for child rather allocating new space for 2 child below existing parent population
			c1 = self.individuals[self.options.populationSize + i]
			c2 = self.individuals[self.options.populationSize + i + 1]
            
			#crossover parents and store new result or combination in child chromosome
			self.xover1Pt(p1, p2, c1, c2)
			
			#flip the bits of child chromosome for new combination or more diversity or exploration, accesing mutate from individual class
			c1.mutate(self.options);
			c2.mutate(self.options);
		self.halve(child)

	def comparator(self, individual):
		return individual.fitness

	def halve(self, child):

		#assigning fitness vlaues to all child
		for	i in range(self.options.populationSize,	self.options.populationSize	* self.options.chcLambda):
			self.individuals[i].fitness = Evaluator.EvaluateX2(self.individuals[i])
		
		#sorting the best fitindividuals out of all parents and children
		self.individuals.sort (key = self.comparator, reverse = True) #reverse since descending order 4 3 2 1

		#self.printPop(0, self.options.populationSize * self.options.chcLambda)
		for i in range(self.options.populationSize):
			#copy the 1st half of best fitness sorted individuals to child space
			child.individuals[i].myCopy(self.individuals[i])
			#			child.individuals[i] = self.individuals[i]

	def xover1Pt(self, p1, p2, c1, c2):
		for i in range(self.options.chromosomeLength):
			c1.chromosome[i] = p1.chromosome[i]
			c2.chromosome[i] = p2.chromosome[i]
		if Utils.flip(self.options.pCross):
			xp = Utils.randInt(1, self.options.chromosomeLength)
			for i in range(xp, self.options.chromosomeLength):
				c1.chromosome[i] = p2.chromosome[i]
				c2.chromosome[i] = p1.chromosome[i]
