from input.window import Window

POD_DETECT_0 = (449, 228)
POD_DETECT_100 = (508, 228)
ORANGE = 0x66ff
EMPTY = 0xaacfd5

class Inventory:
    def __init__(self, window: Window):
        self.window = window

    def open_inventory(self):
        self.window.toggle_menu(2)

