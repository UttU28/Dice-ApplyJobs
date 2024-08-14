import os, re, json, subprocess
from time import sleep
from utils.selenium_utils import *
from utils.database_utils import *
from config.config import CHROME_DRIVER_PATH, CHROME_OPTIONS
import pyautogui


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
    email = re.sub(r'[<>:"/\\|?*]', '_', email)
    return email

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
    driver = initialize_chrome_driver(CHROME_DRIVER_PATH, CHROME_OPTIONS)
    chrome_app = subprocess.Popen([
        'C:/Program Files/Google/Chrome/Application/chrome.exe',
        '--remote-debugging-port=9002',
        f'--user-data-dir=C:/Users/utsav/Desktop/Dice-ApplyJobs/chromeProfiles/{getDirName(ofThis)}',
        '--start-maximized'  # Add this argument to start Chrome in maximized mode
    ])
    sleep(4)
    for j in range(3):
        pyautogui.press('tab')
        sleep(0.5)
    pyautogui.press('enter')
    pyautogui.typewrite('https://www.dice.com/')
    sleep(1)
    pyautogui.press('enter')
    sleep(2)
    driver.get('https://www.dice.com/dashboard/login')
    driver.find_element(By.CL)
    chrome_app.terminate()
    

def checkIfChromeProfile(ofThis):
    if not os.path.isdir("chromeProfiles/"+getDirName(ofThis)):
        chrome_app = subprocess.Popen([
            'C:/Program Files/Google/Chrome/Application/chrome.exe',
            '--remote-debugging-port=9002',
            f'--user-data-dir=C:/Users/utsav/Desktop/Dice-ApplyJobs/chromeProfiles/{getDirName(ofThis)}',
            '--start-maximized'  # Add this argument to start Chrome in maximized mode
        ])
        sleep(4)
        pyautogui.press('tab')
        sleep(0.5)
        pyautogui.press('enter')
        sleep(2)


        
        chrome_app.terminate()
        