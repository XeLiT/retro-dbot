import win32api
import win32.lib.win32con as win32con


class Keyboard:
    def __init__(self, window) -> None:
        self.hwnd = window.hwnd

    def select_to_end(self):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_SHIFT)
        win32api.SendMessage(self.hwnd, win32con.WM_CHAR, win32con.VK_END)

    def delete(self, count=50):
        for _ in range(count):
            win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_DELETE)

    def write(self, content):
        for char in content:
            win32api.SendMessage(self.hwnd, win32con.WM_CHAR, ord(char), 0)

    def enter(self):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)