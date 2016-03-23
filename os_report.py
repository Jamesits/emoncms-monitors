#!/usr/bin/env python3

# modules: requests psutil

import json
import os
import psutil
import requests
from subprocess import Popen, PIPE
import time

apikey = "2032057e1f79261b04bfd9a17ffc90eb"
computer_name = "mbp"
interval = 10

def construct_name(n):
    return computer_name + "-" + n

def run(command):
    p = Popen(command, stdout=PIPE)
    return p.communicate()[0]

def get_cpu_temp():
    return float(run([os.path.join(os.path.dirname(os.path.realpath(__file__)), "osx-cpu-temp", "osx-cpu-temp")]).decode()[:-3])

def get_battery_level():
    return float(run(["pmset", "-g", "batt"]).decode().split("\n")[1].split()[1][:-2])

def send(data):
    payload = {
        "json": json.JSONEncoder(sort_keys=True).encode(data),
        "apikey": apikey
    }
    r = requests.get(r"https://emoncms.org/input/post.json", params=payload)
    print("Response: ", r.text)


if __name__ == "__main__":
    while True:
        try:
            a, b, c = os.getloadavg()
            data = {
                construct_name(r"uptime"): psutil.boot_time(),
                construct_name(r"load-1min"): a,
                construct_name(r"load-5min"): b,
                construct_name(r"load-15min"): c,
                construct_name(r"cpu-percent"): psutil.cpu_percent(),
                construct_name(r"memory-percent"): psutil.virtual_memory().percent,
                construct_name(r"system-disk-percent"): psutil.disk_usage('/').percent,
                construct_name(r"process-count"): len(psutil.pids()),
                construct_name(r"cpu-temp"): get_cpu_temp(),
                construct_name(r"battery"): get_battery_level()
            }
            print("Sending: ", data)
            send(data)
            time.sleep(interval)
        except KeyboardInterrupt:
            break
        except:
            time.sleep(interval)
