import tkinter as tk

class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        tk.Frame.__init__(self, parent)
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text="%s/%s" % (row, column), borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set_background(self, row, column, color):
        widget = self._widgets[row][column]
        widget.configure(background=color)

class GUIMap:

    def __init__(self) -> None:
        app = tk.Tk()
        self.table = SimpleTable(app, 15, 15)
        self.table.pack(side="top")
        self.table.set_background(0, 0, "yellow")
        app.mainloop()


    # def render_map(self, map):



# if __name__ == "__main__":
#