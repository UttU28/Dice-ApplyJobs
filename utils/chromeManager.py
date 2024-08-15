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

from utils.selenium_utils import *
from utils.database_utils import *  # Assuming this is where database functions are imported
from config.config import CHROME_DRIVER_PATH, CHROME_OPTIONS

profileRootDir = "C:/Users/utsav/Desktop/Dice-ApplyJobs/chromeProfiles/"

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

def checkAndLoginToDice(email, thisDriver):
    profileChecking = "https://www.dice.com/dashboard/login?redirectURL=/dashboard/profiles" 
    sleep(1)
    thisDriver.get(profileChecking)
    sleep(2)
    thisDriver.get(profileChecking)
    
    for i in range(3):
        pyautogui.press('esc')
        sleep(0.2)
    sleep(1)
    # thisDriver.execute_script("document.body.style.zoom='75%';")
    print(thisDriver.current_url)
    if thisDriver.current_url == profileChecking:
        # Initialize User Login
        sleep(2)
        dicePassword = fetchDiceCreds(email)
        pyautogui.typewrite(email)
        sleep(0.5)
        pyautogui.press('enter')
        sleep(2)
        pyautogui.typewrite(dicePassword)
        sleep(0.5)
        pyautogui.press('enter')
        sleep(1)
        # clickTheDamnButton('savePassword', 2)
        sleep(1)
        thisDriver.get("https://www.dice.com/dashboard/jobs")
        sleep(2)
        thisDriver.get("https://www.dice.com/jobs")
    sleep(2)
    thisDriver.get('chrome://settings/')
    thisDriver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.75);')

def startChromeProcess(ofThis):
    profile_path = f'{profileRootDir}/{getDirName(ofThis)}'
    chromeApp = subprocess.Popen([
        'C:/Program Files/Google/Chrome/Application/chrome.exe',
        '--remote-debugging-port=9002',
        f'--user-data-dir={profile_path}',
        '--start-maximized'
    ])
    return chromeApp

def killChromeProcess(chromeApp):
    try:
        chromeApp.terminate()
        chromeApp.wait()
        if chromeApp.poll() is None:  # Process is still running
            chromeApp.kill()
        chromeApp.wait()
    except:
        pass


def addDiceProfileToChrome(ofThis):
    chromeApp = startChromeProcess(ofThis)
    sleep(2)
    loginDriver = initialize_chrome_driver(CHROME_DRIVER_PATH, CHROME_OPTIONS)
    sleep(4)

    for _ in range(3):
        pyautogui.press('tab')
        sleep(0.5)
    pyautogui.press('enter')
    sleep(0.5)
    pyautogui.typewrite('https://www.dice.com/')
    sleep(1)
    pyautogui.press('enter')
    sleep(2)

    checkAndLoginToDice(ofThis, loginDriver)

    killChromeProcess(chromeApp)
    loginDriver.quit()

def checkIfChromeProfile(ofThis):
    profile_path = f"{profileRootDir}/{getDirName(ofThis)}"
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

        addDiceProfileToChrome(ofThis)
