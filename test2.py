
import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision
from itertools import cycle

def diff_percentage(diff):
    copy = diff.copy()
    copy.astype(np.uint8)
    return np.count_nonzero(copy)/copy.size * 100

def main():
    # initialize the WindowCapture class
    wincap = WindowCapture('BlueStacks')
    # print(wincap.list_window_names())

    # get an updated image of the game
    frame1 = wincap.get_screenshot()
    frame2 = wincap.get_screenshot()

    loop_time = time()
    while(True):

        
        # screenshot = wincap.get_screenshot()

        diff = cv.absdiff(frame1, frame2)
        percentage = diff_percentage(diff)
        print('DIFF %3.2f%%'%(percentage))
        cv.putText(diff,'DIFF %3.2f%%'%(percentage), (15,25), cv.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 255), 1, cv.LINE_AA)

        gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)

        # cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        backtorgb = cv.cvtColor(gray,cv.COLOR_GRAY2RGB)

        cv.imshow('Computer Vision', diff)

        # debug the loop rate
        print('FPS %3.0f'%(1 / (time() - loop_time)))
        loop_time = time()

        frame1 = frame2
        frame2 = wincap.get_screenshot()

        # press 'q' with the output window focused to exit.
        # press 'p' to save screenshot 
        key = cv.waitKey(25)
        if key == ord('q'):
            cv.destroyAllWindows()
            break
        if key == ord('p'):
            cv.imwrite('images/screenshots/{}.jpg'.format(loop_time), backtorgb)
        if key == ord('o'):
            cv.imwrite('images/screenshots/{}.jpg'.format(loop_time), frame1)
        
    print('Done.')

if __name__ == "__main__":
    main()

#     BLUE = (255,0,0)
#     GREEN = (0,255.0)

# for c in cnts:
#     area = cv.contourArea(c)
#     if area > 10000:
#         M = cv.moments(c)
#         cx = int(M['m10']/M['m00'])
#         cy = int(M['m01']/M['m00'])
#         cv.drawContours(backtorgb, [c], -1, GREEN, 1, cv.LINE_AA)

# y, x, _ = backtorgb.shape
# l1a = int(x/2-34)
# l1b = int(x/2+34)
# cv.line(backtorgb, (l1a+4,0), (l1a-4,y), BLUE, 1, cv.LINE_AA)
# cv.line(backtorgb, (l1b-4,0), (l1b+4,y), BLUE, 1, cv.LINE_AA)

# cv.line(backtorgb, (l1a-68+14,0), (l1a-68-12,y), BLUE, 1, cv.LINE_AA)
# cv.line(backtorgb, (l1b+68-14,0), (l1b+68+12,y), BLUE, 1, cv.LINE_AA)

# cv.line(backtorgb, (l1a-68-70+24,0), (l1a-68-70-16,y), BLUE, 1, cv.LINE_AA)
# cv.line(backtorgb, (l1b+68+70-24,0), (l1b+68+70+16,y), BLUE, 1, cv.LINE_AA)

# cv.line(backtorgb, (l1a-68-70-70+36,0), (l1a-68-70-70-20,y), BLUE, 1, cv.LINE_AA)
# cv.line(backtorgb, (l1b+68+70+70-36,0), (l1b+68+70+70+20,y), BLUE, 1, cv.LINE_AA)