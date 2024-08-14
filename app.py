# main.py

import subprocess
import time
from datetime import datetime, timedelta
import schedule
import logging
from config.config import CHROME_DRIVER_PATH, CHROME_OPTIONS
from utils.resumeManager import *
from utils.chromeManager import *
from utils.database_utils import *
from utils.selenium_utils import *
from config.logging_config import *
import pyautogui
from time import sleep

# Set up logging
logger = setup_logging()

def apply_the_jobs():
    conn = connect_to_database()
    
    jobQueue = fetch_the_queue(conn)
    resumeData = fetch_resume_list(conn)
    cleanedJobQueue = cleanTheDamnJobQueue(jobQueue)
    compareBoth(resumeData)
    thisCounter = 0

    for userEmail, userApplyQueue in cleanedJobQueue.items():
        if userApplyQueue:
            chrome_app = subprocess.Popen([
                'C:/Program Files/Google/Chrome/Application/chrome.exe',
                '--remote-debugging-port=9002',
                f'--user-data-dir=C:/Users/utsav/Desktop/Dice-ApplyJobs/chromeProfiles/{getDirName(userEmail)}',
                '--start-maximized'  # Add this argument to start Chrome in maximized mode
            ])
            time.sleep(2)

            driver = initialize_chrome_driver(CHROME_DRIVER_PATH, CHROME_OPTIONS)
            
            for job in userApplyQueue:
                print(job)
                jobID = job[0]
                selectedResume = job[1]
                # print(jobID, selectedResume)
                resumeName, userDir = getResumeName(selectedResume)
                try:
                    apply_status = apply_dice(jobID, resumeName, userDir, driver)
                    if apply_status == 'applied': thisCounter += 1
                except Exception as e:
                    logging.error(f"Error applying for job {userEmail} - {jobID}: {e}")
                    apply_status = 'error'
                finally:
                    remove_from_queue(conn, jobID)
                    # update_the_job(conn, jobID, apply_status)
            
            chrome_app.terminate()
            driver.quit()
    
    timeForNext = datetime.now() + timedelta(minutes=10)
    print(f"--------- {thisCounter} JOBS APPLIED")
    print(f"--------- ENDED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"--------- NEXT AT  {timeForNext.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*40)

    prevScore = fetchTheScore(conn)
    if thisCounter != 0: setTheScore(conn, thisCounter + prevScore)
    
    logging.info(f"--------- {thisCounter} + {prevScore} JOBS APPLIED")
    logging.info(f"--------- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ||||| {timeForNext.strftime('%Y-%m-%d %H:%M:%S')}")
    conn.close()

def apply_dice(jobID, selectedResume, userDir, thisDriver):
    if thisDriver is None:
        logging.critical("CHROME KE MAA CHUD GAI BHAIIIIIIII")
        raise ValueError("Driver is not initialized. Call loadChrome() first.")
    
    thisDriver.get(f"https://www.dice.com/job-detail/{jobID}")
    sleep(5)
    try:
        clickTheDamnButton('apply', 2)
        clickTheDamnButton('replaceResume', 2)

        pyautogui.click()
        sleep(0.8)
        pyautogui.hotkey('ctrl', 'l')
        sleep(0.8)
        pyautogui.typewrite(f'C:/Users/utsav/OneDrive/Desktop/Dice-ApplyJobs/assets/{userDir}/{selectedResume}')
        sleep(0.8)
        pyautogui.press('enter')
        sleep(0.8)
        for i in range(6):
            pyautogui.press('tab')
            sleep(0.2)
        sleep(0.5)
        pyautogui.typewrite(selectedResume)
        sleep(0.5)
        pyautogui.press('enter')
        sleep(1)

        screen_width, screen_height = pyautogui.size()
        region = (screen_width // 2, 0, screen_width, screen_height)
        pyautogui.click(screen_width//2, screen_height//2)
        sleep(0.2)
        pyautogui.press(['tab'] * 3)
        pyautogui.press('enter')
        sleep(3.5)
        clickTheDamnButton('next', 1)
        location = pyautogui.locateOnScreen('images/submit.png', region=region, confidence=0.8)
        pyautogui.click(location)
        sleep(2)
        return 'applied'

    except Exception as e:
        logging.error(f"Apply Button not FOUND for {jobID}")
        print(f"Error clicking 'Easy apply' button: {e}")
        return 'error'
    


if __name__ == "__main__":
    # Example of downloading blob from Azure
    # downloadBlobFromAzure(
    #     '1723368698677257989',
    #     'assets/sdv.pdf'
    # )
    # print(2)
    apply_the_jobs()
    # schedule.every(15).minutes.do(apply_the_jobs)
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

