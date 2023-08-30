import concurrent.futures
import concurrent.futures
import statistics
import time
import json
import dearpygui.dearpygui as dpg
import keyboard
import pyautogui
import win32api
import win32con
import winsound
import pyglet
from debug import debug_all

with open("refresh_buy.json", "r") as f:
    data = json.load(f)

confirmx = data["confirmx"]
confirmy = data["confirmy"]

with open("data.json", "r") as f:
    pixel_data = json.load(f)


def play_notification_sound():
    sound = pyglet.media.load("sound.mp3")
    player = pyglet.media.Player()
    player.queue(sound)
    player.play()

    def exit_callback(dt):
        pyglet.app.exit()

    pyglet.clock.schedule_once(exit_callback, sound.duration)
    pyglet.app.run()


with open("refresh_buy.json", "r") as f:
    data = json.load(f)
    refreshx = data["refreshx"]
    refreshy = data["refreshy"]
    buyx = data["buyx"]


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def refresh():
    click(refreshx, refreshy)
    time.sleep(0.1)
    click(refreshx, refreshy)


def buy(y):
    click(buyx, y)
    time.sleep(0.025)
    click(confirmx, confirmy)
    click(confirmx, confirmy)
    time.sleep(1)
    debug_all()
    time.sleep(3)


def check_pixel_color(pixel_data, test_mode, mode=1):
    cell_info = pixel_data[f"Cell {mode}"]
    x, y = cell_info["X"], cell_info["Y"]
    r, g, b = cell_info["R"], cell_info["G"], cell_info["B"]
    tolerance = cell_info["tolerance"]
    if not pyautogui.pixelMatchesColor(x, y, (r, g, b), tolerance=tolerance):
        if test_mode:
            print(f"buy {x}, {y} rgb: {r},{g},{b}")
            time.sleep(0.7)
        else:
            buy(y)
            print(f"buy {y}")
            time.sleep(1)
            refresh()


def get_pixels_json(data, sticker=1, test_mode=True):
    print("start catching stickers")
    for i in range(5):
        time.sleep(1)
        print(i)
    counter = 0
    while not keyboard.is_pressed("q"):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for pixel_data in data:
                futures.append(executor.submit(check_pixel_color, pixel_data, test_mode, mode=sticker))

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                counter += 1

        if counter >= 280 and not test_mode:
            counter = 0
            refresh()
    print("quited stickers")


def calculate_tolerance(r_values, g_values, b_values):
    minr = min(r_values)
    maxr = max(r_values)

    ming = min(g_values)
    maxg = max(g_values)

    minb = max(b_values)
    maxb = max(b_values)

    temp1 = abs(minr - maxr)
    temp2 = abs(ming - maxg)
    temp3 = abs(minb - maxb)

    max_difference = max(temp1, temp2, temp3)

    return max_difference + 2


def calculate_middle_color(c1, c2):
    middle_color = (c1 + c2) // 2
    return middle_color


def colors(x, y, duration):
    pixels = []
    start_time = time.time()
    while time.time() - start_time < duration:
        pixels.append(pyautogui.pixel(x, y))

    # Extract the R, G, B values from each pixel tuple
    r_values, g_values, b_values = zip(*pixels)
    cords = [x, y]

    # Calculate the middle color for each RGB component
    middle_r = calculate_middle_color(min(r_values), max(r_values))
    middle_g = calculate_middle_color(min(g_values), max(g_values))
    middle_b = calculate_middle_color(min(b_values), max(b_values))
    avg_color = (middle_r, middle_g, middle_b)

    # Calculate the tolerance based on the RGB values
    tolerance = calculate_tolerance(r_values, g_values, b_values)

    return cords, avg_color, tolerance


def collect_rgb_values(cords, duration):
    collected = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(colors, x, y, duration) for x, y in cords]
        for future in concurrent.futures.as_completed(futures):
            avg = future.result()
            collected.append(avg)

    return collected


