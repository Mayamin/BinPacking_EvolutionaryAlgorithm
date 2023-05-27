import PIL
from PIL import Image

import numpy as np
from numpy import zeros
from pathlib import Path
import math
import matplotlib.pyplot as plt
import pandas as pd
import cv2

#manually selected co-ordinates for people with binoculars in a 1920x1080 grid, subject tp change when grid size changes 
# x_co_ordinates = [1528,1602,1526,1600,1527,1601,1525,1603,1524,1601,1526,1601,1527,1598,1525,1603]
# y_co_ordinates = [1839,1839,1862,1858,1867,1882,1939,1936,1965,1975,1997,1997,2064,2057,2121,2122]

#50x50
x_co_ordinates = 24,25,24,25,24,25,24,25,24,25,24,25,24,25,24,25
y_co_ordinates = 21,21,22,23,23,23,24,24,25,25,26,26,27,27,28,28

# path = Path("/home/mraha/BinPacking-2023 (copy)/ArleighBrukeShip.png")
# path = r'ArleighBrukeShip.png'
# image_file = Image.open(path)

#resize image to size 50x50
im = Image.open(r"ArleighBrukeShip.png")

# Size of the image in pixels (size of original image)
# (This is not mandatory)
# width, height = im.size
# print("Image width,height ",  width, height)

#resize
new_image = im.resize((50, 50))
new_image.save('ArleighBrukeShip_50.png')

im_2 = Image.open(r"ArleighBrukeShip_50.png")
im_2 =np.array(im_2)
combinedAll = np.zeros((im_2.shape[0],im_2.shape[1],im_2.shape[2]))
# print(" Resized Image width, height ",im_2.size)

path = r'ArleighBrukeShip_50.png'
image_file = Image.open(path)

center_x, center_y = 24, 24 


def distance(center_x,center_y, dest_x, dest_y, ref_to_real_dist):
   
    p = np.array([center_x, center_y])
    q = np.array([dest_x, dest_y])
    eDistance = math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
    # eDistance = np.linalg.norm(p - q)
    # print("Euclidean distance ", eDistance )
        
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

# def getAngle(a, b, c):
#     ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
#     return ang + 360 if ang < 0 else ang

#combined intesity calculation based on both linear and angular distance 
def decay(center_x,center_y, dest_x, dest_y, min_dis,max_dis,angle, relative_angle,ref_to_real_dist,style,c):
     
    dist = distance(center_x,center_y, dest_x, dest_y, ref_to_real_dist)
    
    if angle == 360:
        entity_strength = strength_dis(min_dis,max_dis,dist,1,style, c)
        
    else:
         entity_strength = strength_sector(min_dis,max_dis,dist,angle, relative_angle, style,c)

    # print("decay pixel value ", entity_strength)
    return entity_strength

