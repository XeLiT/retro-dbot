from input.window import Window
import win32api, win32gui
import win32.lib.win32con as win32con


COORD_USERNAME = (179, 145)
COORD_PASSWORD = (179, 307)
COORD_SUBMIT_BT = (162, 371)
COORD_SERVER = (125, 365)
COORD_PLAYER_1 = (125, 365)

if __name__ == '__main__':
    xelit = Window.list_windows()[0]
    print(xelit)
    xelit.focus()
    # xelit.frame.capture()
    xelit.click(*COORD_USERNAME)
    # np_edit_wnd = win32gui.GetWindow(xelit.hwnd, win32con.GW_CHILD)
    # print(xelit)
    # print(np_edit_wnd)
    # s = 'LLpeterpan'
    # win32api.SendMessage(np_edit_wnd, win32con.WM_SETTEXT, 0, s)

