from input.window import Window


# TODO
class Inventory:
    def __init__(self, window: Window):
        self.window = window

    def open_inventory(self):
        self.window.toggle_menu(2)