#every angle value from orientation array goes to relative angle parameter of decay function
def fitness_function(orientation_list, location_list):
    
    image = cv2.imread(path)
    #same for all to maintain uniform intesity calculation
    # ref_to_real_dist = 0.138
    # ref_to_real_dist = 7.2

    ref_to_real_dist_defense = 1.5
    ref_to_real_dist_binocular = 1


    #common parameters for all assets
    w = image.shape[0]
    h = image.shape[1]
    # print(" w h values ", w, h)

    # parameters for defense for 4000x3135 image
    # center_x_MK45,center_y_MK45 = 1564,1787
    # center_x_MK61,center_y_MK61 = 1566,2229

    # parameters for defense for 50 x 50 image
    center_x_MK45,center_y_MK45 = 24,24
    center_x_MK61,center_y_MK61 = 25,24

    min_dis_defense,max_dis_defense = 0, 14

    # gunRangeImg_MK45 = np.zeros((image.shape[0],image.shape[1],image.shape[2]))
    # gunRangeImg_MK61 = np.zeros((image.shape[0],image.shape[1],image.shape[2]))

    #parameters for poeple with binocular
    min_dis_binocular, max_dis_binocular = 0, 14


    #considering visual sensor range for 6 people with binocular 
    # binocular_RangeImg_1 = np.zeros((image.shape[0],image.shape[1],image.shape[2]))
    # binocular_RangeImg_2 = np.zeros((image.shape[0],image.shape[1],image.shape[2]))
    # binocular_RangeImg_3 = np.zeros((image.shape[0],image.shape[1],image.shape[2]))
    # binocular_RangeImg_4 = np.zeros((image.shape[0],image.shape[1],image.shape[2]))
    # binocular_RangeImg_5 = np.zeros((image.shape[0],image.shape[1],image.shape[2]))
    # binocular_RangeImg_6 = np.zeros((image.shape[0],image.shape[1],image.shape[2]))

    #array to store all combined intensity values for each pixel
    # combinedAll = np.zeros((image.shape[0],image.shape[1],image.shape[2]))
    coverage_combined = 0

    combinedAll_temp = np.array([])
    # print("START")
    for i in range(w):
        for j in range(h):

            # for MK45
            #any orientation value from 0 to 180 that we get for 1st assest (mk45) from our chromosome
            dest_angle_MK45 = orientation_list[0]
            # 90 is the value for absolute angle of coverage from principal axis .i.e. for mk45 it is +-45 degree from principal axis. Therefore absolute angle coverage = 90 
            coverage_MK45 = decay(center_y_MK45, center_x_MK45, i, j, min_dis_defense, max_dis_defense, 90, dest_angle_MK45, ref_to_real_dist_defense, "piece_wise", 0.5)
            # print("MK45 coverage returned by decay fucntion ", coverage_MK45 )
            # if coverage_MK45 > 0.000001:
            #     gunRangeImg_MK45[i,j,1] = coverage_MK45 
            #     gunRangeImg_MK45[i,j,2] = 1-coverage_MK45

            # print("coverage_MK45" , coverage_MK45) 

            # for MK61
            dest_angle_MK61 = orientation_list[1]
            # 90 is the value for absolute angle of coverage from principal axis .i.e. for mk45 it is +-45 degree from principal axis. Therefore absolute angle coverage = 90 
            coverage_MK61 = decay(center_y_MK61, center_x_MK61, i, j, min_dis_defense, max_dis_defense, 90, dest_angle_MK61, ref_to_real_dist_defense, "piece_wise", 0.5)
            # print("MK461 coverage returned by decay fucntion ", coverage_MK61 )
            # if coverage_MK61> 0.000001:
            #     gunRangeImg_MK61[i,j,1] = coverage_MK61 
            #     gunRangeImg_MK61[i,j,2] = 1-coverage_MK61
            
            # print("coverage_MK61" , coverage_MK61)

            # for person with binocular similar to visual sensor
            dest_angle_binocular_1 = orientation_list[2]
            # 360 is the value for possible angle of coverage from principal axis .i.e. for people with binocular it is +-90 degree from principal axis. Therefore absolute angle coverage = 180 
            # orientation[2]-[7] contains decimal values within range of 0-180 degree
            coverage_binocular_1 = decay(y_co_ordinates[0], x_co_ordinates[0], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle_binocular_1, ref_to_real_dist_binocular, "inv_norm", 1.0)
            # print("binocular_1  coverage returned by decay fucntion ", coverage_binocular_1  )
            # if coverage_binocular_1 > 0.000001:
            #     binocular_RangeImg_1[i,j,1] = coverage_binocular_1 
            #     binocular_RangeImg_1[i,j,2] = 1-coverage_binocular_1

            # print("coverage_binocular_1_saved" , coverage_binocular_1 )  
            
            dest_angle_binocular_2 = orientation_list[3]
            coverage_binocular_2 = decay(y_co_ordinates[1], x_co_ordinates[1], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle_binocular_2, ref_to_real_dist_binocular, "inv_norm", 1.0)
            # print("binocular_2  coverage returned by decay fucntion ", coverage_binocular_2  )
            # if coverage_binocular_2 > 0.000001:
            #     binocular_RangeImg_2[i,j,1] = coverage_binocular_2 
            #     binocular_RangeImg_2[i,j,2] = 1-coverage_binocular_2
            
            dest_angle_binocular_3 = orientation_list[4]
            coverage_binocular_3 = decay(y_co_ordinates[2], x_co_ordinates[2], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle_binocular_3, ref_to_real_dist_binocular, "inv_norm", 1.0)
            # print("binocular_3  coverage returned by decay fucntion ", coverage_binocular_3  )
            # if coverage_binocular_3 > 0.000001:
            #     binocular_RangeImg_3[i,j,1] = coverage_binocular_3 
            #     binocular_RangeImg_3[i,j,2] = 1-coverage_binocular_3
            
            dest_angle_binocular_4 = orientation_list[5]
            coverage_binocular_4 = decay(y_co_ordinates[3], x_co_ordinates[3], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle_binocular_4, ref_to_real_dist_binocular, "inv_norm", 1.0)
            # print("binocular_4  coverage returned by decay fucntion ", coverage_binocular_4  )
            # if coverage_binocular_4 > 0.000001:
            #     binocular_RangeImg_4[i,j,1] = coverage_binocular_4 
            #     binocular_RangeImg_4[i,j,2] = 1-coverage_binocular_4
            
            dest_angle_binocular_5 = orientation_list[6]
            coverage_binocular_5 = decay(y_co_ordinates[4], x_co_ordinates[4], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle_binocular_5, ref_to_real_dist_binocular, "inv_norm", 1.0)
            # print("binocular_5  coverage returned by decay fucntion ", coverage_binocular_5  )
            # if coverage_binocular_5 > 0.000001:
            #     binocular_RangeImg_5[i,j,1] = coverage_binocular_5
            #     binocular_RangeImg_5[i,j,2] = 1-coverage_binocular_5
            
            dest_angle_binocular_6 = orientation_list[7]
            coverage_binocular_6 = decay(y_co_ordinates[5], x_co_ordinates[5], i, j,  min_dis_binocular, max_dis_binocular, 180, dest_angle_binocular_6, ref_to_real_dist_binocular, "inv_norm", 1.0)
            # print("binocular_6  coverage returned by decay fucntion ", coverage_binocular_6  )
            # if coverage_binocular_6 > 0.000001:
                # binocular_RangeImg_6[i,j,1] = coverage_binocular_6
                # binocular_RangeImg_6[i,j,2] = 1-coverage_binocular_6

            
            coverage_combined = coverage_combined + (coverage_MK45 + coverage_MK61 + coverage_binocular_1 + coverage_binocular_2 + coverage_binocular_3 + coverage_binocular_4 + coverage_binocular_5 + coverage_binocular_6)
            combinedAll_temp = np.append(combinedAll, coverage_combined)
            # print("each value limit coverage_combined ", coverage_combined)

            # if coverage_combined > 0.000001:
            #     combinedAll[i,j,1] = coverage_combined    
            #     combinedAll[i,j,2] = 5.5 - coverage_combined

            # print("coverage_combined ",coverage_combined)
            # combinedAll = np.append(combinedAll, coverage_combined)
            # print("combined_all ", combinedAll)

    # print("="*30)
    # print("combined all size ", np.size(combinedAll))
    # fitness_per_choromosome = np.sum(combinedAll)
    # print("Fitness per chromosome ", fitness_per_choromosome)

    # print("fitness ", coverage_combined)
    combined_All = np.sum(combinedAll_temp)
    print("combined_All",combined_All)
    combinedAll_temp = np.empty( shape=(0, 0))
    # coverage_combined = 0
    # print("Fitness value ", coverage_combined)            
    # return np.sum(fitness_per_choromosome)
    return combined_All
            


            #for MK61
    # print("reached end of grid traversal from fitness_function ")
    # norm_image = cv2.normalize(gunRangeImg, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)
    # print("Normalized Image ")
    # image_file.save("gun-MK45.png", quality=25)
    # print("saved image ")
    # cv2.imwrite('gun-MK45-gradient-test2.png', norm_image)
    # print("Wrote image ")
        
