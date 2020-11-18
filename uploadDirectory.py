import os
import boto3
import time
import threading
from boto3.s3.transfer import TransferConfig

start_time = time.time()
S3_BUCKET = ""
DIR_PATH = r""
ACCESS_ID = "" 
ACCESS_KEY=""
maxThreads = 100
sema = threading.Semaphore(value=maxThreads)

config = TransferConfig(use_threads=False)

s3_client = boto3.client('s3',
   aws_access_key_id=ACCESS_ID,
   aws_secret_access_key= ACCESS_KEY)

rootFolder = os.path.basename(os.path.normpath(DIR_PATH))

'''
    https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
    
    This will give the list of all the files I need to upload. S3 effectively
    has a flat file structure (folders are just files with 'folder/' prepended to them) and I can simply
    upload them using the file path to access the file and a modified version of the filepath to create the
    object key.
'''

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

def uploadFiles(files):
    threads = list()
    for file in files:
        thread = threading.Thread(target = uploadFileS3, args=(file,))
        threads.append(thread)
        thread.start()

'''
    Documentation:
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
'''

def uploadFileS3(filePath):
    sema.acquire()
    objectKey = rootFolder + filePath[len(filePath) - (len(filePath)-len(DIR_PATH)):].replace('\\', '/')
    s3_client.upload_file(filePath, S3_BUCKET, objectKey, Config = config)
    sema.release()

    
files = getListOfFiles(DIR_PATH)
uploadFiles(files)
print("--- %s seconds ---" % (time.time() - start_time))