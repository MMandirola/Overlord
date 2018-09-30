#!/usr/bin/python
import base64
import math
import requests
from time import gmtime, strftime, sleep
try:
    from local_settings import *
except ImportError:
    pass

class Overlord:

    # Main constructor
    def __init__(self, replays_url):
        self.replays_url = replays_url
        self.log_file = "Overlord.log"

    # Send replay to an Overmind
    def send_replay(self, replay_title, base64_encoded_text, extra_text):

        # Build JSON body
        body = {'title': replay_title, 'base64_file': base64_encoded_text, 'extra': extra_text}

        # Send replay (HTTP post with exp. regression)
        delay = 1
        while (delay > 0):
            try:
                request = requests.post(self.replays_url, json=body)
                delay = 0
            except Exception as e:
                sleep(math.exp(delay))
                delay += 1

        # Return HTTP status code
        return request.status_code

    # Write text on log file
    def write_log(self, text):
        log_file = open(self.log_file, "a")
        log_file.write("[%s] - %s\n" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), text))
        log_file.close()

    # Return base64 encoded string
    def file_to_base64(self, file_path):

        # Open encoded file
        replay_file = open(file_path, "rb")
        file_content = replay_file.read()
        replay_file.close()

        # Encode file content and return it
        return base64.b64encode(file_content)

    # Write decode base64 string to a file
    def base64_to_file(self, base64_encoded_text, file_path):

        # Open encoded file
        replay_file = open(file_path, "wb")
        replay_file.write(base64.b64decode(base64_encoded_text))
        replay_file.close()
        
        return True

def main():

    # Overlord client
    client = Overlord(REPLAYS_URL)

    # Write start log
    client.write_log("Overlord started")

    while True:
        sleep(10)

if __name__ == "__main__":
    main()