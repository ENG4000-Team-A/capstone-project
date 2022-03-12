#!/usr/bin/env python3

import argparse
import json
import socket
from argparse import RawTextHelpFormatter

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5073  # The port used by the server

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument("-m", "--msg", help="MessageType to send.")
parser.add_argument("-d", "--dest", help="destination of message.")
args = parser.parse_args()

msg = "ping"
dest = "django"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall("{{\"msg\": \"{m}\", \"dest\": \"{d}\"}}".format(m=msg, d=dest).encode())
    print("Sent dummy request with msg : " + msg + ", dest : " + dest)

    data = s.recv(1024)
    data = json.loads(data.decode())
    print("Response : " + data)
