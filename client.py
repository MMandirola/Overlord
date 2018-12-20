#!/usr/bin/python
import base64
import math
import requests
from time import gmtime, strftime, sleep
from sc2_wrapper import client as game
import uuid
import asyncio
import json
import os
import subprocess
import time
try:
    from local_settings import *
except ImportError:
    pass


class Overlord:

    # Main constructor
    def __init__(self, replays_url, max_delay):
        self.replays_url = replays_url
        self.max_delay = max_delay
        self.log_file = "Overlord.log"

    # Send replay to an Overmind
    def send_replay(self, replay_title, base64_encoded_text, extra_text):

        # Build JSON body
        body = {'title': replay_title,
                'base64_file': base64_encoded_text, 'extra': extra_text}

        # Send replay (HTTP post with exp. regression)
        power = 1
        while (power > 0):
            try:
                request = requests.post(self.replays_url, json=body)
                power = 0
            except Exception as e:
                delay = 2**power
                if delay > self.max_delay:
                    sleep(self.max_delay)
                else:
                    sleep(delay)
                    power += 1

        # Return HTTP status code
        return request.status_code

    # Write text on log file
    def write_log(self, text):
        log_file = open(self.log_file, "a")
        log_file.write("[%s] - %s\n" %
                       (strftime("%Y-%m-%d %H:%M:%S", gmtime()), text))
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

    def process_replay(self):

        pass


def base64_to_file(base64_encoded_text, file_path):

    # Open encoded file
    replay_file = open(file_path, "wb")
    replay_file.write(base64.b64decode(base64_encoded_text))
    replay_file.close()

    return True


def main():

    # Overlord client
    client = Overlord(URL, 1024)
    # Write start log
    client.write_log("Overlord started")
    loop = asyncio.get_event_loop()

    while True:
        try:
            if MODE == "CLASSIFY":
                r = requests.get(URL+"/replays/classify")
                if r.status_code == 200:
                    payload = r.json()
                    id = payload["title"]
                    uuidV = uuid.uuid1()
                    pay = payload["base64"][2:]
                    base64_to_file(pay, REPLAY_ROUTE+str(id))
                    file_path = str(id)
                    meta = loop.run_until_complete(game.classify(
                        REPLAY_ROUTE+str(id)))
                    meta = json.loads(meta)
                    requests.post(
                        URL+"/classify/", {"id": id, "player": meta["races"][0], "opponent": meta["races"][1], "map": meta["map"]})
                    os.remove(REPLAY_ROUTE+str(id))
                else:
                    time.sleep(5)
            subprocess.call(
                ["sudo", "killall", "-9", "/home/rts/StarCraftII/Versions/Base55958/SC2_x64"])
        except Exception as e:
            print(e)
    loop.close()


if __name__ == "__main__":
    main()
