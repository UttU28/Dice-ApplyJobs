# utils/selenium_utils.py

import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging

def initialize_chrome_driver(chrome_driver_path, chrome_options):
    options = Options()
    options.add_experimental_option("debuggerAddress", chrome_options['debugger_address'])
    options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
    options.add_argument("--disable-notifications")
    return webdriver.Chrome(options=options)

def clickTheDamnButton(image_name, sleep_time, max_search_time=10, search_interval=2):
    start_time = time.time()
    screen_width, screen_height = pyautogui.size()
    region = (0, 0, screen_width, screen_height)
    
    while time.time() - start_time < max_search_time:
        location = pyautogui.locateOnScreen(f'images/{image_name}.png', region=region, confidence=0.8)
        if location is not None:
            center = pyautogui.center(location)
            pyautogui.moveTo(center)
            time.sleep(sleep_time)
            pyautogui.click()
            return True
        else:
            print(f"Still haven't found {image_name}.png...")
            time.sleep(search_interval)

    logging.error(f"{image_name}.png not found within the time limit.")
    return False
