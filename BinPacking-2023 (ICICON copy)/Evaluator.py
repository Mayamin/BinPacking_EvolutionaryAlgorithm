
import Individual
import math
import numpy as np
import colorUnion
import csv
from csv import writer
from colorUnion import *
# orientation_max_range = 180
# orientation_min_range = 0

# locationNumber_max_range = 16
# locationNumber_min_range = 1

orientation_bits = 8
location_bits = 4

#max as in number of possible principal axis points
orientation_defense_max = 4
orientation_defense_max = 1

orientation_binocular_max = 8
orientation_binocular_min = 1

locationNumber_max_range = 16
locationNumber_min_range = 1

defense_orientation_bits = 2
binocular_orientation_bits = 3
location_bits = 4
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

def decode(binary_array):
    deci = 0
    length = len(binary_array)
#     print("Height block length",length)
    
    #checking if it is height array, otherwise precison 1 by default
    # if length == 8:
    #     for i in range(length):
    #         precision = precision_orientation(orientation_max_range,orientation_min_range,orientation_bits)
    #         val = binary_array[i]*pow(2,7-i)
    #         deci = deci+val*precision
    #     orientation = deci     
    #     return orientation
    #checking if it is locationarray, precison calculation not needed since 2^4 = 16 fits range [0-16] 
    counter = 0
    if length == 2 and counter == 0:
        for i in range(length):
            precision = 1
            deci = deci+ binary_array[i]*pow(2,1-i) 
        point_PA_MK45 = deci
        counter = 1
        return point_PA_MK45
    
    elif length == 2 and counter == 1:
        for i in range(length):
            precision = 1
            deci = deci+ binary_array[i]*pow(2,1-i) 
        point_PA_MK61 = deci
        counter = 1
        return point_PA_MK61
   
    elif length == 3:
        for i in range(length):
            precision = 1
            deci = deci+ binary_array[i]*pow(2,2-i) 
        point_PA_MK45 = deci
        return point_PA_MK45
        
    elif length == 4:
        for i in range(length):
            # print("bin T array", binary_array)
            precision = 1
            deci = deci+ binary_array[i]*pow(2,3-i) 
            # print("theta decimal value",deci)
        
        location = deci
        # print("Location decoded value ", location)
        # decimal_theta = deci
        return  location

  
def  EvaluateX2(individual):
    defense_PA_point_binary = []
    binocular_PA_point_binary = []
    binocular_location_binary = []

    defense_PA_point_decimal = []
    binocular_PA_point_decimal = []
    binocular_location_decimal = []
    x=""
    dummy = []
    
    # print (" lenght of chromosome ",  len(individual.chromosome))
    for i in range(0,len(individual.chromosome)):
        
        # dummy[i] = individual.chromosome[i]
        x = x + str(individual.chromosome[i])
        # print(individual.chromosome[i])
    dummy = x    

    #separating the binary orientation and location values in two separate arrays namely O_binary_val_holder and l_binary_val_holder
    for i in range (0,4):
        defense_PA_point_binary.append(individual.chromosome[i]) 
    for i in range (4,22):
        binocular_PA_point_binary.append(individual.chromosome[i])
    for i in range (22,len(individual.chromosome)):
        binocular_location_binary.append(individual.chromosome[i])  
    
    binary_2bit_temp= []
    binary_3bit_temp= []
    binary_4bit_temp= []

    index_o = 0
    index_temp_1 = 0

    index_l = 0
    index_temp_2 = 0

    #converting each binary orientation value to decimal value and saving 
    for i in range (0, len(defense_PA_point_binary),2): 
        for j in range(i,i+2):
             binary_2bit_temp.append(defense_PA_point_binary[j])
             index_temp_1 += 1
        # print("each 2 bit value taken at a time ", binary_2bit_temp)
        index_temp_1 = 0
        defense_PA_point_decimal.append(decode(binary_2bit_temp))
        # print("corresponding decimal value ", decode(binary_2bit_temp))
        binary_2bit_temp =  []
        index_o += 1

    for i in range (0, len(binocular_PA_point_binary),3):
        for j in range(i,i+3):
             binary_3bit_temp.append(binocular_PA_point_binary[j])
             index_temp_1 += 1
        # print("each 3 bit value taken at a time ", binary_3bit_temp)
        index_temp_1 = 0
        binocular_PA_point_decimal.append(decode(binary_3bit_temp))
        # print("corresponding decimal value ", decode(binary_3bit_temp))
        binary_3bit_temp =  []
        index_o += 1
    
    # print("len(binocular_location_binary) ",len(binocular_location_binary))
    #converting each binary location value to decimal value and saving in l_decimal_val_holder array
    for i in range (0, len( binocular_location_binary),4):
        for j in range(i,i+4):
            # print(i,j)
            binary_4bit_temp.append( binocular_location_binary[j])
            index_temp_2 +=1
        # print("each 4 bit value taken at a time ", binary_4bit_temp)
        index_temp_2 = 0
        binocular_location_decimal.append(decode(binary_4bit_temp))
        # print("corresponding decimal value ", decode(binary_4bit_temp))
        binary_4bit_temp =  []
        index_l += 1

    fitness = fitness_function(defense_PA_point_decimal,  binocular_PA_point_decimal, binocular_location_decimal )

    # print("Fitness of each chromosome ", fitness)
    return fitness
    # return 0
    
  