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


path = r'ArleighBrukeShip_50.png'
im_2 = Image.open(r"ArleighBrukeShip_50.png")
im_2 =np.array(im_2)
im_3 = cv2.imread(path)
combinedAll = np.zeros((im_2.shape[0],im_2.shape[1],im_2.shape[2]))

#50x50
x_co_ordinates = 24,25,24,25,24,25,24,25,24,25,24,25,24,25,24,25
y_co_ordinates = 21,21,22,23,23,23,24,24,25,25,26,26,27,27,28,28
center_x, center_y = 24, 24 
w = im_3.shape[0]
h = im_3.shape[1]

def distance(center_x,center_y, dest_x, dest_y, ref_to_real_dist):
    # Calculate the Euclidean distance 
    # between points P and Q
    p = [center_x, center_y]
    q = [dest_x, dest_y]
    eDistance = math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
    #math.dist(p, q)  
    return eDistance / ref_to_real_dist

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
    
    
def strength_sector(min_dis,max_dis,dist,angle, relative_angle,style,c):
    #print(style)
    if dist < min_dis or dist > max_dis:
        return 0.0    
    #getAngle() can return both relativeAngle or (360 - relativeAngle), the portion bellow deals with it    
    if relative_angle > angle/2 and (360 - relative_angle) > angle/2:
        return 0.0 
    
    if relative_angle > angle:
        relative_angle = 360 - relative_angle       
                                                                                                
    dist_str = 0.0
    dist_str = strength_dis(min_dis,max_dis,dist,1,style,c)
    #print(dist_str)
    angular_strength = 1 - (2 * relative_angle/ (angle))
    entity_strength = (dist_str+angular_strength)/2
    return entity_strength


def intensity(center_x,center_y, dest_x, dest_y, min_dis,max_dis,angle, relative_angle,ref_to_real_dist,style,c):
       
    dist = distance(center_x,center_y, dest_x, dest_y, ref_to_real_dist)
    if angle == 360:
        entity_strength = strength_dis(min_dis,max_dis,dist,1,style, c)       
    else:  
        entity_strength = strength_sector(min_dis,max_dis,dist,angle, relative_angle, style,c)
    return entity_strength

def combination(n,r):
    # Generate combinations
    combinations = list(itertools.combinations(range(0, n), r))
    # print("Combinations: ", combinations)
    return combinations

#ref_to_real_dist means 1 pixel or unit in image represents how many kms in real life ?
coverage_v = 0
coverage_b = 0
ref_to_real_dist = .65
# ref_to_real_dist_defense = 0.65
center_x,center_y = 25,24
# min_dis_visualSensor,max_dis_visualSensor = 0, 20
# min_dis_defense,max_dis_defense = 0, 14

min_dis_visualSensor,max_dis_visualSensor = 0, 14
min_dis_defense,max_dis_defense = 0, 14

center_x_MK45,center_y_MK45 = 25,21
center_x_MK61,center_y_MK61 = 25,28
n = 16 
r = 6
allocations = np.array([])
allocations = np.array(combination(n,r))
coverage_combined = 0
#all the debugging statements below worked
# print("type of allocations ",type(allocations))
# # print("Combinations ", allocations)
# center_binocular1 = allocations[0]
# #we are using allocations[i][j] to avoid type error
# print("center_binocular1 = ",center_binocular1, " 1st element ",allocations[0][0])

# # center_binocular2 = allocations[8006] 
# # print("center_binocular2 = ",center_binocular2, " 1st element ",allocations[8006][0])

# #checking if we are able to access co_ordinates perfectly
# print("x(center_binocular1) from system ", x_co_ordinates[allocations[0][0]], "y(center_binocular1) from system ",  y_co_ordinates[allocations[0][0]])

#NOW BINOCUULAR IS ALSO A HYBRID VERSION OF MK45 so the ref to real dis is same and angle is 70 degree from princiapl axis
container = np.array([])

