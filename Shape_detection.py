import cv2 as cv
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

img = cv.imread('Photos\shapes2.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (7, 7), 1)
canny = cv.Canny(blur, 125, 175)
blank = np.zeros_like(img)
imgcontour = img.copy()

def getcontours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        #print(area)   
        if area>500:
            cv.drawContours(imgcontour, cnt, -1, (0, 255, 0), 3)
            para = cv.arcLength(cnt, True) # To find the points or corners of the shapes
            # print(para)
            approx = cv.approxPolyDP(cnt, 0.03*para, True) # To sharpen the corners and get good count, the middle parameter is for the resolution
            # print(len(approx))
            objcorner = len(approx)
            x, y, w, h = cv.boundingRect(approx)

            if objcorner == 3:
                objectType = 'Triangle'
            elif objcorner==4:
                aspratio = w/float(h) # Here for sqaure the approx value will be 1, float is because we have decimal numbers
                if aspratio>0.95 and aspratio<1.04:
                    objectType = 'Sqaure'
                else:
                    objectType='Rectangle'
            elif objcorner==6:
                objectType='Hexagon'
            elif objcorner>7:
                objectType='Circle'
            else: 
                objectType = 'None'
            cv.rectangle(imgcontour, (x, y), (x+w, y+h), (0, 0, 255), thickness=1)
            cv.putText(imgcontour, objectType, (x+(w//2) -10, y+(h//2)-10), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                

getcontours(canny)

imagestack = stackImages(0.6, ([img, imgcontour]))
cv.imshow('Shape_Detection', imagestack)

# ret, thresh = cv.threshold(gray, 50, 255, cv.THRESH_BINARY_INV)
# cv.imshow('Thresh', thresh)
cv.waitKey(0)