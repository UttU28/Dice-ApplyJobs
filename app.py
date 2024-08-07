import subprocess
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import pypyodbc as odbc
from datetime import datetime, timezone, timedelta
import schedule
import logging
import sys


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')


server = 'dice-sql.database.windows.net'
database = 'dice_sql_database'
username = 'iAmRoot'
password = 'Qwerty@213'

connectionString = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

def applyTheJobs():
    def fetchTheQueue(conn):
        cursor = conn.cursor()
        query = """
            SELECT id, selectedResume, timeOfArrival 
            FROM applyQueue 
            ORDER BY timeOfArrival ASC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        jobQueue = []
        for row in rows:
            data_dict = {'id': row[0],'selectedResume': row[1],'timeOfArrival': str(row[2])}
            jobQueue.append(data_dict)
        cursor.close()
        if jobQueue: return jobQueue
        else: return False

    def removeFromQueue(conn, jobID):
        cursor = conn.cursor()
        query = f"DELETE FROM applyQueue WHERE id = '{jobID}'"
        cursor.execute(query)
        conn.commit()
        print("Job Removed from Apply Queue")
        cursor.close()

    def updateTheJob(conn, jobID, applyStatus):
        cursor = conn.cursor()
        timestamp = int(datetime.now(timezone.utc).timestamp())
        query = f"""
            UPDATE allData
            SET myStatus = '{applyStatus}', decisionTime = {timestamp}
            WHERE id = '{jobID}';
        """
        cursor.execute(query)
        conn.commit()
        cursor.close()

    def fetchResumeList(conn):
        try:
            cursor = conn.cursor()
            query = """SELECT * FROM resumeList"""
            cursor.execute(query)
            rows = cursor.fetchall()
            resumeData = {row[0]: row[1] for row in rows}
            cursor.close()
            return resumeData
        except: logging.critical('RESUME NOT FOUND')

    def fetchTheScore(conn):
        try:
            cursor = conn.cursor()
            query = """SELECT score FROM scoreBoard where contender = 'theMachine';"""
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            if (not result) or (type(result[0][0]) != int): result = 0
            else: result = result[0][0]
            conn.commit()
            cursor.close()
            return result
        except: logging.critical('SCORE NOT FOUND for theMachine')

    def setTheScore(conn, newScore):
        # try:
            cursor = conn.cursor()
            query = f"""
                UPDATE scoreBoard 
                SET score = {newScore} 
                WHERE contender = 'theMachine';
            """
            cursor.execute(query)
            print(newScore, 'newScore')
            conn.commit()
            cursor.close()
            logging.info("Score Setteled on the ScoreBoard for theMachine")
        # except: logging.critical('SCORE NOT SETTELED for theMachine')

    def clickTheDamnButton(imageName, sleepTime, max_search_time=10, search_interval=2):
        start_time = time.time()
        screen_width, screen_height = pyautogui.size()
        region = (0, 0, screen_width, screen_height)
        
        while time.time() - start_time < max_search_time:
            location = pyautogui.locateOnScreen(f'images/{imageName}.png', region=region, confidence=0.8)  # Adjust confidence as needed
            if location is not None:
                center = pyautogui.center(location)
                pyautogui.moveTo(center)
                pyautogui.click()
                sleep(sleepTime)
                return True  # Return True when the button is clicked successfully
            else:
                print(f"Still haven't found {imageName}.png...")
                sleep(search_interval)

        logging.error(f"{imageName}.png not found within the time limit.")
        return False  # Return False if the image was not found within the time limit

    def applyDice(conn, jobID, selectedResume, thisDriver):
        print(jobID, selectedResume)
        if thisDriver is None:
            logging.critical("CHROME KE MAA CHUD GAI BHAIIIIIIII")
            raise ValueError("Driver is not initialized. Call loadChrome() first.")
        
        thisDriver.get(f"https://www.dice.com/job-detail/{jobID}")
        sleep(7)
        try:
            clickTheDamnButton('apply', 2)
            clickTheDamnButton('replaceResume', 2)

            pyautogui.click()
            sleep(0.8)
            pyautogui.hotkey('ctrl', 'l')
            sleep(0.8)
            pyautogui.typewrite('C:/Users/utsav/OneDrive/Desktop/Dice-Saral-Apply/allResume')
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
        

    conn = odbc.connect(connectionString)
    thisCounter = 0
    jobQueue = fetchTheQueue(conn)
    resumeData = fetchResumeList(conn)

    
    # print(jobQueue)
    if jobQueue:
        chrome_driver_path = 'C:/chromeDriver/chromedriver.exe'  # Ensure the path is correct
        chromeApp = subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe', '--remote-debugging-port=9002', '--user-data-dir=C:/chromeDriver/diceApply/'])
        sleep(2)
        options = Options()
        options.add_experimental_option("debuggerAddress", "localhost:9002")
        options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
        options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=options)

        for thisJob in jobQueue:
            jobID = thisJob['id']
            selectedResume = resumeData.get(thisJob['selectedResume'])
            try:
                applyStatus = applyDice(conn, jobID, selectedResume, driver)
                thisCounter += 1
            except:
                applyStatus = 'error'
            removeFromQueue(conn, jobID)
            # updateTheJob(conn, jobID, applyStatus)
        chromeApp.terminate()

    timeForNext = datetime.now() + timedelta(minutes = 10)
    print(f"--------- {thisCounter} JOBS APPLIED")
    print(f"--------- ENDED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"--------- NEXT AT  {timeForNext.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*40)

    prevScore = fetchTheScore(conn)
    if thisCounter != 0: setTheScore(conn, thisCounter + prevScore)
    
    logging.info(f"--------- {thisCounter} + {prevScore} JOBS APPLIED")
    logging.info(f"--------- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ||||| {timeForNext.strftime('%Y-%m-%d %H:%M:%S')}")
    conn.close()


if __name__ == "__main__":
    applyTheJobs()
    schedule.every(15).minutes.do(applyTheJobs)

    while True:
        schedule.run_pending()
        sleep(1)
