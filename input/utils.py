import win32api
import win32.lib.win32con as win32con
import win32gui


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def _window_enumeration_handler(hwnd, top_windows):
    name = win32gui.GetWindowText(hwnd)
    if 'Dofus Retro' in name:
        top_windows.append((hwnd, name))

# returns list of tuple (hwnd, name of window)
def list_windows():
    windows = []
    win32gui.EnumWindows(_window_enumeration_handler, windows)
    print(*windows, sep='\n')
    return windows

def minify_window():
    pass

def click_bg(x, y):
    pass


if __name__ == "__main__":
    windows = list_windows()
    w = windows[0][0]
    # win32gui.ShowWindow(w, 5)
    # win32gui.SetForegroundWindow(w)
    q = win32gui.GetWindowPlacement(w)
    print(q)
    a = win32gui.GetWindowRect(w)
    print(a)


# if __name__ == '__main__':
#     click(0, 0)