

import PIL
import sys
import math
import time
import numpy as np

import pygame
import pygame.gfxdraw
import pygame.surfarray as surfarray
from pygame.locals import KEYDOWN, K_q
from PIL import Image
from numpy import zeros

global totalPixel_number,triangle_pixelCountInside_Circle, pixelcountInside_Circle

# CONSTANTS:
# triangle_pixel_values = zeros([970, 970], int)
SCREENSIZE = WIDTH, HEIGHT = 512, 512
#resolution
number_of_columns_in_grid = 256
number_of_rows_in_grid = 256
pixel_size = WIDTH/number_of_columns_in_grid
# print("pixel size is ",pixel_size )
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
GREEN = (61,145,1)
BLUE = (0,0,255)
RED = (255, 0, 0)
INTERSECTION_COLOUR = RED
PADDING = PADTOPBOTTOM, PADLEFTRIGHT = 0, 0
# VARS:
_VARS = {'surf': False}
# _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)


def CalculateArea(theta,P):
    # print("theta values fron theta1 to theta 6 are ", theta, "height values for height1 to height6 are ", P)
    Penalize_area = 1
    # print("H and theta values from CalculateArea function", P,theta)
    pygame.init()
#     we are using set mode here to set the width and height which is screen size
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    
    #if there is 0 value in anyone or more of theta or height value then fitness is zero
    for i in range (len(theta)):
        # if(P[i]>128):
        #     P[i]=P[i]/3
        #     Penalize_area = 2
        
        # elif(theta[i]<=10):
        #     theta[i]=theta[i]*5
        #     Penalize_area = 0.01
            
        if(theta[i] or P[i]) == 0:
            return 0
 
    while True:
        try:
            checkEvents()
            _VARS['surf'].fill(GREY)
            # drawGrid(256)
            drawCircle()
            # time.sleep(3)
            drawTriangles(theta, P)
            # time.sleep(3)
            display = _VARS['surf'] 
            pos = (0,0)
            size = SCREENSIZE
            name = "x.png"
            # print("H and theta values from CalculateArea function", P,theta)
            saveSurface(display,name,pos,size)
            area_covered = findRGB_pixelValue()
            pygame.display.update()
                
            return math.floor(area_covered * Penalize_area)
            break
        except OverflowError:
            return 0

def drawCircle():
    divisions = 256
#     Get cell size
    horizontal_cellsize = (WIDTH - (PADLEFTRIGHT*2))/divisions
    vertical_cellsize = (HEIGHT - (PADTOPBOTTOM*2))/divisions
    circle_center = 0 + PADLEFTRIGHT + (horizontal_cellsize*128), 0 + PADTOPBOTTOM + (vertical_cellsize*128) 
    
#     circle(surface, color, center, radius, width=0, draw_top_right=None, draw_top_left=None, draw_bottom_left=None, draw_bottom_right=None) -> Rect
    pygame.draw.circle(_VARS['surf'], BLACK, circle_center, 128*vertical_cellsize, 1) 
    pygame.display.update()
    # time.sleep(1)

def find_triangleCorners(theta,p):
#     print("theta and p values from find_triangleCorners function", theta,P)
    a1=90
    a2=0
    a3=90+ int(theta[0])

    for i in range (len(theta)):
        A=[[np.cos(np.radians(a1)),np.sin(np.radians(a1))],
           [np.cos(np.radians(a2+(theta[i]/2))),np.sin(np.radians(a2+theta[i]/2))],
           [np.cos(np.radians(a3)),np.sin(np.radians(a3))]]
        B=[0,p[i],0]

        solutions=[[0,0],
                   np.linalg.solve(A[:2],B[:2]),
                   np.linalg.solve(A[1:],B[1:])]
        try:
            triangles=np.append(triangles,[solutions],axis=0)
        except:
            triangles=[solutions]

        a1=theta[i]+a1
        a2=theta[i]+a2
        a3=theta[i]+a3
#     print("x value of point 2 of triangle 1 is ",triangles[0][1][0])
    return triangles


