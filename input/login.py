from input.window import Window
from input.keyboard import Keyboard
from config import PLAYERS
import time

COORD_USERNAME = (108, 192)
COORD_PASSWORD = (108, 260)
COORD_SUBMIT_BT = (160, 320)

COORD_SERVER = (120, 304)
COORD_PLAYER_1 = (120, 304)
COORD_PLAY = (368, 443)


def get_credentials(path):
    text = open(path).read().split('\n')
    return {'username': text[0], 'password': text[1]}


# TODO open process
if __name__ == '__main__':
    creds = get_credentials(PLAYERS[0]['secret'])
    xelit: Window = Window.list_windows()[0]
    kb = Keyboard(xelit)
    xelit.focus()
    xelit.frame.click(*COORD_USERNAME)
    kb.delete()
    kb.write(creds['username'])
    time.sleep(0.5)

    xelit.frame.click(*COORD_PASSWORD)
    kb.delete()
    kb.write(creds['password'])
    xelit.click(*COORD_SUBMIT_BT)
    # TODO wait for queue
