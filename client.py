#!/usr/bin/python
from time import gmtime, strftime, sleep

# Return base64 encoded file
def file_to_base64():
    return ""

# Send replay to an Overmind
def send_replay():
    pass

# Write text on log file
def write_log(text):
    log_file = open("Overlord.log", "a")
    log_file.write("[%s] - %s\n" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), text))
    log_file.close()

# Write start log
write_log("Overlord started")

# Log here
while True:
    sleep(10)