def drawTriangles(theta,P):
#     print("theta and p values from drawTriangle function", theta,P)
    divisions = 256
    horizontal_cellsize = (WIDTH - (PADLEFTRIGHT*2))/divisions
    vertical_cellsize = (HEIGHT - (PADTOPBOTTOM*2))/divisions
    
    triangle_corners = find_triangleCorners(theta,P)
    
    for i in range(6):
    
            P1_T =  0 + PADLEFTRIGHT + (horizontal_cellsize*128), 0 + PADTOPBOTTOM + (vertical_cellsize*128)

            P2_T =  P1_T[0] + (horizontal_cellsize*triangle_corners[i][1][0]),  P1_T[1] + (vertical_cellsize*triangle_corners[i][1][1])

            P3_T =  P1_T[0] + (horizontal_cellsize*triangle_corners[i][2][0]),  P1_T[1] + (vertical_cellsize*triangle_corners[i][2][1])

            # pygame.gfxdraw.filled_trigon(_VARS['surf'],  int(P1_T[0]), int(P1_T[1]),int(P2_T[0]),  int(P2_T[1]),  int(P3_T[0]), int(P3_T[1]) , GREEN)
            pygame.gfxdraw.filled_trigon(_VARS['surf'],  int(math.ceil(P1_T[0])), int(math.ceil(P1_T[1])),int(math.ceil(P2_T[0])),  int(math.ceil(P2_T[1])),  int(math.ceil(P3_T[0])), int(math.ceil(P3_T[1])) , GREEN)

            pygame.display.update()
            # time.sleep(1)

def findRGB_pixelValue():
    # Create a PIL.Image object
    triangle_image = Image.open("x.png")
    # Convert to RGB colorspaceGRID_CIRCLE_TRIANGLES.png
    triangle_image_rgb = triangle_image.convert("RGB")
#     rgb_pixel_value = red_image_rgb.getpixel((969,969))
    
    totalPixel_number = 0
    triangle_pixelCountInside_Circle = 0
    pixelcountInside_Circle = 0
    rows, cols = (512, 512)
    global triangle_pixel_values
    triangle_pixel_values = [[0]*cols]*rows
    divisions = 256
    horizontal_cellsize = (WIDTH - (PADLEFTRIGHT*2))/divisions
    vertical_cellsize = (WIDTH - (PADLEFTRIGHT*2))/divisions
    circle_center = 0 + PADLEFTRIGHT + (horizontal_cellsize*128), 0 + PADTOPBOTTOM + (vertical_cellsize*128)
    radius = horizontal_cellsize*128
    
# looping through all pixels in image and storing rgb color value in 2D array of size equal to image
    for x in range(512):
           for y in range(512):
            
            # totalPixel_number,triangle_pixelCountInside_Circle, pixelcountInside_Circle
           
            #    total count
               totalPixel_number+=1
               
               if triangle_image_rgb.getpixel((x,y))== GREEN:
                # _VARS['surf'].set_at((x,y),BLUE)
                
                # pygame.display.update()
                               
                # inside circle triangle pixel count
                if calculateDistance(circle_center[0],circle_center[1],x,y) <= radius:
                #    _VARS['surf'].set_at((x,y),INTERSECTION_COLOUR)
                   triangle_pixelCountInside_Circle += 1
                #    pygame.display.update()
                              
               if calculateDistance(circle_center[0],circle_center[1],x,y) <= radius:
                   pixelcountInside_Circle += 1
    
    Circle_area = pixel_size * pixelcountInside_Circle*1.00
    AreaCovered_inside_circle = pixel_size * triangle_pixelCountInside_Circle
        
    # print(" Circle_area = ", Circle_area, "AreaCovered_inside_circle = ",AreaCovered_inside_circle, "PercentageOfAreaCovered = ", ( (AreaCovered_inside_circle /Circle_area) *100.00) )
     
    return ((AreaCovered_inside_circle/411718.00)*100.00)

def calculateDistance(x1,y1,x2,y2): 
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

def saveSurface(display,name,pos,size):
    image =pygame.Surface(size)
    image.blit(display,(0,0),(pos,size))
    pygame.image.save(image,name)

def checkEvents():
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            time.sleep(1)
            pygame.quit()
            sys.exit()


