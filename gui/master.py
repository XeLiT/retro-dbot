import tkinter as tk
from gui.table import Table


class MasterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        tk.Label(self, text="Actions").grid(column=0)
        tk.Label(self, text="GameMapStatus").grid(column=1, row=0)
        self.stop_button = tk.Button(self, text="Stop", relief=tk.FLAT)
        self.stop_button.grid(row=1)
        self.table = Table(self, 15, 15)
        self.table.grid(row=1, column=1, rowspan=15)

    def set_stop_button_action_handler(self, handler):
        self.stop_button.bind("<Button-1>", handler)


class Test:
    def handler(self, *args):
        print('Button Stop pressed')

if __name__ == '__main__':
    t = Test()
    m = MasterGUI()
    m.set_stop_button_action_handler(t.handler)
    m.mainloop()