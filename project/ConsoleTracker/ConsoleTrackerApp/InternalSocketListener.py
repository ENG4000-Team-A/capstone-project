#!/usr/bin/env python3
import asyncio
import json
import socket
import sys
from threading import Thread

from .tasks import update_user_time, ping_all_machines

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5073  # The port used by the server


def listen():
    # outer while loop for restarting client
    # inner for reading socket
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            initMsg = {"conn_type": 1}
            s.sendall(json.dumps(initMsg).encode())
            while True:
                data = s.recv(1024)
                if data:
                    print(data)
                    data = json.loads(data.decode())
                    msg = data["msg"] if "msg" in data else ""
                    # Check for message type
                    if msg == "timer_update":  # Update time request
                        timeBalance = int(data["timeBalance"])
                        username = data["username"]
                        if update_user_time(username, timeBalance):
                            print("Update time request SUCCESS")
                        else:
                            print("Update time request FAILED")
                    elif msg == "ping":  # Ping request
                        print("Ping request")
                        data["dest"] = "external"
                        data["machines"] = [dump(machine) for machine in ping_all_machines()]
                        s.sendall(json.dumps(data).encode())
                else:
                    # only reached if serversocket is closed
                    # break loop to restart client
                    break
        except:
            pass


# Turn machine query to JSON format
def dump(machine):
    return {"name": machine.name, "active": machine.active, "ip": machine.ip, "mac": machine.mac,
            "machine_type": machine.machine_type}


def start_listener_daemon():
    # Background thread for the listener
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith(
            'win'):  # windows bug https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    t = Thread(target=listen)
    t.daemon = True
    t.start()
