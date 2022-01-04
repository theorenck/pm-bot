import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision


loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = cv.imread('images/screenshots/rule.jpg')
    # gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    # blur = cv.GaussianBlur(gray, (5,5), 0)
    # thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    # cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # backtorgb = cv.cvtColor(gray,cv.COLOR_GRAY2RGB)

    y, x, _ = screenshot.shape
    l1a = int(x/2-34)
    l1b = int(x/2+34)
    cv.line(screenshot, (l1a+4,0), (l1a-4,y), (255,0,0), 1, cv.LINE_AA)
    cv.line(screenshot, (l1b-4,0), (l1b+4,y), (255,0,0), 1, cv.LINE_AA)

    cv.line(screenshot, (l1a-68+14,0), (l1a-68-12,y), (255,0,0), 1, cv.LINE_AA)
    cv.line(screenshot, (l1b+68-14,0), (l1b+68+12,y), (255,0,0), 1, cv.LINE_AA)

    # for c in cnts:
    # area = cv.contourArea(c)
    #     if area > 10000:
    #         cv.drawContours(backtorgb, [c], -1, (0,255,0), 1)

    cv.imshow('Computer Vision', screenshot)

    # debug the loop rate
    print('FPS %3.0f'%(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # press 'p' to save screenshot 
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    if key == ord('p'):
        cv.imwrite('images/screenshots/{}.jpg'.format(loop_time), backtorgb)

print('Done.')
