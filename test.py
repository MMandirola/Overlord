#!/usr/bin/python
from client import *

def main():

    # Overlord client
    client = Overlord(REPLAYS_URL, MAX_DELAY)

    # Check client attributes
    print(client.replays_url)
    print(client.max_delay)
    print(client.log_file)

    # Test log
    client.write_log("Overlord started")

    # File to base64 string
    base64_string = client.file_to_base64("/home/sc2/dev/Overlord/Replays/replay1.SC2Replay")

    # Base64 string to file
    print(client.base64_to_file(base64_string, "/home/sc2/dev/Overlord/Replays/replay1_copy.SC2Replay"))

    # Send file
    status_code = client.send_replay("overlord1.SC2Replay", base64_string, "")
    print(status_code)

if __name__ == "__main__":
    main()