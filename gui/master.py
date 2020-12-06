import tkinter as tk
from gui.table import Table
from utils.patterns.observable import Observable

class MasterGUI(tk.Tk, Observable):
    def __init__(self):
        tk.Tk.__init__(self)
        Observable.__init__(self)
        self.geometry("800x700")
        self.resizable(0, 0)
        self.observers = []

        tk.Label(self, text="Actions", width=20).grid(column=0, row=0, columnspan=3, sticky="n")
        # tk.Label(self, text="GameMapStatus").grid(column=1, row=0)
        self.player_infos = []
        for i in range(10):
            label = tk.Label(self, text="-", borderwidth=0, width=20)
            label.grid(row=(1 + i), column=0, padx=0, rowspan=1, columnspan=3, sticky="n")
            self.player_infos.append(label)

        self.fighting_state = tk.Label(self, text="Not fighting", background='green', borderwidth=0, width=10)
        self.fighting_state.grid(row=(1 + 10 + 1), column=0, sticky="n", padx=0, rowspan=2, columnspan=3)
        self.update_bot_config_search_mob()

        self.table = None
        self.player = None
        self.init_table(40, 40)

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

    def update_bot_config_search_mob(self):
        button = tk.Button(self, text="Searching Mob: False", borderwidth=0, width=20)
        button.grid(row=15, column=0, sticky="nw", padx=0)
        button.bind("<Button-1>", lambda e: self.dispatch(e, "flag_search_mob"))

    def init_table(self, width, height):
        if self.table:
            self.table.pack_forget()
            self.table.destroy()
        self.table = Table(self, rows=height, columns=width)
        self.table.grid(row=1, column=3, rowspan=height)

    def onAfter(self):
        # self.grid(sticky=tk.N+tk.S)
        # self.pack_slaves()
        pass
