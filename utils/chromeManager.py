import os, re, json, subprocess
from time import sleep

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
        email = getDirName(eachApply['email'])
        job_id = eachApply['id']
        resume = eachApply['selectedResume']
        if email not in result:
            checkIfChromeProfile(email)
            result[email] = []
        result[email].append([job_id, resume])
    return result

def checkIfChromeProfile(ofThis):
    if not os.path.isdir("chromeProfiles/"+ofThis):
        print("creatingThis")
        # chrome_app = subprocess.Popen([
        #         f'C:/Program Files/Google/Chrome/Application/chrome.exe',
        #         f'--remote-debugging-port=9002',
        #         f'--user-data-dir=C:/Users/iandm/Desktop/Dice-ApplyJobs/chromeProfiles/{ofThis}'
        #     ])
        # sleep(10)
        # chrome_app.terminate()