# dummy_o = [180, 0, 0, 0, 0, 0, 0, 0]
# dummy_l = [0, 0, 0, 0, 0, 0, 0, 0, 0]      
# fitness_function(dummy_o, dummy_l)









    






























# import pygame
# import pygame.gfxdraw
# import pygame.surfarray as surfarray
# from pygame.locals import KEYDOWN, K_q


# global totalPixel_number,triangle_pixelCountInside_Circle, pixelcountInside_Circle

# # CONSTANTS:
# # triangle_pixel_values = zeros([970, 970], int)
# SCREENSIZE = WIDTH, HEIGHT = 512, 512
# #resolution
# number_of_columns_in_grid = 256
# number_of_rows_in_grid = 256
# pixel_size = WIDTH/number_of_columns_in_grid
# # print("pixel size is ",pixel_size )
# BLACK = (0, 0, 0)
# GREY = (160, 160, 160)
# GREEN = (61,145,1)
# BLUE = (0,0,255)
# RED = (255, 0, 0)

# INTERSECTION_COLOUR = RED
# PADDING = PADTOPBOTTOM, PADLEFTRIGHT = 0, 0
# # VARS:
# _VARS = {'surf': False}
# # _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
# # Calculate the Euclidean distance 



# def CalculateArea(theta,P):
#     # print("theta values fron theta1 to theta 6 are ", theta, "height values for height1 to height6 are ", P)
#     Penalize_area = 1
#     # print("H and theta values from CalculateArea function", P,theta)
#     pygame.init()
# #     we are using set mode here to set the width and height which is screen size
#     _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    
#     #if there is 0 value in anyone or more of theta or height value then fitness is zero
#     for i in range (len(theta)):
#         # if(P[i]>128):
#         #     P[i]=P[i]/3
#         #     Penalize_area = 2
        
