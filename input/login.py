from input.window import Window
from input.keyboard import Keyboard
from config import PLAYERS, BINARY, VERSION
from ai.eye import Eye, IMAGE_LOGIN_MOTIF, IMAGE_LOGIN_MOTIF1, IMAGE_LOGIN_MOTIF2
import time
import input.coordinates as coord
import win32api
from utils.helpers.collection import Collection
import logging


class Login:
    @staticmethod
    def get_credentials(path):
        text = open(path).read().split('\n')
        return {'username': text[0], 'password': text[1]}

    def open_new_window(self):
        windows = Window.list_windows()
        player_window = Collection(windows).find_one(callback=lambda x: self.player_info['name'] in x.name)
        if player_window:
            return player_window
        login_window = Collection(windows).find_one(name=f'Dofus Retro v{VERSION}')
        if login_window:
            return login_window

        try:
            win32api.WinExec(BINARY)
        except Exception as e:
            logging.warning(e)

        while True:
            logging.info(f'Opening new window for {self.player_info["name"]}')
            time.sleep(1)
            window = Collection(Window.list_windows()).find_one(name=f'Dofus Retro v{VERSION}')
            if window:
                return window


    def __init__(self, player_info) -> None:
        self.player_info = player_info
        self.creds = Login.get_credentials(self.player_info['secret'])
        self.window: Window = self.open_new_window()
        self.eye: Eye = Eye(self.window)
        self.kb: Keyboard = Keyboard(self.window)

    def login(self):
        self.window.resize()
        self.window.focus()
        self.eye.wait_for_image(IMAGE_LOGIN_MOTIF)
        self.window.frame.click(*coord.COORD_USERNAME)
        self.kb.delete()
        self.kb.write(self.creds['username'])
        time.sleep(0.5)
        self.window.frame.click(*coord.COORD_PASSWORD)
        self.kb.delete()
        self.kb.write(self.creds['password'])
        self.window.click(*coord.COORD_SUBMIT_BT)

        self.eye.wait_for_image(IMAGE_LOGIN_MOTIF1)
        self.window.frame.click(*coord.COORD_SERVER)
        self.window.frame.click(*coord.COORD_SERVER)
        self.eye.wait_for_image(IMAGE_LOGIN_MOTIF2)
        time.sleep(0.5)
        self.window.frame.click(*coord.COORD_PLAYER_1)
        self.window.frame.click(*coord.COORD_PLAY)


if __name__ == '__main__':
    login = Login(PLAYERS[0])
    login.login()