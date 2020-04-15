import tkinter as tk
from utils.cell import Cell

class Table(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        tk.Frame.__init__(self, parent)
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text=" ", borderwidth=0, width=5, background='pink')
                label.grid(row=row, column=column, sticky="nsew", padx=0, pady=0)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set_background(self, row, column, color):
        widget = self._widgets[row][column]
        widget.configure(background=color)

    def set_data(self, cells: [[Cell]]):
        for i in range(len(cells)):
            for j in range(len(cells[i])):
                cell = cells[i][j]
                widget = self._widgets[i][j]
                widget.configure(background=cell.color, text=cell.text)