#         # elif(theta[i]<=10):
#         #     theta[i]=theta[i]*5
#         #     Penalize_area = 0.01
            
#         if(theta[i] or P[i]) == 0:
#             return 0
 
#     while True:
#         try:
#             checkEvents()
#             _VARS['surf'].fill(GREY)
#             # drawGrid(256)
#             drawCircle()
#             # time.sleep(3)
#             drawTriangles(theta, P)
#             # time.sleep(3)
#             display = _VARS['surf'] 
#             pos = (0,0)
#             size = SCREENSIZE
#             name = "x.png"
#             # print("H and theta values from CalculateArea function", P,theta)
#             saveSurface(display,name,pos,size)
#             area_covered = findRGB_pixelValue()
#             pygame.display.update()
                
#             return math.floor(area_covered * Penalize_area)
#             break
#         except OverflowError:
#             return 0

# def drawCircle():
#     divisions = 256
# #     Get cell size
#     horizontal_cellsize = (WIDTH - (PADLEFTRIGHT*2))/divisions
#     vertical_cellsize = (HEIGHT - (PADTOPBOTTOM*2))/divisions
#     circle_center = int( 0 + PADLEFTRIGHT + (horizontal_cellsize*128) ), int( 0 + PADTOPBOTTOM + (vertical_cellsize*128) ) 
    
# #     circle(surface, color, center, radius, width=0, draw_top_right=None, draw_top_left=None, draw_bottom_left=None, draw_bottom_right=None) -> Rect
#     pygame.draw.circle(_VARS['surf'], BLACK, circle_center, int(128*vertical_cellsize), 1) 
#     pygame.display.update()
#     # time.sleep(1)

# def find_triangleCorners(theta,p):
# #     print("theta and p values from find_triangleCorners function", theta,P)
#     a1=90
#     a2=0
#     a3=90+ int(theta[0])

#     for i in range (len(theta)):
#         A=[[np.cos(np.radians(a1)),np.sin(np.radians(a1))],
#            [np.cos(np.radians(a2+(theta[i]/2))),np.sin(np.radians(a2+theta[i]/2))],
#            [np.cos(np.radians(a3)),np.sin(np.radians(a3))]]
#         B=[0,p[i],0]

#         solutions=[[0,0],
#                    np.linalg.solve(A[:2],B[:2]),
#                    np.linalg.solve(A[1:],B[1:])]
#         try:
#             triangles=np.append(triangles,[solutions],axis=0)
#         except:
#             triangles=[solutions]

#         a1=theta[i]+a1
#         a2=theta[i]+a2
#         a3=theta[i]+a3
# #     print("x value of point 2 of triangle 1 is ",triangles[0][1][0])
#     return triangles


# def drawTriangles(theta,P):
# #     print("theta and p values from drawTriangle function", theta,P)
#     divisions = 256
#     horizontal_cellsize = (WIDTH - (PADLEFTRIGHT*2))/divisions
#     vertical_cellsize = (HEIGHT - (PADTOPBOTTOM*2))/divisions
    
