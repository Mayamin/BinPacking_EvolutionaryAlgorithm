import random
import Utils

class Individual:

	def __init__(self, options):
		self.chromosome = []
		self.chromosomeLength = options.chromosomeLength
		self.fitness = -1
		self.objective = -1 #what is this for?!
		
        #initializing chromosome
		for i in range(options.chromosomeLength):
			self.chromosome.append(random.choice((0, 1)))

	def mutate(self, options):
		for i in range(options.chromosomeLength):
			if Utils.flip(options.pMut):
				self.chromosome[i] = 1 - self.chromosome[i]

	def myCopy(self, ind):
		self.fitness = ind.fitness
		self.chromosomeLength = ind.chromosomeLength # this should not change!
		self.objective = ind.objective
  
		for i in range(self.chromosomeLength):
			self.chromosome[i] = ind.chromosome[i]
