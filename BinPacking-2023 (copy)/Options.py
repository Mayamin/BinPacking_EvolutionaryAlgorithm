

class Options:

	def __init__(self):
		#here self.name means it is an instance varaible (has unique value for each object)
		#self.chromosomeLength = 90
		self.chromosomeLength = 88
		self.populationSize = 100
		# self.populationSize = 26
		self.maxGen =150
		# self.maxGen = 39
		self.pCross = 0.9
		self.pMut = 0.05
		self.infile = ""
		self.randomSeed = 2
		#what is this value for ? Ans: the size of combined population is double of the parent population -> 2 stands for double
		self.chcLambda = 2


