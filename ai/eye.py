import cv2
import time
import config
from input.window import Window
from utils.helpers.rect import Rectangle

IMAGE_DIR = '../utils/refs/' if __name__ == '__main__' else config.MOTIF_DIR
TICK = 0.5
IMAGE_CLOSE_BUTTON = cv2.imread(IMAGE_DIR + 'close_button.png')
IMAGE_MENU_END_FIGHT1 = cv2.imread(IMAGE_DIR + 'end_fight_menu_1.png')
IMAGE_MENU_END_FIGHT_CLOSE_MENU = cv2.imread(IMAGE_DIR + 'end_fight_menu_2.png')
IMAGE_BUTTON_OK = cv2.imread(IMAGE_DIR + 'ok_button.png')
IMAGE_LOGIN_MOTIF = cv2.imread(IMAGE_DIR + 'login_motif.png')
IMAGE_LOGIN_MOTIF1 = cv2.imread(IMAGE_DIR + 'login_motif1.png')
IMAGE_LOGIN_MOTIF2 = cv2.imread(IMAGE_DIR + 'login_motif2.png')


class Eye:
    def __init__(self, window) -> None:
        self.window = window

    @staticmethod
    def match(screenshot, motif, acceptance=0.97, get_position=False):
        result = cv2.matchTemplate(motif, screenshot, cv2.TM_CCOEFF_NORMED)
        if get_position:
            min_val, max_val, min_loc, top_left = cv2.minMaxLoc(result)
            h, w, _ = motif.shape
            return cv2.minMaxLoc(result)[1] > acceptance, Rectangle(top_left, w, h)
        return cv2.minMaxLoc(result)[1], None

    @staticmethod
    def debug(screenshot, top_left, bottom_right):
        cv2.rectangle(screenshot, top_left, bottom_right, 255, 2)
        cv2.imshow('image', screenshot)
        cv2.waitKey(0)

    # Check menus to close, return false if nothing to close, else return True, Rectangle of center of match
    def check_menus(self):
        capture = self.window.frame.capture()



    def wait_for_image(self, motif, timeout=20):
        remaining_time = timeout
        while remaining_time > 0:
            capture = self.window.frame.capture()
            if Eye.match(capture, motif)[0]:
                break
            time.sleep(TICK)
            remaining_time -= TICK
        return self


if __name__ == '__main__':
    w = Window.list_windows()[0]
    capture = w.frame.capture()
    match = Eye.match(capture, IMAGE_BUTTON_OK, 0.99, True)
    print(match)
    Eye.debug(capture, match[1])
