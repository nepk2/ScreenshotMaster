from io import BytesIO
from ctypes import c_size_t, memmove, windll
from ctypes.wintypes import BOOL, HANDLE, HWND, LPVOID, UINT
import pyautogui as pg
from PIL import Image


def copy_image_to_clipboard(screenshot):
    HGLOBAL = HANDLE
    SIZE_T = c_size_t
    GHND = 0x0042
    GMEM_SHARE = 0x2000

    GlobalAlloc = windll.kernel32.GlobalAlloc
    GlobalAlloc.restype = HGLOBAL
    GlobalAlloc.argtypes = [UINT, SIZE_T]

    GlobalLock = windll.kernel32.GlobalLock
    GlobalLock.restype = LPVOID
    GlobalLock.argtypes = [HGLOBAL]

    GlobalUnlock = windll.kernel32.GlobalUnlock
    GlobalUnlock.restype = BOOL
    GlobalUnlock.argtypes = [HGLOBAL]

    CF_DIB = 8

    OpenClipboard = windll.user32.OpenClipboard
    OpenClipboard.restype = BOOL
    OpenClipboard.argtypes = [HWND]

    EmptyClipboard = windll.user32.EmptyClipboard
    EmptyClipboard.restype = BOOL
    EmptyClipboard.argtypes = None

    SetClipboardData = windll.user32.SetClipboardData
    SetClipboardData.restype = HANDLE
    SetClipboardData.argtypes = [UINT, HANDLE]

    CloseClipboard = windll.user32.CloseClipboard
    CloseClipboard.restype = BOOL
    CloseClipboard.argtypes = None

    #################################################

    image = screenshot

    # output = StringIO()
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    hData = GlobalAlloc(GHND | GMEM_SHARE, len(data))
    pData = GlobalLock(hData)
    memmove(pData, data, len(data))
    GlobalUnlock(hData)

    OpenClipboard(None)
    EmptyClipboard()
    SetClipboardData(CF_DIB, pData)
    CloseClipboard()