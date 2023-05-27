import PIL
from PIL import Image
import numpy as np
from numpy import zeros
from pathlib import Path
import math
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import itertools

im = Image.open(r"ArleighBrukeShip.png")
new_image = im.resize((50, 50))
new_image.save('ArleighBrukeShip_50.png')

x_co_ordinates = [24,25,24,25,24,25,24,25,24,25,24,25,24,25,24,25]
y_co_ordinates = [21,21,22,23,23,23,24,24,25,25,26,26,27,27,28,28]

im_2 = Image.open(r"ArleighBrukeShip_50.png")
width, height = im_2.size
im_2 =np.array(im_2)
combinedAll = np.zeros((im_2.shape[0],im_2.shape[1],im_2.shape[2]))

path = r'ArleighBrukeShip_50.png'
image_file = Image.open(path)
center_x, center_y = 24, 24 
n = 16
r = 6
total_combinations = math.comb(n,r)

dest_angle = 180
min_dis_defense,max_dis_defense = 0, 13
#parameters for poeple with binocular
min_dis_binocular, max_dis_binocular = 0, 20

#we have approximately 20 pixels to represent distance coverage
#for defense with maximum distance coverage of 13 km, ref_real_dis_defense = 20/13
ref_to_real_dist_defense = 1.5
#for visual sensor with maximum distance coverage of 20 km, ref_real_dis_defense = 20/20 = 1
ref_to_real_dist_binocular = 1
# print("START")
combinedAll_temp = np.array([])


def combination(n,r):
    # Generate combinations
    combinations = list(itertools.combinations(range(0, n), r))
    
    # Print the combinations
    # print("Combinations: ", combinations)
    return combinations

def distance(center_x,center_y, dest_x, dest_y, ref_to_real_dist):
   
    p = np.array([center_x, center_y])
    q = np.array([dest_x, dest_y])
    eDistance = math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
    return eDistance 

# intesity calculation based on linear distance
def strength_dis(min_dis,max_dis,dist,sp,style,c=1):
    
    #print(style)
    if dist < min_dis or dist > max_dis:
        return 0.0
    
    #Inverse Normalized Function
    if style=="inv_norm":
        return sp - ((dist-min_dis)/ (max_dis-min_dis))
    
    #Exponential Decay Function
    if style=="exponent":
        return 1/math.exp(c*((dist-min_dis)))
    
    # Piece-wise Decay Function:
    if style=="piece_wise":
        if dist>0 and dist < 0.025 * max_dis:
            return 0.9
        elif dist >= 0.025 * max_dis and dist < 0.045 * max_dis:
            return 0.7
        elif dist >= 0.045 * max_dis and dist < 0.2 * max_dis:
            return 0.2
        else:
            return 0.05
        
    #Exponential Decay Function
    if style=="radar_exp":
        return 1/math.exp((c*dist)/(max_dis-min_dis))
    
# intesity calculation based on angular distance only used for defenses  
def strength_sector(min_dis,max_dis,dist,angle, relative_angle,style,c):
    
    if dist < min_dis or dist > max_dis:
        return 0.0
    
    #getAngle() can return both relativeAngle or (360 - relativeAngle), the portion bellow deals with it
    
    if relative_angle > angle/2 and (360 - relative_angle) > angle/2:
        return 0.0 
    
    if relative_angle > angle:
        relative_angle = 360 - relative_angle       
                                                                                                
    dist_str = 0.0
    dist_str = strength_dis(min_dis,max_dis,dist,1,style,c)
   
    angular_strength = 1 - (2 * relative_angle/ (angle))
    entity_strength = (dist_str+angular_strength)/2

    # print("entity_Sector_strength ", entity_strength )
    return entity_strength


#combined intesity calculation based on both linear and angular distance 
def decay(center_x,center_y, dest_x, dest_y, min_dis,max_dis,angle, relative_angle,ref_to_real_dist,style,c):
     
    dist = distance(center_x,center_y, dest_x, dest_y, ref_to_real_dist)
    
    if angle == 360:
        entity_strength = strength_dis(min_dis,max_dis,dist,1,style, c)
        
    else:
         entity_strength = strength_sector(min_dis,max_dis,dist,angle, relative_angle, style,c)

    # print("decay pixel value ", entity_strength)
    return entity_strength

combinations_list = combination(n,r)

def fitness_function(combinations_list):
    container = np.array([])
    image = cv2.imread(path)
    #common parameters for all assets
 
    # parameters for defense for 50 x 50 image
    center_x_MK45,center_y_MK45 = 25,21
    center_x_MK61,center_y_MK61 = 25,28
  
    coverage_combined = 0
    combinedAll_temp = np.array([])
    dest_angle_MK45 = 180
    # print("Combinations ", combinations_list)
