import numpy as np
import win32gui, win32ui, win32con


class Vision:

    #constants

    # properties
    w = 0 
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, hwnd, resize_to=(960,540)):
        self.hwnd = hwnd

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)

        # account for the window border and titlebar and cut them off
        BORDER_PIXELS = 1
        TITLEBAR_PIXELS = 32

        # check if resize_to is a tuple and then ajust window size 
        if type(resize_to) is tuple:
            self.w = resize_to[0] + (BORDER_PIXELS * 2)
            self.h = resize_to[1] + TITLEBAR_PIXELS + (BORDER_PIXELS * 2)
            win32gui.MoveWindow(self.hwnd, window_rect[0], window_rect[1], self.w, self.h, True)
        else:
            self.w = window_rect[2] - window_rect[0]
            self.h = window_rect[3] - window_rect[1]

        self.w = self.w - (BORDER_PIXELS * 2)
        self.h = self.h - TITLEBAR_PIXELS - (BORDER_PIXELS * 2)
        
        self.cropped_x = BORDER_PIXELS
        self.cropped_y = TITLEBAR_PIXELS + BORDER_PIXELS

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):

        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
        # convert the raw data into a format opencv can read
        dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)