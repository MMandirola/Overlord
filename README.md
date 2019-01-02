# Overlord

## Installation

### VM
#### Arch-linux
* Create user `Overlord`
* Clone this repo into `/home/Overlord/`
* Copy `Overlord.service` into `/etc/systemd/system/`
* Start and enable Overlord service: `sudo systemctl start Overlord && sudo systemctl enable Overlord`

### Non VM

* Download Starcraft2 client 3.16.1
* Extract Battle.net.tar.xz into Battle.net Cache
* pip install -r requirements.txt
* Create a local_setting.py into the same folder as client.py with this settings

`URL = "dumbbots.ddns.net"
MAX_DELAY = 1024
SERVER_ROUTE = "{{ Starcraft route }}"
SERVER_ADDRESS = "127.0.0.1"
REPLAY_ROUTE = "{{ Starcraft replays folder }}"
DATABASE_NAME = "mongo"
DATABASE_ROUTE = "localhost"
DATABASE_PORT = 27017
MODE = "CLASSIFY"`

* sudo python3 client.py