#     triangle_corners = find_triangleCorners(theta,P)
    
#     for i in range(6):
    
#             P1_T =  0 + PADLEFTRIGHT + (horizontal_cellsize*128), 0 + PADTOPBOTTOM + (vertical_cellsize*128)

#             P2_T =  P1_T[0] + (horizontal_cellsize*triangle_corners[i][1][0]),  P1_T[1] + (vertical_cellsize*triangle_corners[i][1][1])

#             P3_T =  P1_T[0] + (horizontal_cellsize*triangle_corners[i][2][0]),  P1_T[1] + (vertical_cellsize*triangle_corners[i][2][1])

#             # pygame.gfxdraw.filled_trigon(_VARS['surf'],  int(P1_T[0]), int(P1_T[1]),int(P2_T[0]),  int(P2_T[1]),  int(P3_T[0]), int(P3_T[1]) , GREEN)
#             pygame.gfxdraw.filled_trigon(_VARS['surf'],  int(math.ceil(P1_T[0])), int(math.ceil(P1_T[1])),int(math.ceil(P2_T[0])),  int(math.ceil(P2_T[1])),  int(math.ceil(P3_T[0])), int(math.ceil(P3_T[1])) , GREEN)

#             pygame.display.update()
#             # time.sleep(1)

# def findRGB_pixelValue():
#     # Create a PIL.Image object
#     triangle_image = Image.open("x.png")
#     # Convert to RGB colorspaceGRID_CIRCLE_TRIANGLES.png
#     triangle_image_rgb = triangle_image.convert("RGB")
# #     rgb_pixel_value = red_image_rgb.getpixel((969,969))
    
#     totalPixel_number = 0
#     triangle_pixelCountInside_Circle = 0
#     pixelcountInside_Circle = 0
#     rows, cols = (512, 512)
#     global triangle_pixel_values
#     triangle_pixel_values = [[0]*cols]*rows
#     divisions = 256
#     horizontal_cellsize = (WIDTH - (PADLEFTRIGHT*2))/divisions
#     vertical_cellsize = (WIDTH - (PADLEFTRIGHT*2))/divisions
#     circle_center = 0 + PADLEFTRIGHT + (horizontal_cellsize*128), 0 + PADTOPBOTTOM + (vertical_cellsize*128)
#     radius = horizontal_cellsize*128
    
# # looping through all pixels in image and storing rgb color value in 2D array of size equal to image
#     for x in range(512):
#            for y in range(512):
            
#             # totalPixel_number,triangle_pixelCountInside_Circle, pixelcountInside_Circle
           
#             #    total count
#                totalPixel_number+=1
               
#                if triangle_image_rgb.getpixel((x,y))== GREEN:
#                 # _VARS['surf'].set_at((x,y),BLUE)
                
#                 # pygame.display.update()
                               
#                 # inside circle triangle pixel count
#                 if calculateDistance(circle_center[0],circle_center[1],x,y) <= radius:
#                 #    _VARS['surf'].set_at((x,y),INTERSECTION_COLOUR)
#                    triangle_pixelCountInside_Circle += 1
#                 #    pygame.display.update()
                              
#                if calculateDistance(circle_center[0],circle_center[1],x,y) <= radius:
#                    pixelcountInside_Circle += 1
    
#     Circle_area = pixel_size * pixelcountInside_Circle*1.00
#     AreaCovered_inside_circle = pixel_size * triangle_pixelCountInside_Circle
        
#     # print(" Circle_area = ", Circle_area, "AreaCovered_inside_circle = ",AreaCovered_inside_circle, "PercentageOfAreaCovered = ", ( (AreaCovered_inside_circle /Circle_area) *100.00) )
     
#     return ((AreaCovered_inside_circle/411718.00)*100.00)

# def calculateDistance(x1,y1,x2,y2): 
#     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
#     return dist

# def saveSurface(display,name,pos,size):
#     image =pygame.Surface(size)
#     image.blit(display,(0,0),(pos,size))
#     pygame.image.save(image,name)

# def checkEvents():
  
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#         elif event.type == KEYDOWN and event.key == K_q:
#             time.sleep(1)
#             pygame.quit()
#             sys.exit()


