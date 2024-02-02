import cv2

import time
import math

carCascade= cv2.carCascadeClassifier()
video= cv2.VideoCapture()

WIDTH=1280
HEIGHT=720

def estimateSpeed(location1, location2):
    d_pixels= math.sqrt(math.pow(location2[0]-location[0],2)+math.pow(location2[1]-location1[1],2))
    ppm = 8.8
    d_meters = d_pixels/ppm
    fps = 18
    speed = d_meters * fps * 3.6
    return speed

def trackMultipleObjects():
    rectangleColor= (0,255,0)
    frameCounter= 0
    currentCarID= 0
    fps= 0

    carTracker = {}
    carNumber = {}
    carLocation1= {}
    carLocation2 = {}

    speed = [None] * 1000

    out = cv2.VideoWriter('outTraffic.avi',cv2.VideoWriter_fourcc('M','J'))

