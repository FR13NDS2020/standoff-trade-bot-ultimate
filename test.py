import time
import mss
import pyautogui
from multiprocessing import Pool

def check_pixel_color_pyautogui(x, y, r, g, b, t):
    return pyautogui.pixelMatchesColor(x, y, (r, g, b), tolerance=t)

def check_pixel_color_mss(x, y, r, g, b, t):
    tolerance = t

    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        sct_img = sct.grab(monitor)
        pixel = sct_img.pixel(0, 0)

    captured_r, captured_g, captured_b = pixel[:3]

    if (
        r - tolerance <= captured_r <= r + tolerance and
        g - tolerance <= captured_g <= g + tolerance and
        b - tolerance <= captured_b <= b + tolerance
    ):
        return captured_r, captured_g, captured_b

    return None

def execute_function(args):
    function, arg_values, duration = args
    count = 0
    start_time = time.perf_counter()

    while time.perf_counter() - start_time < duration:
        function(*arg_values)
        count += 1

    return count

def test_function_time(function, *args):
    arg_values = [args] * 4
    duration = 10  # Time in seconds
    pool = Pool(processes=4)  # Number of processes to use

    results = pool.map(execute_function, zip([function] * 4, arg_values, [duration] * 4))
    pool.close()
    pool.join()

    total_count = sum(results)
    elapsed_time = duration

    return total_count, elapsed_time

if __name__ == '__main__':
    # Test the execution time for check_pixel_color_pyautogui
    x = 100
    y = 200
    r = 255
    g = 0
    b = 0
    tolerance = 10

    count, elapsed_time = test_function_time(check_pixel_color_pyautogui, x, y, r, g, b, tolerance)
    print("check_pixel_color_pyautogui executed", count, "times in", elapsed_time, "seconds")

    # Test the execution time for check_pixel_color_mss
    x = 100
    y = 200
    r = 255
    g = 0
    b = 0
    tolerance = 10

    count, elapsed_time = test_function_time(check_pixel_color_mss, x, y, r, g, b, tolerance)
    print("check_pixel_color_mss executed", count, "times in", elapsed_time, "seconds")
