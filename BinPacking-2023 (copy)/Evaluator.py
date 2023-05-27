
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
orientation_max_range = 180
orientation_min_range = 0

locationNumber_max_range = 16
locationNumber_min_range = 1

orientation_bits = 8
location_bits = 4
# theta_bits = 7


filename_2 = "height_theta_2.csv"
heading_2 =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

with open(filename_2,'w') as csvfile:
#csv writer object
	csvwriter_2 = csv.writer(csvfile)
	#writing
	csvwriter_2.writerow(heading_2)

def precision_orientation(orientation_max_range,orientation_min_range,orientation_bits):
    # sum = 0
    # for i in range(individual.chromosomeLength):
    precision_value = (orientation_max_range- orientation_min_range)/((pow(2,orientation_bits)*1.00) )                                                                                
    # print("precision value ", precision_value)
    return precision_value

# def precision_location(location_max_range,location_min_range,location_bits):
#     # sum = 0
#     # for i in range(individual.chromosomeLength):
#     precision_value = (location_max_range- location_min_range)/((pow(2,location_bits)*1.00) )                                                                                
#     # print("precision value ", precision_value)
#     return precision_value

# def precision_theta(theta_max_range,theta_min_range,theta_bits):
#     # sum = 0
#     # for i in range(individual.chromosomeLength):
#     precision_value = (theta_max_range - theta_min_range)/((pow(2,theta_bits)*1.00) )                                                                                
#     # print("precision value ", precision_value)
#     return precision_value
def decode(binary_array):
    deci = 0
    length = len(binary_array)
#     print("Height block length",length)
    
    #checking if it is height array, precison 1 by default
    if length == 8:
        for i in range(length):
            # print("Enters decode loop")
            precision = precision_orientation(orientation_max_range,orientation_min_range,orientation_bits)
            # print("precision value calculated ", precision)
            #val = binary_array[i]*pow(2,8-(i+1))
            val = binary_array[i]*pow(2,7-i)
            # print("binary to decimal value calculated ", val)
            deci = deci+val*precision
        # print("decoded value ", deci )
        
        # height = deci 
        orientation = deci 
        # print("Orientation decoded value ", orientation)
        return orientation
    #checking if it is locationarray, precison calculation not needed since 2^4 = 16 fits range [0-16] 
    elif length == 4:
        for i in range(length):
            # print("bin T array", binary_array)
            precision = 1
            # val = binary_array[i]*pow(2,4-(i+1))
            # deci = locationNumber_min_range + val * precision
            deci = deci+ binary_array[i]*pow(2,3-i) 
            # print("theta decimal value",deci)
        
        location = deci
        # print("Location decoded value ", location)
        # decimal_theta = deci
        return  location
# def decode(binary_array):
#     deci = 0
#     length = len(binary_array)
# #     print("Height block length",length)
    
#     #checking if it is height array, precison 1 by default
#     if length == 8:
#         for i in range(length):
#             deci = deci+ binary_array[i]*pow(2,7-i)
        
#         height = deci 
        
    
     
#         return height
#     #checking if it is theta array, precison calculation needed
#     elif length == 7:
#         for i in range(length):
#             # print("bin T array", binary_array)
#             precision = precision_theta(theta_max_range,theta_min_range,theta_bits)
#             val = binary_array[i]*pow(2,6-i)
#             deci = deci+(val * precision)
#             # print("theta decimal value",deci)
        
#         theta = deci
#         # decimal_theta = deci
        
#         return  theta
    
