#!/usr/bin/python
from time import gmtime, strftime, sleep

# Return base64 encoded file
def fileToBase64():
    return ""

'''
Post request to http://127.0.0.1:8000/api/replays/
Raw content example:
    {
        "title": "prueba1",
        "base64_file": "fdfsf",
        "extra": "fdf"
    }
'''
def sendReplay():
    pass

# Write text on log file
def writeLog(text):
    logFile = open("Overlord.log", "a")
    logFile.write("[%s] - %s\n" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), mensaje))
    logFile.close()

# Write start log
writeLog("Overlord started")

# Log here
while True:
    sleep(10)