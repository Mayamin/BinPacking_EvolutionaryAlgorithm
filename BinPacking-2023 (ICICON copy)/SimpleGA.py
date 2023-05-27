
import random
import Options #where all initializations are done
from Population import Population
import time
from datetime import timedelta
class GA:
	#the following will be called evertime GA object is made
	def __init__(self):
		#options class has an __init__ method with no parameter except self
		self.options = Options.Options()
		random.seed(self.options.randomSeed)
    
	#function to initialize parent and child population and report statistics
	def Init(self):
		#population class has an __init__ function that takes options as parameter, creating population type object named parent
		self.parent = Population(self.options)
  
		#population class has functions evaluate, statistics and report
		self.parent.evaluate()
		self.parent.statistics()
		self.parent.report(0)
  
		#creating population type object named child
		self.child = Population(self.options)
		return

    #function to run GA for max Gen
	def Run(self):
		for	i in range(1, self.options.maxGen):
			# population class has all these functions -> generation, statistics, report
#			self.parent.generation(self.child)
#			self.child.evaluate()
			self.parent.CHCGeneration(self.child)
			self.child.statistics()
			self.child.report(i)
            
			#parent child swapping
			tmp = self.parent
			self.parent = self.child
			self.child = tmp

		#self.parent.printPop(0, self.options.populationSize)
		return


if __name__ == "__main__":
        # record start time
		start = time.time()
for i in range(0,30):
		Options.randomSeed = i
		# Options.randomSeed = 2
		ga = GA()
		ga.Init()
		ga.Run()

		end = time.time()
		# print the difference between start
# and end time in milli. secs
# print("The time of execution of above program is :",timedelta((end-start) * 10**3), "hr:min:sec")
     
        # Options.randomSeed(i)
		# #creating GA object
		# ga = GA()
		# #initializing GA by calling Init function
		# ga.Init()
		# #running GA
		# ga.Run()
		# # filename = "CHC_data.csv"
		# #  heading = ["gen", "min", "avg", "max"]
		# # with open(filename,'w') as csvfile:
		# #     #csv writer object
		# # 	csv_object = writer(csvfile)
		# # 	#writing
		# # 	csv_object.writerow(heading)

