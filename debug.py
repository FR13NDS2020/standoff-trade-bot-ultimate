import time
import pyautogui
import win32api
import win32con


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def locate_image(image, region):
    if pyautogui.locateOnScreen(image, region=region, grayscale=True, confidence=0.8) is not None:
        return True
    else:
        return False


def debug_all():
    nazad = (500, 1300, 150, 70)
    if locate_image("./debug_img/nazad.png", nazad):
        click(600, 1340)
        return "debug"

    if pyautogui.pixelMatchesColor(1200, 880, (102, 126, 165), tolerance=10):
        click(1200, 880)