def coordinate_calculator(x1, x2, y1, y2, n):
    print("calculate")
    multiplier = (y2 - y1) / (n - 1)
    multiplier2 = (x1 - x2) / 2
    print(multiplier)
    for i, y in enumerate(range(y1, y2 + 1, int(multiplier))):
        for j, x in enumerate([x1 - (k * multiplier2) for k in range(3)]):
            dpg.set_value(f"X#{i}{j}", int(x))
            dpg.set_value(f"Y#{i}{j}", int(y))
            # set in setup
            dpg.set_value(f"X##{i}{j}", int(x))
            dpg.set_value(f"Y##{i}{j}", int(y))


def save_recognize():
    print("save data to recognize.json")
    sell_x = dpg.get_value("SellButton_X")
    sell_y = dpg.get_value("SellButton_Y")
    first_item_x = dpg.get_value("FirstItem_X")
    first_item_y = dpg.get_value("FirstItem_Y")
    select_x = dpg.get_value("SelectButton_X")
    select_y = dpg.get_value("SelectButton_Y")
    enter_price_x = dpg.get_value("EnterPrice_X")
    enter_price_y = dpg.get_value("EnterPrice_Y")
    create_listing_x = dpg.get_value("CreateListing_X")
    create_listing_y = dpg.get_value("CreateListing_Y")
    wait_time = dpg.get_value("WaitTime")

    monitor_top = dpg.get_value("top")
    monitor_left = dpg.get_value("left")
    monitor_width = dpg.get_value("width")
    monitor_height = dpg.get_value("height")

    refreshx = dpg.get_value("refresh_x")
    refreshy = dpg.get_value("refresh_y")

    min_price = dpg.get_value("Min_price")


    data = {
        "SellButton": {"X": sell_x, "Y": sell_y},
        "FirstItem": {"X": first_item_x, "Y": first_item_y},
        "SelectButton": {"X": select_x, "Y": select_y},
        "EnterPrice": {"X": enter_price_x, "Y": enter_price_y},
        "CreateListingButton": {"X": create_listing_x, "Y": create_listing_y},
        "WaitTime": wait_time,
        "RefreshButton": {"X": refreshx, "Y": refreshy},
        "MinPrice": min_price,
        "Text": "продажу за",
        "Monitor": {"top": monitor_top,
                    "left": monitor_left,
                    "width": monitor_width,
                    "height": monitor_height
                    }
    }

    # Now you can save the data dictionary to the recognize.json file using the json module
    with open("recognize.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_data(row_count):
    print("save data")
    data = []
    for i in range(row_count):
        row_data = {}
        for j in range(3):
            cell_data = {}
            x_value = dpg.get_value(f"X##{i}{j}")
            cell_data["X"] = x_value

            y_value = dpg.get_value(f"Y##{i}{j}")
            cell_data["Y"] = y_value

            r_value = dpg.get_value(f"R##{i}{j}")
            cell_data["R"] = r_value

            g_value = dpg.get_value(f"G##{i}{j}")
            cell_data["G"] = g_value

            b_value = dpg.get_value(f"B##{i}{j}")
            cell_data["B"] = b_value

            tolerance_value = dpg.get_value(f"tolerance##{i}{j}")
            cell_data["tolerance"] = tolerance_value

            row_data[f"Cell {j + 1}"] = cell_data
        data.append(row_data)

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


def save_refresh_buy(sender, app_data):
    print("save refresh_buy")
    refreshx = dpg.get_value("refresh x")
    refreshy = dpg.get_value("refresh y")
    buyx = dpg.get_value("buy x")

    confirmy = dpg.get_value("confirm y")
    confirmx = dpg.get_value("confirm x")

    data = {
        "refreshx": refreshx,
        "refreshy": refreshy,
        "buyx": buyx,
        "confirmy": confirmy,
        "confirmx": confirmx,

    }

    with open("refresh_buy.json", "w") as f:
        json.dump(data, f, indent=2)


def load_data(sender, app_data):
    print("load data")
    with open("data.json", "r") as f:
        data = json.load(f)

    for i, row_data in enumerate(data):
        for j, cell_data in enumerate(row_data.values()):
            dpg.set_value(f"X##{i}{j}", cell_data["X"])
            dpg.set_value(f"Y##{i}{j}", cell_data["Y"])
            dpg.set_value(f"R##{i}{j}", cell_data["R"])
            dpg.set_value(f"G##{i}{j}", cell_data["G"])
            dpg.set_value(f"B##{i}{j}", cell_data["B"])
            # for configure colors table
            dpg.set_value(f"X#{i}{j}", cell_data["X"])
            dpg.set_value(f"Y#{i}{j}", cell_data["Y"])
            dpg.set_value(f"tolerance##{i}{j}", cell_data["tolerance"])

    with open("refresh_buy.json", "r") as f:
        data = json.load(f)
    dpg.set_value("buy x", data["buyx"])
    dpg.set_value("refresh x", data["refreshx"])
    dpg.set_value("refresh y", data["refreshy"])

    dpg.set_value("confirm x", data["confirmx"])
    dpg.set_value("confirm y", data["confirmy"])


def load_recognize():
    try:
        with open("recognize.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Update the UI elements with the loaded data
        dpg.set_value("SellButton_X", data["SellButton"]["X"])
        dpg.set_value("SellButton_Y", data["SellButton"]["Y"])

        dpg.set_value("FirstItem_X", data["FirstItem"]["X"])
        dpg.set_value("FirstItem_Y", data["FirstItem"]["Y"])

        dpg.set_value("SelectButton_X", data["SelectButton"]["X"])
        dpg.set_value("SelectButton_Y", data["SelectButton"]["Y"])

        dpg.set_value("EnterPrice_X", data["EnterPrice"]["X"])
        dpg.set_value("EnterPrice_Y", data["EnterPrice"]["Y"])

        dpg.set_value("CreateListing_X", data["CreateListingButton"]["X"])
        dpg.set_value("CreateListing_Y", data["CreateListingButton"]["Y"])

        dpg.set_value("WaitTime", data["WaitTime"])

        dpg.set_value("top", data["Monitor"]["top"])
        dpg.set_value("left", data["Monitor"]["left"])
        dpg.set_value("width", data["Monitor"]["width"])
        dpg.set_value("height", data["Monitor"]["height"])

        dpg.set_value("refresh_x", data["RefreshButton"]["X"])
        dpg.set_value("refresh_y", data["RefreshButton"]["Y"])

        dpg.set_value("Min_price", data["MinPrice"])

    except FileNotFoundError:
        print("recognize.json not found. No data loaded.")
    except KeyError:
        print("Error: Missing or incorrect keys in recognize.json. No data loaded.")
    except json.JSONDecodeError:
        print("Error: Unable to parse recognize.json. No data loaded.")


def configure_colors(row_count, duration=10):
    print("start configuring colors wait 10 seconds...")
    time.sleep(10)
    cords = []
    for i in range(row_count):
        for j in range(3):
            x_value = dpg.get_value(f"X#{i}{j}")
            y_value = dpg.get_value(f"Y#{i}{j}")
            cords.append((x_value, y_value))

    collected_rgb = collect_rgb_values(cords, duration)
    winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)

    for i in range(row_count):
        for j in range(3):
            index = i * 3 + j  # Calculate the corresponding index in the collected_rgb list
            r, g, b = collected_rgb[index][1]
            dpg.set_value(f"R##{i}{j}", r)
            dpg.set_value(f"G##{i}{j}", g)
            dpg.set_value(f"B##{i}{j}", b)

            max_scatter = collected_rgb[index][2]
            # tolerance = max(max_scatter)  # Use the maximum scatter as tolerance
            dpg.set_value(f"tolerance##{i}{j}", max_scatter)

    play_notification_sound()
