from input.window import Window
from input.keyboard import Keyboard
from config import PLAYERS, BINARY
import time
import win32com.client

COORD_USERNAME = (108, 192)
COORD_PASSWORD = (108, 260)
COORD_SUBMIT_BT = (160, 320)

COORD_SERVER = (120, 304)
COORD_PLAYER_1 = (120, 304)
COORD_PLAY = (368, 443)


def get_credentials(path):
    text = open(path).read().split('\n')
    return {'username': text[0], 'password': text[1]}


if __name__ == '__main__':
    windows = Window.list_windows()
    creds = get_credentials(PLAYERS[0]['secret'])

    # initial_length = len(windows)
    # shell = win32com.client.Dispatch("WScript.Shell")
    # shell.Run(BINARY)
    # shell.AppActivate("Dofus Retro")
    #
    # while len(windows) <= initial_length:
    #     windows = Window.list_windows()
    #     print(windows)
    #     time.sleep(1)


    xelit: Window = windows[0]
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
