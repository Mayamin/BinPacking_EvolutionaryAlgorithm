# import PIL
# from PIL import Image
# import numpy as np
# from numpy import zeros
# from pathlib import Path
# import math
# import matplotlib.pyplot as plt
# import pandas as pd
# import cv2
# import itertools

# #50x50
# x_co_ordinates = 24,25,24,25,24,25,24,25,24,25,24,25,24,25,24,25
# y_co_ordinates = 21,21,22,23,23,23,24,24,25,25,26,26,27,27,28,28

# #resize image to size 50x50
# im = Image.open(r"ArleighBrukeShip.png")

# #resize
# new_image = im.resize((50, 50))
# new_image.save('ArleighBrukeShip_50.png')

# im_2 = Image.open(r"ArleighBrukeShip_50.png")
# im_2 =np.array(im_2)
# combinedAll = np.zeros((im_2.shape[0],im_2.shape[1],im_2.shape[2]))

# path = r'ArleighBrukeShip_50.png'
# image_file = Image.open(path)

# center_x, center_y = 24, 24 
# im_3 = cv2.imread(path)
# w = im_3.shape[0]
# h = im_3.shape[1]

# def distance(center_x,center_y, dest_x, dest_y, ref_to_real_dist):
#     # Calculate the Euclidean distance 
#     # between points P and Q
#     p = [center_x, center_y]
#     q = [dest_x, dest_y]
#     eDistance = math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
#     #math.dist(p, q)
    
#     return eDistance / ref_to_real_dist

# def strength_dis(min_dis,max_dis,dist,sp,style,c=1):
    
#     #print(style)
#     if dist < min_dis or dist > max_dis:
#         return 0.0
    
#     #Inverse Normalized Function
#     if style=="inv_norm":
#         return sp - ((dist-min_dis)/ (max_dis-min_dis))
    
#     #Exponential Decay Function
#     if style=="exponent":
#         return 1/math.exp(c*((dist-min_dis)))
    
#     # Piece-wise Decay Function:
#     if style=="piece_wise":
#         if dist>0 and dist < 0.025 * max_dis:
#             return 0.9
#         elif dist >= 0.025 * max_dis and dist < 0.045 * max_dis:
#             return 0.7
#         elif dist >= 0.045 * max_dis and dist < 0.2 * max_dis:
#             return 0.2
#         else:
#             return 0.05
        
#     #Exponential Decay Function
#     if style=="radar_exp":
#         return 1/math.exp((c*dist)/(max_dis-min_dis))
    
    
# def strength_sector(min_dis,max_dis,dist,angle, relative_angle,style,c):
#     #print(style)
#     if dist < min_dis or dist > max_dis:
#         return 0.0
    
#     #getAngle() can return both relativeAngle or (360 - relativeAngle), the portion bellow deals with it
    
#     if relative_angle > angle/2 and (360 - relative_angle) > angle/2:
#         return 0.0 
    
#     if relative_angle > angle:
#         relative_angle = 360 - relative_angle       
                                                                                                
#     dist_str = 0.0
#     dist_str = strength_dis(min_dis,max_dis,dist,1,style,c)
#     #print(dist_str)
#     angular_strength = 1 - (2 * relative_angle/ (angle))
#     entity_strength = (dist_str+angular_strength)/2
#     return entity_strength


# def intensity(center_x,center_y, dest_x, dest_y, min_dis,max_dis,angle, relative_angle,ref_to_real_dist,style,c):
    
    
#     dist = distance(center_x,center_y, dest_x, dest_y, ref_to_real_dist)
    
#     if angle == 360:
#         entity_strength = strength_dis(min_dis,max_dis,dist,1,style, c)
        
#     else:
        
#         entity_strength = strength_sector(min_dis,max_dis,dist,angle, relative_angle, style,c)
#     return entity_strength

