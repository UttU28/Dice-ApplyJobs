from utils.azure_blob_utils import downloadBlobFromAzure
import os, json, re
import shutil


def deleteDir(whichDir):
    thisDir = "assets/" + whichDir
    if os.path.exists(thisDir):
        try:
            shutil.rmtree(thisDir)
            print(f"Directory '{thisDir}' and all its contents have been deleted.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Directory '{thisDir}' does not exist.")

def deleteFile(whichFile, whichDir):
    thisFile = "assets/" + whichDir + whichFile
    if os.path.isfile(thisFile):
        try:
            os.remove(thisFile)
            print(f"File '{thisFile}' has been deleted.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"File '{thisFile}' does not exist.")

def getCurrentStructure():
    cwd = os.getcwd()+"/assets/"
    currentStructure = {}

    for item in os.listdir(cwd):
        resumePath = os.path.join(cwd, item)
        if os.path.isdir(resumePath):
            file_names = [f for f in os.listdir(resumePath) if os.path.isfile(os.path.join(resumePath, f))]
            currentStructure[item] = file_names

    return currentStructure


def convertToDir(email):
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

def dirBanaoBC(konsa):
    konsa = "assets/"+konsa
    if not os.path.exists(konsa):
        os.makedirs(konsa)
        print(f"Directory '{konsa}' created.")
    else:
        print(f"Directory '{konsa}' already exists.")

def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def findDifferences(new_data, old_data):
    new_keys = set(new_data.keys())
    old_keys = set(old_data.keys())
    
    added_keys = new_keys - old_keys
    removed_keys = old_keys - new_keys

    common_keys = new_keys & old_keys
    added_values = {}
    removed_values = {}

    for key in common_keys:
        new_values = set(map(tuple, new_data[key]))
        old_values = set(map(tuple, old_data[key]))

        added_items = new_values - old_values
        removed_items = old_values - new_values

        if added_items:
            added_values[key] = list(map(list, added_items))
        if removed_items:
            removed_values[key] = list(map(list, removed_items))

    return added_keys, removed_keys, added_values, removed_values

def compareBoth(newStructure):
    newResumeStructure = {convertToDir(key): value for key, value in newStructure.items()}
    currentResumeStructure = read_json('thisResumeManager.json')
    added_keys, removed_keys, added_values, removed_values = findDifferences(newResumeStructure, currentResumeStructure)

    print("\nNew keys and values:")
    for key in added_keys:
        dirBanaoBC(key)
        for eachData in newResumeStructure[key]:
            resumeID, resumeName = eachData[0], eachData[1]
            downloadBlobFromAzure(resumeID, key, resumeName)
        print(f"New value: {newResumeStructure[key]}")
            
    print("\nDeleted keys and values:")
    for key in removed_keys:
        deleteDir(key)
        print(f"Deleted key: {key}")

    print("\nAdded values:")
    for key, values in added_values.items():
        print(f"Key: {key}")
        for value in values:
            resumeID, resumeName = value[0], value[1]
            downloadBlobFromAzure(resumeID, key, resumeName)
            print(f"Added value: {value}")

    print("\nRemoved values:")
    for key, values in removed_values.items():
        print(f"Key: {key}")
        for value in values:
            resumeID, resumeName = value[0], value[1]
            deleteFile(resumeName, key)
            print(f"Removed value: {value}")

    # Save the modified dictionary to a JSON file
    with open('thisResumeManager.json', 'w') as json_file:
        json.dump(newResumeStructure, json_file, indent=4)

    print("Data has been saved to 'thisResumeManager.json'.")


def getResumeName(resumeNumber):
    with open('thisResumeManager.json', 'r') as file:
        data = json.load(file)
    
    for email, resumes in data.items():
        for resume in resumes:
            if resume[0] == resumeNumber:
                return resume[1], email
