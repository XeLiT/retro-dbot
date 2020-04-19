import tkinter as tk
from gui.table import Table
from utils.contants import *


class MasterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x700")
        self.resizable(0, 0)
        tk.Label(self, text="Actions").grid(column=0)
        tk.Label(self, text="GameMapStatus").grid(column=1, row=0)
        self.player_infos = []
        for i in range(10):
            label = tk.Label(self, text="-", borderwidth=0, width=10)
            label.grid(row=(1 + i), column=0, sticky="n", padx=0, rowspan=3)
            self.player_infos.append(label)

        self.fighting_state = tk.Label(self, text="Not fighting", borderwidth=0, width=10)
        self.fighting_state.grid(row=(1 + 10 + 1), column=0, sticky="n", padx=0, rowspan=2)
        # self.stop_button = tk.Button(self, text="Stop", relief=tk.FLAT)
        # self.stop_button.grid(row=1)
        self.table = None
        self.player = None
        self.init_table(19, 42)

    def set_fighting_state(self, state):
        if state:
            self.fighting_state.configure(text="Fighting", background='yellow')
        else:
            self.fighting_state.configure(text="Not Fighting", background='green')

    def update_player_info(self, entity):
        i = 0
        for key in entity.__dict__.keys():
            if i < len(self.player_infos):
                text = '{}: {}'.format(key, entity.__dict__[key])
                self.player_infos[i].configure(text=text)
            i += 1

    def init_table(self, width, height):
        if self.table:
            self.table.pack_forget()
            self.table.destroy()
        self.table = Table(self, rows=height, columns=width)
        self.table.grid(row=1, column=3, rowspan=height)