# #ref_to_real_dist means 1 pixel or unit in image represents how many kms in real life ?
# coverage_v = 0
# coverage_b = 0
# ref_to_real_dist = 1
# ref_to_real_dist_defense = .65
# center_x,center_y = 25,24
# min_dis_visualSensor,max_dis_visualSensor = 0, 14
# min_dis_defense,max_dis_defense = 0, 14
# center_x_MK45,center_y_MK45 = 25,21
# center_x_MK61,center_y_MK61 = 25,28

# # 1st angle parameter = 90 , second angle value can be from 0-180 where a value of zero will yield maximum coverage
# # if we place relative angle = 0 then we can get maximum coverage and Angle is the value for total angle covered using +- angle from principal axis

# for i in range(w):
#     for j in range(h):

#         # coverage_v = coverage_v + intensity(center_y_MK45,center_x_MK45, i, j,min_dis_defense,max_dis_defense, 90,15,ref_to_real_dist_defense, "piece_wise", 0.5)
#         # coverage_v = coverage_v + intensity(center_y_MK61,center_x_MK61, i, j,min_dis_defense,max_dis_defense, 120,15,ref_to_real_dist_defense, "piece_wise", 0.5)
#         # coverage_b = coverage_b + intensity(center_y,center_x, i, j,min_dis_visualSensor,max_dis_visualSensor, 140,15,ref_to_real_dist, "piece_wise", 0.5)

#         # coverage_v = coverage_v + intensity(center_y_MK45,center_x_MK45, i, j,min_dis_defense,max_dis_defense, 180,0,ref_to_real_dist_defense, "piece_wise", 0.5)
#         # coverage_v = coverage_v + intensity(center_y_MK61,center_x_MK61, i, j,min_dis_defense,max_dis_defense, 180,0,ref_to_real_dist_defense, "piece_wise", 0.5)
#         # coverage_b = coverage_b + intensity(center_y,center_x, i, j,min_dis_visualSensor,max_dis_visualSensor, 180,0,ref_to_real_dist, "inv_norm", 1.0)

#         coverage_v = coverage_v + intensity(center_y_MK45,center_x_MK45, i, j,min_dis_defense,max_dis_defense, 90,0,ref_to_real_dist_defense, "piece_wise", 0.5)
#         coverage_v = coverage_v + intensity(center_y_MK61,center_x_MK61, i, j,min_dis_defense,max_dis_defense, 90,0,ref_to_real_dist_defense, "piece_wise", 0.5)
#         coverage_v = coverage_v + intensity(center_y,center_x, i, j,min_dis_defense,max_dis_defense, 140,0,ref_to_real_dist_defense, "piece_wise", 0.5)
#         # coverage_b = coverage_b + intensity(center_y,center_x, i, j,min_dis_visualSensor,max_dis_visualSensor, 360,180,ref_to_real_dist, "inv_norm", 1.0)
#         # coverage_b = coverage_b + decay(center_y,center_x, i, j,min_dis_visualSensor,max_dis_visualSensor, 360,180,ref_to_real_dist, "inv_norm", 1.0)
# # print("Visual Sensor coverage ", coverage_v)
# print("Defense coverage from MK45 and MK 61 in fixed position ", coverage_v)
# # print("Each Visual Sensor coverage when placed in center ", coverage_b)
# # dest_angle_MK45 = 180
# # coverage_MK45 = decay(center_y, center_x, 0, 0, min_dis, max_dis, 90, dest_angle_MK45, ref_to_real_dist, "piece_wise", 0.5)    

def strength_dis(min_dis,max_dis,dist,sp,style,c=1):
    
    #print(style)
    if dist < min_dis or dist > max_dis:
        return 0.0
    
    #Inverse Normalized Function
    if style=="inv_norm":
        return sp - ((dist-min_dis)/ (max_dis-min_dis))
    
strength =  strength_dis(1,20,10,1,"inv_norm", 1.0)
print("strength at distance 10 ", strength )

strength =  strength_dis(1,20,20,1,"inv_norm", 1.0)
print("strength at distance 20 ", strength )