for k in range(len(allocations)-1, -1, -1):
    center_binocular1 = allocations[k][0] 
    # print("k value", k, "  center_binocular1 index value between 0-15 ",allocations[k][0])
    center_binocular2 = allocations[k][1] 
        # print("k value", k, "  center_binocular1 index value between 0-15 ",combinations_list[k][1])
    center_binocular3 = allocations[k][2] 
        # print("k value", k, "  center_binocular1 index value between 0-15 ",combinations_list[k][2])
    center_binocular4 = allocations[k][3] 
        # print("k value", k, "  center_binocular1 index value between 0-15 ",combinations_list[k][3])
    center_binocular5 = allocations[k][4] 
        # print("k value", k, "  center_binocular1 index value between 0-15 ",combinations_list[k][4])
    center_binocular6 = allocations[k][5] 

    for i in range(w):
        for j in range(h):
            # coverage_v = coverage_v + intensity(center_y_MK45,center_x_MK45, i, j,min_dis_defense,max_dis_defense, 90,15,ref_to_real_dist_defense, "piece_wise", 0.5)
            # coverage_v = coverage_v + intensity(center_y_MK61,center_x_MK61, i, j,min_dis_defense,max_dis_defense, 120,15,ref_to_real_dist_defense, "piece_wise", 0.5)
            # coverage_b = coverage_b + intensity(center_y,center_x, i, j,min_dis_visualSensor,max_dis_visualSensor, 140,15,ref_to_real_dist, "piece_wise", 0.5)
            # print("when k value is ", k," the co_ordinates are ", allocations[k])
            # print("k value", k, "  center_binocular1 index value between 0-15 ",allocations[k][0])
            # print("k value", k, "  center_binocular1 index value between 0-15 ",allocations[k][1])
            # print("k value", k, "  center_binocular1 index value between 0-15 ",allocations[k][2])
            coverage_MK45 = intensity(center_y_MK45,  center_x_MK45, i, j, min_dis_defense, max_dis_defense, 90, 0, ref_to_real_dist, "piece_wise", 0.5)
            # print("coverage_MK45",coverage_MK45)
            coverage_MK61 = intensity(center_y_MK61,  center_x_MK61, i, j, min_dis_defense, max_dis_defense, 90, 0, ref_to_real_dist, "piece_wise", 0.5)
            # print("coverage_MK61",coverage_MK61)
            # print("y_co_ordinates[center_binocular1], x_co_ordinates[center_binocular1]",center_binocular1, center_binocular1)
            # 180 is the value for possible angle of coverage from principal axis .i.e. for people with binocular it is +-70 degree from principal axis. Therefore absolute angle coverage = 140
            coverage_binocular_1 = intensity(y_co_ordinates[center_binocular1], x_co_ordinates[center_binocular1], i, j,  min_dis_visualSensor,max_dis_visualSensor, 140, 0, ref_to_real_dist , "piece_wise", 0.5)
            # print("coverage_binocular_1",coverage_binocular_1)
            coverage_binocular_2 = intensity(y_co_ordinates[center_binocular2], x_co_ordinates[center_binocular2], i, j,  min_dis_visualSensor,max_dis_visualSensor, 140, 0, ref_to_real_dist , "piece_wise", 0.5)
            # print("coverage_binocular_2",coverage_binocular_2)
            coverage_binocular_3 = intensity(y_co_ordinates[center_binocular3], x_co_ordinates[center_binocular3], i, j,  min_dis_visualSensor,max_dis_visualSensor, 140, 0, ref_to_real_dist , "piece_wise", 0.5)
            # print("coverage_binocular_3",coverage_binocular_3)
            coverage_binocular_4 = intensity(y_co_ordinates[center_binocular4], x_co_ordinates[center_binocular4], i, j,  min_dis_visualSensor,max_dis_visualSensor, 140, 0, ref_to_real_dist , "piece_wise", 0.5)
            # print("coverage_binocular_4",coverage_binocular_4)
            coverage_binocular_5 = intensity(y_co_ordinates[center_binocular5], x_co_ordinates[center_binocular5], i, j,  min_dis_visualSensor,max_dis_visualSensor, 140, 0, ref_to_real_dist , "piece_wise", 0.5)
            # print("coverage_binocular_5",coverage_binocular_5)
            coverage_binocular_6 = intensity(y_co_ordinates[center_binocular6], x_co_ordinates[center_binocular6], i, j, min_dis_visualSensor,max_dis_visualSensor, 140, 0, ref_to_real_dist , "piece_wise", 0.5)
            # print("coverage_binocular_6",coverage_binocular_6)
            coverage_combined = coverage_combined + (coverage_MK45 + coverage_MK61 + coverage_binocular_1 + coverage_binocular_2 + coverage_binocular_3 + coverage_binocular_4 + coverage_binocular_5 + coverage_binocular_6)
            # print("coverage_combined", coverage_combined , " k value ", k)

    container = np.append(container, coverage_combined)
    # print("Coverage combined ", coverage_combined, "for k = ", k)
    coverage_combined = 0

max_index = np.argmax(container)
optimum_fitness_value = container[max_index]
print("Max index ", max_index, " allocation at max index ", allocations[max_index], "Fitness value at max_index ", optimum_fitness_value)
# print("Max index+1 ", max_index+1, " allocation at max index +1", allocations[max_index+1], "Fitness value at max_index + 1", container[max_index+1])



