import win32api
import win32.lib.win32con as win32con
import win32gui
import time

TICK = 0.1
DEFAULT_SIZE_X = 758
DEFAULT_SIZE_Y = 615
MENU_HEIGHT = 51
CELL_Y_OFFSET = 10
CELL_GAP_X = 54
CELL_GAP_Y = 27
PLAYER_MENU_OFFSETS = (490, 505)
PLAYER_MENU_GAP_X = 29.25
PLAYER_MENU_ORDER = {'player': 0, 'spells': 1, 'inventory': 2}


class Window:
    def __init__(self, hwnd, name):
        self.hwnd = hwnd
        self.name = name
        self.resize()
        self.dim = self.get_dim()

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def _window_enumeration_handler(hwnd, top_windows):
        name = win32gui.GetWindowText(hwnd)
        if 'Dofus Retro' in name:
            top_windows.append(Window(hwnd, name))

    @staticmethod
    def list_windows():
        windows = []
        win32gui.EnumWindows(Window._window_enumeration_handler, windows)
        return windows

    def resize(self, minimize=False):
        dim = self.get_dim()
        if minimize:
            y = win32api.GetSystemMetrics(1) - 30
            win32gui.MoveWindow(self.hwnd, dim['left'], y, DEFAULT_SIZE_X, DEFAULT_SIZE_Y, True)
        else:
            win32gui.MoveWindow(self.hwnd, 0, 0, DEFAULT_SIZE_X, DEFAULT_SIZE_Y, True)

    def get_dim(self):
        dim = win32gui.GetWindowRect(self.hwnd)
        size_x = dim[2] - dim[0]
        size_y = dim[3] - dim[1]
        return {"left": dim[0], "top": dim[1], "right": dim[2], "bottom": dim[3], "size_x": size_x, "size_y": size_y}

    def minimize_window(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)
        time.sleep(TICK)

    def click(self, x=0, y=0):
        # win32gui.SetForegroundWindow(self.hwnd)
        time.sleep(TICK)
        lp = win32api.MAKELONG(x, y - CELL_GAP_Y)
        # win32api.SetCursorPos((x + self.dim['left'], y + self.dim['top']))
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, lp)
        time.sleep(TICK)
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lp)

    def click_cell(self, cell):
        y, x = divmod(cell, 14.5)
        _x = int(x * CELL_GAP_X)
        _y = int(y * (CELL_GAP_Y / 2)) + MENU_HEIGHT
        # print(_x, _y)
        self.click(_x, _y)

    def toggle_menu(self, index):
        x, y = PLAYER_MENU_OFFSETS
        x += int(index * PLAYER_MENU_GAP_X)
        self.click(x, y)
        time.sleep(TICK * 5)


if __name__ == "__main__":
    windows = Window.list_windows()
    xelit = windows[0]
    print(xelit)
    # xelit.click_cell(448)
    xelit.toggle_menu(PLAYER_MENU_ORDER['inventory'])
