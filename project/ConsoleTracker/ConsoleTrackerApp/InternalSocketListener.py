#!/usr/bin/env python3
import asyncio
import json
import socket
import sys
from threading import Thread

from .tasks import update_user_time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5073  # The port used by the server


def listen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        initMsg = {"conn_type": 1}
        s.sendall(json.dumps(initMsg).encode())
        while True:
            data = s.recv(1024)
            if data:
                data = json.loads(data.decode())
                messageType = int(data["messageType"])
                # Check for message type
                if messageType == 1:  # Update time request
                    timeBalance = int(data["timeBalance"])
                    username = data["username"]
                    print("Update time request")
                    update_user_time(username, timeBalance)
                elif messageType == 2:  # Ping request
                    print("Ping request")


def start_listener_daemon():
    # Background thread for the listener
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith(
            'win'):  # windows bug https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    t = Thread(target=listen)
    t.daemon = True
    t.start()