def  EvaluateX2(individual):
    binary_height = []
    binary_theta= []
    decimal_height = []
    decimal_theta = []

    O_binary_val_holder = []
    l_binary_val_holder = []

    O_decimal_val_holder = []
    l_decimal_val_holder = []

    x=""
    dummy = []
    
    # print (" lenght of chromosome ",  len(individual.chromosome))
    for i in range(0,len(individual.chromosome)):
        
        # dummy[i] = individual.chromosome[i]
        x = x + str(individual.chromosome[i])
        # print(individual.chromosome[i])
    dummy = x    
    # print("Binary value of each chromosome", x)
    
    # checked the following functions work
    # for i in range (0,8):
    #     O_binary_val_holder.append(individual.chromosome[i]) 

    # for i in range( 64,len(individual.chromosome),4):
    #     print("index ", i)
    #     l_binary_val_holder[i] = individual.chromosome[i]

    #separating the binary orientation and location values in two separate arrays namely O_binary_val_holder and l_binary_val_holder
    for i in range (0,64):
        O_binary_val_holder.append(individual.chromosome[i]) 

    for i in range (64,len(individual.chromosome)):
        l_binary_val_holder.append(individual.chromosome[i])  
    
    binary_8bit_temp= []
    binary_4bit_temp= []

    index_o = 0
    index_temp_1 = 0

    index_l = 0
    index_temp_2 = 0

    #converting each binary orientation value to decimal value and saving in O_decimal_val_holder array
    for i in range (0, len(O_binary_val_holder),8):
        # print ("i values ", i)
        for j in range(i,i+8):
            #  print ("j values ", j)
            #  print ("index_temp_1 values ", index_temp_1)
             binary_8bit_temp.append(O_binary_val_holder[j])
             index_temp_1 += 1
        # print("each 8 bit value taken at a time ", binary_8bit_temp)
        index_temp_1 = 0
        O_decimal_val_holder.append(decode(binary_8bit_temp))
        # print("corresponding decimal value ", decode(binary_8bit_temp))
        binary_8bit_temp =  []
        index_o += 1
    # print("decimal values", O_decimal_val_holder)

    #converting each binary location value to decimal value and saving in l_decimal_val_holder array
    for i in range (0, len(l_binary_val_holder),4):
        # print ("i values ", i)
        for j in range(i,i+4):
            binary_4bit_temp.append(l_binary_val_holder[j])
            index_temp_2 +=1
        # print("each 4 bit value taken at a time ", binary_4bit_temp)
        index_temp_2 = 0
        l_decimal_val_holder.append(decode(binary_4bit_temp))

        # print("corresponding decimal value ", decode(binary_4bit_temp))
        binary_4bit_temp =  []
        index_l += 1


    fitness = fitness_function(O_decimal_val_holder, l_decimal_val_holder)

    # print("Fitness of each chromosome ", fitness)
    return fitness
    
       
    # for i in range (0, len(l_binary_val_holder),4):
    #     for j in range(i,i+4):
    #         binary_4bit_temp[i] = l_binary_val_holder[j]
    #     print("binary location value ", binary_4bit_temp)  
    #     index_l += 1
    #     l_decimal_val_holder[index_l] = decode(binary_4bit_temp) 
    #     print("corresponding decimal value", l_decimal_val_holder[index_l])  
       
   

    


    # y = [1, 1, 1, 1, 1, 1, 1, 1]
    # m = decode(O_binary_val_holder)  
    # print("Orientation binary value ", O_binary_val_holder)
    # print("Orientation value decoded", m)
    # print("Checking Orientation decoding max val ", decode([1,1,1,1,1,1,1,1]))
    # print(" \n Checking location decoding max val ", decode([0,0,1,0]))        
            
        # O_binary_val_holder[i]=  individual.chromosome[i]

    # m = decode(O_binary_val_holder[0])
    # print("Orientation value ", m)

    # for i in range( 64,len(individual.chromosome),4):
    #     print("index ", i)
    #     l_binary_val_holder[i] = individual.chromosome[i]

    # n = decode(l_binary_val_holder[0])
    # print("location value ", n)
        # print (dummy)
    # print(dummy)

    
#     # print("whole chromosome vlaues", individual.chromosome)
#     for i in range(0, len(individual.chromosome)-42, 8):
#         for j in range (i,i+8):
#             binary_height.append(individual.chromosome[j])
# #             print(chromosome[j])
    
#     # taking the 1st 6 theta values in binary 6*7 = 42,
#     # theta_array = [theta1,theta2....theta6]
    
# #     print("2nd 42 chromosome vlaues")
#     for i in range(48,len(individual.chromosome),7):
#         for j in range (i,i+7):
#             binary_theta.append(individual.chromosome[j])
# #             print(chromosome[j])
    
    #decimal H theta separate
    # converting height bin to deci 
#     print("bin h",binary_height) 
#     print("bin theta",binary_theta) 
   
#     print("len bin H , len bin T", len(binary_height), len(binary_theta))
    
    # for i in range(0,len(binary_height), 8):
        
    #     #temporary hold of each binary height values (8 bits)
    #     height_block = []
    #     for j in range (i, i+8):
    #         height_block.append(binary_height[j])

    #     decimal_height.append( decode(height_block) )
        
    
    # for i in range(0,len(binary_theta), 7):
        
    #     #temporary hold of each binary height values (8 bits)
    #     theta_block = []
    #     for j in range (i, i+7):
    #         theta_block.append(binary_theta[j])

    #     decimal_theta.append( decode(theta_block) )   
    #     # print("bin T per block", theta_block)
   
    # theta = np.array(decimal_theta)
    # P = np.array(decimal_height)
    # info_2 = [P, theta]
    
    # try:
    #     with open(filename_2,'a') as csvfile:
    #         csvwriter_2 = writer(csvfile)
    #         csvwriter_2.writerow(info_2)
    #         csvwriter_2.close()
    # except AttributeError:
    #         pass        
    # area = CalculateArea(theta,P)
    # # print("6 height values are ", P, "corresponding 6 theta values are ", theta, " Area covered by these height and angle values is ", area)
    
    
    # return area

   
    


