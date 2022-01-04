import cv2 as cv
import numpy as np
import os
from time import time
# from windowcapture import WindowCapture
# from vision import Vision
from environment import Environment

# initialize the Environment class
env = Environment('BlueStacks') 

# print(wincap.list_window_names())

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = env.vision.get_screenshot()


    cv.imshow('Computer Vision', screenshot)


    # debug the loop rate
    print('FPS %3.0f'%(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # press 'p' to save screenshot 
    key = cv.waitKey(25)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    if key == ord('p'):
        cv.imwrite('images/screenshots/{}.jpg'.format(loop_time), screenshot)

print('Done.')