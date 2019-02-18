#!/usr/bin/python
import base64
import math
import requests
from time import gmtime, strftime, sleep
from sc2_wrapper import client as game
from sc2_wrapper.players.cbr_algorithm import CBRAlgorithm
import uuid
import asyncio
import json
import os
import subprocess
import time
from sys import getsizeof
import traceback
import pkg_resources
import sys
import os

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR + "/sc2_wrapper")
print(sys.path)

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



    # Write decode base64 string to a file

    def process_replay(self):

        pass


def base64_to_file(base64_encoded_text, file_path):

    # Open encoded file
    replay_file = open(file_path, "wb")
    replay_file.write(base64.b64decode(base64_encoded_text))
    replay_file.close()

    return True
# Return base64 encoded string
def file_to_base64(file_path):

    # Open encoded file
    replay_file = open(file_path, "rb")
    file_content = replay_file.read()
    replay_file.close()

    # Encode file content and return it
    return base64.b64encode(file_content)

async def main():

    # Overlord client
    client = Overlord(URL, 1024)
    # Write start log
    client.write_log("Overlord started")


    while True:
        version = pkg_resources.get_distribution("SC2ApiWrapper").version
        try:
            r = requests.get(URL+"/mode")
            payload = r.json()
            payload = payload[0]
            print(payload)
            if payload["fields"]["title"] == "CLASSIFY":
                r = requests.get(URL+"/replays/classify")
                payload = r.json()
                id = payload["title"]
                pay = payload["base64"][2:]
                base64_to_file(pay, REPLAY_ROUTE+str(id))
                file_path = str(id)
                meta = await game.classify(
                    REPLAY_ROUTE+str(id))
                meta = json.loads(meta)
                requests.post(
                    URL+"/classify/", {"id": id, "player": meta["races"][0], "opponent": meta["races"][1], "map": meta["map"]})
                os.remove(REPLAY_ROUTE+str(id))
            elif payload["fields"]["title"] == "UPDATE":
                subprocess.call(["git", "pull"])
                subprocess.call(["pip3", "install", "-r", "requirements.txt", "--force-reinstall", "--no-cache-dir"])
            elif payload["fields"]["title"] == "PROCESS":
                path = "/replays?"
                if payload["fields"]["map"]:
                    path += "map=" + payload["fields"]["map"] + "&"
                if payload["fields"]["player"]:
                    path += "player=" + payload["fields"]["player"] + "&"
                if payload["fields"]["oponent"]:
                    path += "oponent=" + payload["fields"]["oponent"] + "&"
                r = requests.get(URL+path)
                payload = r.json()
                id = payload["title"]
                pay = payload["base64"][2:]
                base64_to_file(pay, REPLAY_ROUTE+str(id))
                file_path = str(id)
                observations = []
                counter = 0
                async for obs in game.load_replay(REPLAY_ROUTE+str(id)):
                    observations.append(obs)
                    counter += 1
                    if counter == 12:
                        observations = json.dumps(observations)
                        requests.post(
                            URL+"/proccess/", {"id": id, "observations": observations})
                        counter = 0
                        observations = []

                observations = json.dumps(observations)
                requests.post(
                    URL+"/proccess/", {"id": id, "observations": observations})
                requests.post(
                    URL+"/proccess/finish", {"id": id })               
                os.remove(REPLAY_ROUTE+str(id))
            elif payload["fields"]["title"] == "PLAY":
                difficulty = payload["fields"]["difficulty_opponent"]
                if not difficulty:
                    difficulty = "VeryEasy"
                observations = []
                i = 0
                while i < 80:
                    print(i)
                    r = requests.get(URL + "/sample/")
                    if r.status_code == 200:
                        observations += r.json()
                        i += 1
                    else:
                        print("Error, retrying")
                player1 = CBRAlgorithm()
                await player1.create(
                        "Terran", "Human",
                        server_route=SERVER_ROUTE, server_address=SERVER_ADDRESS,
                        cases=observations, rules=[],
                )
                replay_name, result = await game.play_vs_ia(player1, {}, "InterloperLE.SC2Map", "Terran", difficulty, 24)
                requests.post(
                    URL+"/stats/", {"version": str(version), "difficulty":difficulty, "name": replay_name, "result": str(result)})
                base64_replay = file_to_base64(replay_name)
                requests.post(URL+"/player_replay/", {"title": replay_name, 'base64_file': base64_replay})
                os.remove(replay_name)        
            elif payload["fields"]["title"] == "FEEDBACK":
                path = "/feedback/"
                r = requests.get(URL+path)
                payload = r.json()
                id = payload["title"][8:]
                pay = payload["base64"]
                base64_to_file(pay, REPLAY_ROUTE+str(id))
                file_path = str(id)
                observations = []
                counter = 0
                async for obs in game.load_replay(REPLAY_ROUTE+str(id)):
                    observations.append(obs)
                    counter += 1
                    if counter == 12:
                        observations = json.dumps(observations)
                        requests.post(
                            URL+"/proccess_feedback/", {"id": id, "observations": observations})
                        counter = 0
                        observations = []

                observations = json.dumps(observations)
                requests.post(
                    URL+"/proccess_feedback/", {"id": id, "observations": observations})
                requests.post(
                    URL+"/proccess_feddback/finish/", {"id": id })               
                os.remove(REPLAY_ROUTE + str(id))
            subprocess.call(
                ["sudo", "killall", "-9", SERVER_ROUTE + "/Versions/Base55958/SC2_x64"])
        except Exception as e:
            time.sleep(5)
            traceback.print_exc()
            print(e)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
