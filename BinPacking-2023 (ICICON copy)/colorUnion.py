import PIL
from PIL import Image
import numpy as np
from numpy import zeros
from pathlib import Path
import math
import matplotlib.pyplot as plt
import pandas as pd
import cv2

#resize image to size 50x50
im = Image.open(r"ArleighBrukeShip.png")
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

def distance(center_x,center_y, dest_x, dest_y):   
    p = np.array([center_x, center_y])
    q = np.array([dest_x, dest_y])
    eDistance = math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))    
    return eDistance 

# intesity calculation based on linear distance
def strength_dis(min_dis,max_dis,dist,sp,style,c=1):    
    if dist < min_dis or dist > max_dis:
        return 0.0    
    if style=="inv_norm":
        return sp - ((dist-min_dis)/ (max_dis-min_dis))
    if style=="exponent":
        return 1/math.exp(c*((dist-min_dis)))
    if style=="piece_wise":
        if dist>0 and dist < 0.025 * max_dis:
            return 0.9
        elif dist >= 0.025 * max_dis and dist < 0.045 * max_dis:
            return 0.7
        elif dist >= 0.045 * max_dis and dist < 0.2 * max_dis:
            return 0.2
        else:
            return 0.05
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
    dist = distance(center_x,center_y, dest_x, dest_y)    
    if angle == 360:
        entity_strength = strength_dis(min_dis,max_dis,dist,1,style, c)        
    else:
         entity_strength = strength_sector(min_dis,max_dis,dist,angle, relative_angle, style,c)
    return entity_strength

def calculate_angle(x1, y1, x2, y2, x3, y3, x4, y4):
    # Calculate the vectors for the line segments
    vector1 = (x2 - x1, y2 - y1)
    vector2 = (x4 - x3, y4 - y3)   
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]    
    # Calculate the magnitudes of the vectors
    magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)    
    # Calculate the cosine of the angle
    cosine = dot_product / (magnitude1 * magnitude2)    
    # Calculate the angle in radians
    angle_radians = math.acos(cosine)    
    # Convert the angle to degrees
    angle_degrees = math.degrees(angle_radians)    
    return angle_degrees
# # Example usage
# angle = calculate_angle(x1, y1, x2, y2, x3, y3, x4, y4)
#location of gun
center_MK45=[]
# center_x_MK45,center_y_MK45 = 25,21
center_MK45 = 25,21
center_MK61 = []
# center_x_MK61,center_y_MK61 = 25,27
center_MK61 = 25,27
# PA_point for defenses_01 MK45
x_co_ordinates_MK45 = 24, 30, 19, 22
y_co_ordinates_MK45 = 16, 17, 18, 13
# for defenses_02 MK61
x_co_ordinates_MK61 = 19, 23, 27, 30
y_co_ordinates_MK61 = 30, 34, 35, 32
#16 location of binoculars
x_co_ordinates_B = 24,25,24,25,24,25,24,25,24,25,24,25,24,25,24,25
y_co_ordinates_B = 21,21,22,23,23,23,24,24,25,25,26,26,27,27,28,28

#PA point for binocular left b1-b3
x_co_ordinates_Bl = 14,14,14,14,14,14,14,14
y_co_ordinates_Bl = 22,14,24,25,35,27,28,23
#PA point for binocular right
x_co_ordinates_Br = 35,35,35,35,35,35,35,35
y_co_ordinates_Br = 21,24,25,33,27,28,18,28

def fitness_function(defense_PA_point_decimal,  binocular_PA_point_decimal, binocular_location_decimal):    
    image = cv2.imread(path)
    ref_to_real_dist_defense = 1.5
    ref_to_real_dist_binocular = 1
    w = image.shape[0]
    h = image.shape[1]
    min_dis_defense,max_dis_defense = 0, 14
    min_dis_binocular, max_dis_binocular = 0, 14
    coverage_combined = 0
    combinedAll_temp = np.array([])
    #for binoculars
    b_loc_PA = []
    b_loc_temp_PA = []
    b_loc_temp = []
    b_loc = []
    combinedAll = []
    intensity_per_pixel = []

    for i in range (6):
        if i<3:
            b_loc_temp_PA = x_co_ordinates_Bl[(binocular_PA_point_decimal[i]-1)], y_co_ordinates_Bl[(binocular_PA_point_decimal[i]-1)]
            b_loc_PA.append(b_loc_temp_PA)                      
        else:
            b_loc_temp_PA = x_co_ordinates_Br[(binocular_PA_point_decimal[i]-1)], y_co_ordinates_Br[(binocular_PA_point_decimal[i]-1)]
            b_loc_PA.append(b_loc_temp_PA)  

        b_loc_temp =  x_co_ordinates_B[(binocular_location_decimal[i]-1)], y_co_ordinates_B[(binocular_location_decimal[i]-1)]
        b_loc.append(b_loc_temp)

    PA_point_MK45 = []
    PA_point_MK45 = x_co_ordinates_MK45[(defense_PA_point_decimal[0]-1)],y_co_ordinates_MK45[(defense_PA_point_decimal[0]-1)]
    PA_point_MK61 = []
    PA_point_MK61 = x_co_ordinates_MK61[(defense_PA_point_decimal[1]-1)], y_co_ordinates_MK61[(defense_PA_point_decimal[1]-1)]

   #binocular_PA_point_decimal -> 1st 3 values are for location index of 3 binoculars on the left and 3 binoculars on the right
    for i in range(w):
        for j in range(h):         
            alpha_Mk45 = calculate_angle(center_MK45[0],center_MK45[1],PA_point_MK45[0],PA_point_MK45[1],center_MK45[0],center_MK45[1],w,h)
            obj_func_MK45 = decay(center_MK45[1], center_MK45[0], i, j, min_dis_defense, max_dis_defense, 90, alpha_Mk45, ref_to_real_dist_defense, "piece_wise", 0.5)                     
            alpha_Mk61 = calculate_angle(center_MK61[0],center_MK61[1],PA_point_MK61[0],PA_point_MK61[1],center_MK61[0],center_MK61[1],w,h)  
            obj_func_MK61 = decay(center_MK61[1], center_MK61[0], i, j, min_dis_defense, max_dis_defense, 90, alpha_Mk61, ref_to_real_dist_defense, "piece_wise", 0.5)
        
            coverage_MK45 = 0 if  alpha_Mk45>45 else obj_func_MK45
            coverage_MK61 = 0 if  alpha_Mk61>45 else obj_func_MK61
            
            coverage_B = []
            for i in range (6): 
                                                
                    alpha_b = calculate_angle(b_loc[i][0], b_loc[i][1], b_loc_PA[i][0],b_loc_PA[i][1],b_loc[i][0], b_loc[i][1],w,h)
                    obj_func_b =  decay(b_loc[i][1], b_loc[i][0], i, j, min_dis_binocular, max_dis_binocular, 130, alpha_b, ref_to_real_dist_binocular, "inv_norm", 1.0)   
                    coverage_B_temp = 0 if alpha_b > 65 else obj_func_b
                    coverage_B.append(coverage_B_temp)

            bin_sum = np.sum(np.array(coverage_B))
            coverage_combined = coverage_MK45 + coverage_MK61 + bin_sum 
            if coverage_combined > 1:
                print("ALERT coverage_combined > 1 ! and it is " ,coverage_combined )
            
            intensity_per_pixel.append(coverage_combined)
         
    # print("fitness ", coverage_combined)
    combined_All = sum(intensity_per_pixel)
    if combined_All > 2500:
        print("ALERT coverage_combined > 2500 ! and it is ", combined_All)
    
    return combined_All
            










    






























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


