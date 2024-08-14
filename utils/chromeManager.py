import os
import re
import subprocess
from time import sleep
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils.selenium_utils import initialize_chrome_driver
from utils.database_utils import *  # Assuming this is where database functions are imported
from config.config import CHROME_DRIVER_PATH, CHROME_OPTIONS

def getDirName(email):
    replacements = {
        '@': '_at_',
        '.': '_dot_',
        ':': '_colon_',
        '/': '_slash_',
        '\\': '_backslash_',
        '?': '_question_',
        '*': '_asterisk_',
        '|': '_pipe_'
    }
    for old, new in replacements.items():
        email = email.replace(old, new)
    return re.sub(r'[<>:"/\\|?*]', '_', email)

def cleanTheDamnJobQueue(onThisData):
    result = {}
    for eachApply in onThisData:
        email = eachApply['email']
        job_id = eachApply['id']
        resume = eachApply['selectedResume']
        if email not in result:
            checkIfChromeProfile(email)
            result[email] = []
        result[email].append([job_id, resume])
    return result

def createProfile(ofThis):
    profile_path = f'C:/Users/utsav/Desktop/Dice-ApplyJobs/chromeProfiles/{getDirName(ofThis)}'
    driver = initialize_chrome_driver(CHROME_DRIVER_PATH, CHROME_OPTIONS)

    chrome_app = subprocess.Popen([
        'C:/Program Files/Google/Chrome/Application/chrome.exe',
        '--remote-debugging-port=9002',
        f'--user-data-dir={profile_path}',
        '--start-maximized'
    ])
    sleep(4)

    pyautogui.press('tab')
    sleep(0.5)
    pyautogui.press('enter')
    pyautogui.typewrite('https://www.dice.com/')
    sleep(1)
    pyautogui.press('enter')
    sleep(2)

    driver.get('https://www.dice.com/dashboard/login')
    sleep(2)

    dicePassword = fetchDiceCreds(ofThis)

    email_element = driver.find_element_by_xpath('//div[@data-testid="email-input"]')
    email_element.send_keys(ofThis)
    password_element = driver.find_element_by_xpath('//div[@data-testid="password-input"]')
    password_element.send_keys(dicePassword)
    password_element.send_keys(Keys.RETURN)

    sleep(5)

    chrome_app.terminate()

def checkIfChromeProfile(ofThis):
    profile_path = f"chromeProfiles/{getDirName(ofThis)}"
    if not os.path.isdir(profile_path):
        thisChromeApp = subprocess.Popen([
            'C:/Program Files/Google/Chrome/Application/chrome.exe',
            '--remote-debugging-port=9002',
            f'--user-data-dir={profile_path}',
            '--start-maximized'
        ])
        sleep(4)

        pyautogui.press('tab')
        sleep(0.5)
        pyautogui.press('enter')
        sleep(2)

        thisChromeApp.terminate()

    createProfile(ofThis)
