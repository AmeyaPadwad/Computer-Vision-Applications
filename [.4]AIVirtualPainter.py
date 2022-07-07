from email import header
from json import detect_encoding
import cv2 as cv
import time
from matplotlib.pyplot import draw
import numpy as np
import os
import HandTrackingModule as htm



brushThickness = 15
eraserThickness = 50


#Inputting all the overlay images as headers
folderPath = "virtual painter"
myList = os.listdir(folderPath)
overlayImgs = []

for imgPath in myList:
    image = cv.imread(folderPath + "/" + imgPath)
    overlayImgs.append(image)

#Setting video window
cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
success, img = cap.read()

detector = htm.handDetector(minTrackingConf=0.75)
overlay = overlayImgs[8]
drawColor = (0, 255, 0)
imgCanvas = np.zeros(img.shape, np.uint8)

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)

    #Tracking Hands
    lmList, img = detector.trackhands(img, draw=False)
    if (len(lmList)!=0):
        #tip of index and middle fingers
        inX, inY = lmList[8][1]
        midX, midY = lmList[12][1]
        
        #to check which fingers are up
        fingersUp = detector.fingersUp() 

        #Check selection mode (meaning two fingers are up)
        if fingersUp[1] and fingersUp[2]:
            xPrev, yPrev = 0, 0

            #What is being selected
            if inY<125:
                if 950<inX<1000:
                    overlay = overlayImgs[7] #eraser
                    drawColor = (0,0,0)
                elif 850<inX<950:
                    overlay = overlayImgs[6] #pink
                    drawColor = (147,20,255)
                elif 750<inX<850:
                    overlay = overlayImgs[5] #yellow
                    drawColor = (0,255,255)
                elif 650<inX<750:
                    overlay = overlayImgs[4] #white
                    drawColor = (255,255,255)
                elif 550<inX<650:
                    overlay = overlayImgs[3] #black
                    
                elif 450<inX<550:
                    overlay = overlayImgs[2] #green
                    drawColor = (0,255,0)
                elif 350<inX<450:
                    overlay = overlayImgs[1] #red
                    drawColor = (0,0,255)
                elif 250<inX<350:
                    overlay = overlayImgs[0] #blue
                    drawColor = (255,0,0)
            cv.rectangle(img, (inX, inY), (midX, midY), drawColor, cv.FILLED)

        #Check drawing mode (meaning index finger is up)
        if fingersUp[1] and not fingersUp[2]:
            cv.circle(img, (inX, inY), 15, drawColor, cv.FILLED)

            if xPrev == 0 and yPrev == 0:
                xPrev, yPrev = inX, inY
            
            if drawColor == (0,0,0):
                cv.line(img, (xPrev, yPrev), (inX, inY), drawColor, eraserThickness)
                cv.line(imgCanvas, (xPrev, yPrev), (inX, inY), drawColor, eraserThickness)
            else:
                cv.line(img, (xPrev, yPrev), (inX, inY), drawColor, brushThickness)
                cv.line(imgCanvas, (xPrev, yPrev), (inX, inY), drawColor, brushThickness)

            xPrev, yPrev = inX, inY
    
    imgGray = cv.cvtColor(imgCanvas, cv.COLOR_BGR2GRAY)
    thresh, imgInv = cv.threshold(imgGray, 50, 255, cv.THRESH_BINARY_INV)
    imgInv = cv.cvtColor(imgInv, cv.COLOR_GRAY2BGR)
    img = cv.bitwise_and(img, imgInv)
    img = cv.bitwise_or(img, imgCanvas)

    #Overlays
    img[0:125, 0:1280] = overlay
    cv.imshow("img", img)
    
    if cv.waitKey(1)==27:
        cv.destroyAllWindows()
        break