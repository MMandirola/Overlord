#!/usr/bin/python
from client import *

def main():

    # Overlord client
    client = Overlord(REPLAYS_URL)

    # Check client attributes
    print(client.replays_url)
    print(client.log_file)

    # Test log
    client.write_log("Overlord started")

    # File to base64 string
    base64_string = client.file_to_base64("/home/sc2/dev/Overlord/replay1.SC2Replay")

    # Base64 string to file
    print(client.base64_to_file(base64_string, "/home/sc2/dev/Overlord/replay1_copy.SC2Replay"))

    # Send file
    status_code = client.send_replay("overlord1.SC2Replay", base64_string, "")
    print("sent" if (status_code == 201) else "not sent")

if __name__ == "__main__":
    main()