

import Individual
import math
import numpy as np
import colorUnion
from colorUnion import *

binary_height = []
binary_theta= []

decimal_height = []
decimal_theta = []
theta_max_range = 120
theta_min_range = 1
theta_bits = 7

# chromosome =  [0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0]


def precision_theta(theta_max_range,theta_min_range,theta_bits):
    # sum = 0
    # for i in range(individual.chromosomeLength):
    precision_value = (theta_max_range - theta_min_range)/(pow(2,theta_bits))                                                                                 

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
    if length ==7:
        for i in range(length):
            
            precision = precision_theta(theta_max_range,theta_min_range,theta_bits)
            val = binary_array[i]*pow(2,6-i)
            deci = deci+(val * precision)
        
        theta = deci
        # decimal_theta = deci
        
        return  theta
    
def  EvaluateX2(individual):
#     print("1st 48 chromosome vlaues")
    for i in range(0, 90-42, 8):
        for j in range (i,i+8):
            binary_height.append(individual.chromosome[j])
#             print(chromosome[j])
    
    # taking the 1st 6 theta values in binary 6*7 = 42,
    # theta_array = [theta1,theta2....theta6]
    
#     print("2nd 42 chromosome vlaues")
    for i in range(48,90,7):
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
        print("bin T per block", theta_block)
#     print("binary theta ",binary_theta)    
#     for i in range(0,len(binary_theta), 7):
#         theta_block = []
#         for j in range (i, i+7):
#             theta_block.append(binary_theta[j])
    
#     print("bin T per block", theta_block)
#     decimal_theta.append(decode(theta_block))
     
    
    
    theta = np.array(decimal_theta)
    P = np.array(decimal_height)
    
    print("h theta values are ",decimal_height, decimal_theta)
    
    area = CalculateArea(theta,P)
    
    return area
    










