import enum
import sys
import ctypes

# Reference:
# msdn.microsoft.com/en-us/library/windows/desktop/bb762153(v=vs.85).aspx


class SW(enum.IntEnum):
    HIDE = 0
    MAXIMIZE = 3
    MINIMIZE = 6
    RESTORE = 9
    SHOW = 5
    SHOWDEFAULT = 10
    SHOWMAXIMIZED = 3
    SHOWMINIMIZED = 2
    SHOWMINNOACTIVE = 7
    SHOWNA = 8
    SHOWNOACTIVATE = 4
    SHOWNORMAL = 1


class ERROR(enum.IntEnum):
    ZERO = 0
    FILE_NOT_FOUND = 2
    PATH_NOT_FOUND = 3
    BAD_FORMAT = 11
    ACCESS_DENIED = 5
    ASSOC_INCOMPLETE = 27
    DDE_BUSY = 30
    DDE_FAIL = 29
    DDE_TIMEOUT = 28
    DLL_NOT_FOUND = 32
    NO_ASSOC = 31
    OOM = 8
    SHARE = 26


def ask_admin_access():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        hinstance = ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, sys.argv[0], None, SW.SHOWNORMAL)
        if hinstance <= 32:
            raise RuntimeError(ERROR(hinstance))


# http://docs.python.org/c-api/init.html#PyThreadState_SetAsyncExc
def interrupt_thread(thread_id):
    ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(KeyboardInterrupt))
    if ret == 0:
        raise ValueError("Invalid thread ID")
    elif ret > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    print("Interrupted {}".format(thread_id))



