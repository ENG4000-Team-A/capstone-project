#!/usr/bin/env python3

import socket, json, sys, signal
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5073        # The port used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1024)
        if data:
            print(data)
            data = json.loads(data.decode())
            data["response"] = data["msg"] + " recieved"
            s.sendall(json.dumps(data).encode())



