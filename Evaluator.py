
import Individual
import math
import numpy as np
import colorUnion
import csv
from csv import writer
from colorUnion import *

# binary_height = []
# binary_theta= []

# decimal_height = []
# decimal_theta = []

theta_max_range = 120
theta_min_range = 1
theta_bits = 7

filename_2 = "height_theta_2.csv"
heading_2 =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
with open(filename_2,'w') as csvfile:
#csv writer object
	csvwriter_2 = csv.writer(csvfile)
	#writing
	csvwriter_2.writerow(heading_2)



def precision_theta(theta_max_range,theta_min_range,theta_bits):
    # sum = 0
    # for i in range(individual.chromosomeLength):
    precision_value = (theta_max_range - theta_min_range)/((pow(2,theta_bits)*1.00) )                                                                                
    # print("precision value ", precision_value)
    return precision_value


def decode(binary_array):
    deci = 0
    length = len(binary_array)
#     print("Height block length",length)
    
    #checking if it is height array, precison 1 by default
    if length == 8:
        for i in range(length):
            deci = deci+ binary_array[i]*pow(2,7-i)
        
        height = deci 
        
        
     
        return height
    #checking if it is theta array, precison calculation needed
    elif length == 7:
        for i in range(length):
            # print("bin T array", binary_array)
            precision = precision_theta(theta_max_range,theta_min_range,theta_bits)
            val = binary_array[i]*pow(2,6-i)
            deci = deci+(val * precision)
            # print("theta decimal value",deci)
        
        theta = deci
        # decimal_theta = deci
        
        return  theta
    
def  EvaluateX2(individual):
    binary_height = []
    binary_theta= []
    decimal_height = []
    decimal_theta = []
 

    
    # print("whole chromosome vlaues", individual.chromosome)
    for i in range(0, len(individual.chromosome)-42, 8):
        for j in range (i,i+8):
            binary_height.append(individual.chromosome[j])
#             print(chromosome[j])
    
    # taking the 1st 6 theta values in binary 6*7 = 42,
    # theta_array = [theta1,theta2....theta6]
    
#     print("2nd 42 chromosome vlaues")
    for i in range(48,len(individual.chromosome),7):
        for j in range (i,i+7):
            binary_theta.append(individual.chromosome[j])
#             print(chromosome[j])
    
    #decimal H theta separate
    # converting height bin to deci 
#     print("bin h",binary_height) 
#     print("bin theta",binary_theta) 
   
#     print("len bin H , len bin T", len(binary_height), len(binary_theta))
    
    for i in range(0,len(binary_height), 8):
        
        #temporary hold of each binary height values (8 bits)
        height_block = []
        for j in range (i, i+8):
            height_block.append(binary_height[j])

        decimal_height.append( decode(height_block) )
        
    
    for i in range(0,len(binary_theta), 7):
        
        #temporary hold of each binary height values (8 bits)
        theta_block = []
        for j in range (i, i+7):
            theta_block.append(binary_theta[j])

        decimal_theta.append( decode(theta_block) )   
        # print("bin T per block", theta_block)
   
    theta = np.array(decimal_theta)
    P = np.array(decimal_height)
    info_2 = [P, theta]
    try:
        with open(filename_2,'a') as csvfile:
            csvwriter_2 = writer(csvfile)
            csvwriter_2.writerow(info_2)
            csvwriter_2.close()
    except AttributeError:
            pass        
    area = CalculateArea(theta,P)
    # print("6 height values are ", P, "corresponding 6 theta values are ", theta, " Area covered by these height and angle values is ", area)
    
    
        
  
    
    return area
    


