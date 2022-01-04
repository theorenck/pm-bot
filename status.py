import pytesseract
import cv2 as cv
import numpy as np


# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string
img = cv.imread('images/screenshots/1639498585.940024.jpg')

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

# th = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
th = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,11,1)
kernel = np.ones((1,1), np.uint8)
d = cv.dilate(th, kernel, iterations=2)
e = cv.erode(d,kernel, iterations=2) 

frame = th

# h, w = frame.shape
config = r'--oem 3 --psm 6 outputbase words'
boxes = pytesseract.image_to_data(frame)
# print(boxes)
for i,b in enumerate(boxes.splitlines()):
    if i != 0:
        b = b.split()
        print(b)
        if len(b) == 12:
            x,y,w,h = [int(p) for p in b[6:10]]
            cv.rectangle(img, (x, y), (w+x, h+y), (0,0,255), 1)


print(pytesseract.image_to_string(frame))
cv.imshow('result',img)
cv.waitKey(0)

