import sched
from time import sleep, time
from numpy import array
import win32gui, win32ui, win32con, win32api

# http://www.kbdedit.com/manual/low_level_vk_list.html
KEY_W = 0x57
KEY_A = 0x41
KEY_S = 0x53
KEY_D = 0x44

KEY_ESCAPE = 0x1B
KEY_RETURN = 0x0D
KEY_SPACE  = 0x20

class Control:

    #constants
    DURATION_TURN = 0.033
    DURATION_WALK = 0.23
    DURATION_RUN = 0.1333
    
    UP    = 0x57
    RIGHT = 0x44
    DOWN  = 0x53
    LEFT  = 0x41

    ACTION_A = 0x0D

    ACTION_IMORTY = 0x1B

    # constructor
    def __init__(self, hwnd):
        self.hwnd = hwnd
        # activate the child window so we can commmunicate like it was on the foreground
        win32gui.SendMessage(self.hwnd , win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)

        self.scheduler= sched.scheduler(time, sleep)

    def send_message(self, idMessage, wParam=None, lParam=None):
        win32gui.SendMessage(self.hwnd , win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
        win32api.SendMessage(self.hwnd, idMessage, wParam, lParam)

    def key_down(self, key, lParam=None):
        self.send_message(win32con.WM_KEYDOWN, key, lParam)

    def key_up(self, key, lParam=None):
        self.send_message(win32con.WM_KEYUP, key, lParam)

    def key_press(self, keys, duration):
        
        def schedule():
            self.scheduler.enter(0, i, self.key_down, argument=(key, 0))
            self.scheduler.enter(duration, i, self.key_up, argument=(key, 0))
            self.scheduler.run()
        
        if type(keys) is list:
            for i, key in enumerate(keys):
                schedule()
        else:
            i, key = 0, keys
            schedule()
            # self.key_down(key,0)
            # sleep(duration)
            # self.key_up(key,0)

    def turn(self, dir):
        dir = self.norm_dir(dir)
        self.key_press(dir, self.DURATION_TURN)
        sleep(0.02)

    def walk(self, dir, steps=1, cooldown_duration = 0.23, step_duration = 0.23):
        dir = self.norm_dir(dir)
        self.key_press(dir, step_duration * steps)
        # cooldown ~ duration of one step, 
        # c = 0.19, works when minimap is active
        sleep(cooldown_duration)

    def run(self, dir, steps=1):
        dir = self.norm_dir(dir)
        self.key_press([self.ACTION_A, dir], self.DURATION_RUN * steps)
        sleep(0.02)

    def toggle_imorty(self):
        self.key_press(self.ACTION_IMORTY, 0.05)
        sleep(0.5)

    def norm_dir(self,dir):
        if type(dir) == str:
            return ord(dir)
        return dir

    def get_actions(self):
        return [
            self.ACTION_A,
            self.UP,
            self.RIGHT,
            self.DOWN,
            self.LEFT
        ]