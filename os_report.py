#!/usr/bin/env python3

# modules: requests psutil

import json
import os
import psutil
import requests
from subprocess import Popen, PIPE
import time

apikey = "2032057e1f79261b04bfd9a17ffc90eb"
computer_name = "MacBook Pro"
interval = 10

def construct_name(n):
    return computer_name + " - " + n

def send(data):
    payload = {
        "json": json.JSONEncoder(sort_keys=True).encode(data),
        "apikey": apikey
    }
    r = requests.get(r"https://emoncms.org/input/post.json", params=payload)
    print("Response: ", r.text)


if __name__ == "__main__":
    while True:
        a, b, c = os.getloadavg()
        p = Popen([os.path.join(os.path.dirname(os.path.realpath(__file__)), "osx-cpu-temp", "osx-cpu-temp")], stdout=PIPE)
        cpu_temp = float(p.communicate()[0].decode())
        data = {
            construct_name(r"boot time"): psutil.boot_time(),
            construct_name(r"load average - 1min"): a,
            construct_name(r"load average - 5min"): b,
            construct_name(r"load average - 15min"): c,
            construct_name(r"CPU usage"): psutil.cpu_percent(),
            construct_name(r"memory usage"): psutil.virtual_memory().percent / 100,
            construct_name(r"system disk usage"): psutil.disk_usage('/').percent / 100,
            construct_name(r"process count"): len(psutil.pids()),
            construct_name(r"CPU temperature"): cpu_temp
        }
        print("Sending: ", data)
        send(data)
        time.sleep(interval)
