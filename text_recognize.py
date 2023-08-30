import mss
import cv2 as cv
import numpy as np
import pytesseract
import time
from PIL import Image
# import pyautogui
import keyboard
import re
import json
from functions import click, refresh


def text_recognition():
    print("Start Text recognition")
    with open("recognize.json", 'r') as file:
        config = json.load(file)
    recognize_text = config["Text"]
    def remove(refreshx, refreshy):
        click(refreshx, refreshy)
        time.sleep(0.5)
        click(refreshx, refreshy)
        time.sleep(0.4)
        click(2000, 470)  # remove item

    def sell(price):
        click(config["FirstItem"]["X"], config["FirstItem"]["Y"])  # sell button
        time.sleep(0.015)
        click(config["SelectButton"]["X"], config["SelectButton"]["Y"])  # first item
        time.sleep(0.02)
        click(config["EnterPrice"]["X"], config["EnterPrice"]["Y"])  # select button
        time.sleep(0.022)
        click(1600, 625)  # enter price
        time.sleep(0.1)
        keyboard.write(price, delay=0.01)
        keyboard.send("enter")
        time.sleep(0.01)
        click(1400, 900)  # create listing button
        time.sleep(config["WaitTime"])  # wait some time

    def process_image():
        global n_frames, t0
        img = sct.grab(monitor=config["Monitor"])
        img = np.array(img)  # Convert to NumPy array
        # small = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
        # cv.imshow("Computer Vision", small)

        # Convert the PIL image to grayscale for better OCR accuracy
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(Image.fromarray(gray_img), lang='rus')
        print(text)
        if recognize_text in text:
            pattern = rf"{recognize_text} (\d+\.\d+)"
            match = re.search(pattern, text)
            if match:
                number = float(match.group(1))
                if number > config["MinPrice"]:
                    print("Float Number:", number)
                    sell(str(number))
                    remove(config["RefreshButton"]["X"], config["RefreshButton"]["Y"])
            else:
                print("No match found.")

        key = cv.waitKey(1)
        if key == ord('q'):
            return False

        return True

    img = None

    with mss.mss() as sct:
        while process_image():
            pass
