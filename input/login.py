from input.window import Window
from input.keyboard import Keyboard
from config import PLAYERS, BINARY, VERSION
from ai.eye import Eye, IMAGE_LOGIN_MOTIF, IMAGE_LOGIN_MOTIF1, IMAGE_LOGIN_MOTIF2
import time
import win32com.client
import os

COORD_USERNAME = (108, 192)
COORD_PASSWORD = (108, 260)
COORD_SUBMIT_BT = (160, 320)

COORD_SERVER = (120, 304)
COORD_PLAYER_1 = (115, 323)
COORD_PLAY = (365, 438)


class Login:
    @staticmethod
    def get_credentials(path):
        text = open(path).read().split('\n')
        return {'username': text[0], 'password': text[1]}

    @staticmethod
    def open_new_window():
        windows = Window.list_windows()
        window_names = list(map(lambda x: x.name, windows))
        for w in windows:
            if w.name == f'Dofus Retro v{VERSION}':
                return w

        initial_length = len(windows)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.Run(BINARY)
        shell.AppActivate("Dofus Retro")
        while len(windows) <= initial_length:
            windows = Window.list_windows()
            time.sleep(1)

        for w in windows:
            if w.name not in window_names:
                return w
        return None

    def __init__(self, player_info) -> None:
        self.player_info = player_info
        self.creds = Login.get_credentials(self.player_info['secret'])
        self.window: Window = Login.open_new_window()
        self.eye: Eye = Eye(self.window)
        self.kb: Keyboard = Keyboard(self.window)

    def login(self):
        self.window.focus()
        self.eye.wait_for_image(IMAGE_LOGIN_MOTIF)
        self.window.frame.click(*COORD_USERNAME)
        self.kb.delete()
        self.kb.write(self.creds['username'])
        time.sleep(0.5)
        self.window.frame.click(*COORD_PASSWORD)
        self.kb.delete()
        self.kb.write(self.creds['password'])
        self.window.click(*COORD_SUBMIT_BT)

        self.eye.wait_for_image(IMAGE_LOGIN_MOTIF1)
        self.window.frame.click(*COORD_SERVER)
        self.window.frame.click(*COORD_SERVER)
        self.eye.wait_for_image(IMAGE_LOGIN_MOTIF2)
        time.sleep(0.5)
        self.window.frame.click(*COORD_PLAYER_1)
        self.window.frame.click(*COORD_PLAY)


if __name__ == '__main__':
    login = Login(PLAYERS[0])
    login.login()