#combinations function return structure
#[ (1,2,3,4,5,6), (7,8,9,10,11,12)......] 8008 sub lists inside the list
#8008 different combinations of 6 number possible out of 16, which is the range ofr k 
    # for k in range (total_combinations,1,1):
    for k in range(len(combinations_list)-1, -1, -1):    
         #for every 8008 combinations of 6 locations of binocular from 16 possible location options
        #subtracting 1 since combinations list will have values from 0-15
        # For every pixel we are assigning intensity values to it depending on location of binoculars
        #will save total intensity value for each and every combination
        center_binocular1 = combinations_list[k][0] 
        # print("k value", k, "  center_binocular1 index value between 0-15 ",combinations_list[k][0])
        center_binocular2 = combinations_list[k][1] 
        # print("k value", k, "  center_binocular1 index value between 0-15 ",combinations_list[k][1])
        center_binocular3 = combinations_list[k][2] 
        # print("k value", k, "  center_binocular1 index value between 0-15 ",combinations_list[k][2])
        center_binocular4 = combinations_list[k][3] 
        # print("k value", k, "  center_binocular1 index value between 0-15 ",combinations_list[k][3])
        center_binocular5 = combinations_list[k][4] 
        # print("k value", k, "  center_binocular1 index value between 0-15 ",combinations_list[k][4])
        center_binocular6 = combinations_list[k][5] 
        # print("k value", k, "  center_binocular1 index value between 0-15 ",combinations_list[k][5])
        # print(n*30,=)
        #traversing image once
        #when k value is something lets looks at the co_ordinates
        # print("when k value is ", k," the co_ordinates are ", combinations_list[k])
        for i in range(width):
            for j in range(height):
                print("when k value is ", k," the co_ordinates are ", combinations_list[k])
                # for MK45
                #any orientation value from 0 to 180 that we get for 1st assest (mk45) from our chromosome
                # 90 is the value for absolute angle of coverage from principal axis .i.e. for mk45 it is +-45 degree from principal axis. Therefore absolute angle coverage = 90 
                coverage_MK45 = decay(center_y_MK45,  center_x_MK45, i, j, min_dis_defense, max_dis_defense, 90, dest_angle, ref_to_real_dist_defense, "piece_wise", 0.5)
                print("coverage_MK45",coverage_MK45)
                coverage_MK61 = decay(center_y_MK61,  center_x_MK61, i, j, min_dis_defense, max_dis_defense, 90, dest_angle, ref_to_real_dist_defense, "piece_wise", 0.5)
                print("coverage_MK61",coverage_MK61)
                # 180 is the value for possible angle of coverage from principal axis .i.e. for people with binocular it is +-90 degree from principal axis. Therefore absolute angle coverage = 180
                coverage_binocular_1 = decay(y_co_ordinates[center_binocular1], x_co_ordinates[center_binocular1], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle, ref_to_real_dist_binocular, "inv_norm", 1.0)
                print("coverage_binocular_1",coverage_binocular_1)
                coverage_binocular_2 = decay(y_co_ordinates[center_binocular2], x_co_ordinates[center_binocular2], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle, ref_to_real_dist_binocular, "inv_norm", 1.0)
                print("coverage_binocular_2",coverage_binocular_2)
                coverage_binocular_3 = decay(y_co_ordinates[center_binocular3], x_co_ordinates[center_binocular3], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle, ref_to_real_dist_binocular, "inv_norm", 1.0)
                print("coverage_binocular_3",coverage_binocular_3)
                coverage_binocular_4 = decay(y_co_ordinates[center_binocular4], x_co_ordinates[center_binocular4], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle, ref_to_real_dist_binocular, "inv_norm", 1.0)
                print("coverage_binocular_4",coverage_binocular_4)
                coverage_binocular_5 = decay(y_co_ordinates[center_binocular5], x_co_ordinates[center_binocular5], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle, ref_to_real_dist_binocular, "inv_norm", 1.0)
                print("coverage_binocular_5",coverage_binocular_5)
                coverage_binocular_6 = decay(y_co_ordinates[center_binocular6], x_co_ordinates[center_binocular6], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle, ref_to_real_dist_binocular, "inv_norm", 1.0)
                print("coverage_binocular_6",coverage_binocular_6)
                coverage_combined = coverage_combined + (coverage_MK45 + coverage_MK61 + coverage_binocular_1 + coverage_binocular_2 + coverage_binocular_3 + coverage_binocular_4 + coverage_binocular_5 + coverage_binocular_6)
                print("coverage_combined", coverage_combined , " k value ", k)

        #combined intensity value for 1 set of resource allocation possibility, 1 intensity value (combining intensities of every pixels) for 1 set of allocation possibility
        # combinedAll = np.append(combinedAll, coverage_combined)
        # print("coverage_combined",coverage_combined)
        container = np.append(container, coverage_combined)
        # print ("Container ",container)
        #after traversing image once make combined coverage zero so that we can calculate it again for a new combination of resource allocation``
        coverage_combined = 0
    
    print("length of combinedAll", len(container))
    print("combinedAll VALUES ", container[0])
    max_index = np.argmax(container[0])
    optimum_fitness_value = container[max_index]
    print("Max index ", max_index, " allocation at max index ", combinations_list[max_index], "Fitness value at max_index ", optimum_fitness_value)
    print("Max index+1 ", max_index+1, " allocation at max index ", combinations_list[max_index+1], "Fitness value at max_index ", container[max_index+1])
    
    #this wont work since cannot iterate over float
    # container_2 = container.tolist()

    # flat_list = [num for sublist in container_2 for num in sublist]
    # max_number = max(flat_list)
    # min_number = min(flat_list)
    # max_index = np.argmax(container_2)
    # min_index = np.argmin(container_2)
    # print("Maximum intensity value:", max_number, " max index ", max_index)
    # print("Minimum intensity value:", min_number," min index ", min_index)

      
    # combined_All = np.sum(combinedAll_temp)
    # print("combined_All",combined_All)
    # combinedAll_temp = np.empty( shape=(0, 0) )




combinations_list = combination(n,r)
fitness_function(combinations_list)