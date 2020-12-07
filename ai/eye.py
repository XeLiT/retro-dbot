import cv2
import time
import config
from input.window import Window
from utils.helpers.rect import Rectangle

IMAGE_DIR = '../utils/motifs/' if __name__ == '__main__' else config.MOTIF_DIR
TICK = 0.1
IMAGE_CLOSE_BUTTON = cv2.imread(IMAGE_DIR + 'close_button.png')
IMAGE_CLOSE_BUTTON_2 = cv2.imread(IMAGE_DIR + 'close_button_2.png')
IMAGE_MENU_END_FIGHT1 = cv2.imread(IMAGE_DIR + 'end_fight_menu_1.png')
IMAGE_MENU_END_FIGHT_CLOSE_MENU = cv2.imread(IMAGE_DIR + 'end_fight_menu_2.png')
IMAGE_BUTTON_OK = cv2.imread(IMAGE_DIR + 'ok_button.png')
IMAGE_LOGIN_MOTIF = cv2.imread(IMAGE_DIR + 'login_motif.png')
IMAGE_LOGIN_MOTIF1 = cv2.imread(IMAGE_DIR + 'login_motif1.png')
IMAGE_LOGIN_MOTIF2 = cv2.imread(IMAGE_DIR + 'login_motif2.png')

DEFAULT_ACCEPTANCE = 0.97

class Eye:
    def __init__(self, window) -> None:
        self.window = window

    @staticmethod
    def match(screenshot, motif, acceptance=DEFAULT_ACCEPTANCE, get_position=False):
        result = cv2.matchTemplate(motif, screenshot, cv2.TM_CCOEFF_NORMED)
        if get_position:
            min_val, max_val, min_loc, top_left = cv2.minMaxLoc(result)
            h, w, _ = motif.shape
            return cv2.minMaxLoc(result)[1] > acceptance, Rectangle(top_left, w, h)
        return cv2.minMaxLoc(result)[1] > acceptance, None

    @staticmethod
    def debug(screenshot, top_left, bottom_right):
        cv2.rectangle(screenshot, top_left, bottom_right, 255, 2)
        cv2.imshow('image', screenshot)
        cv2.waitKey(0)

    def wait_for_image(self, motif, timeout=TICK):
        while timeout >= 0:
            capture = self.window.frame.capture()
            match = Eye.match(capture, motif, get_position=True)
            if match[0]:
                return match
            time.sleep(TICK)
            timeout -= TICK
        return timeout > 0, None


if __name__ == '__main__':
    w = Window.list_windows()[0]
    w.resize()
    w.focus()
    capture = w.frame.capture()
    eye = Eye(w)
    match = eye.wait_for_image(IMAGE_CLOSE_BUTTON_2)
    print(match)
    if match[0]:
        w.click(*match[1].center)

        # Eye.debug(capture, match[1].top_left, match[1].bottom_right)


