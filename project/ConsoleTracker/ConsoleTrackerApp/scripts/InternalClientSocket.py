#!/usr/bin/env python3

import argparse
import json
import socket
from argparse import RawTextHelpFormatter

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5073  # The port used by the server

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument("-m", "--message", help="Message to send.")
parser.add_argument("-u", "--username", help="Username to send.")
parser.add_argument("-p", "--password", help="Password to send.")
args = parser.parse_args()
msg = args.message if args.message is not None else "Login Request For"
username = args.message if args.message is not None else "chris354"  # Dummy Username
password = args.message if args.message is not None else "greet984;d"  # Dummy Password

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall("{{\"msg\": \"{m}\", \"username\": \"{u}\", \"password\": \"{p}\"}}"
              .format(m=msg, u=username, p=password).encode())
    print("Sent:", msg, username)
    data = s.recv(1024)
    data = json.loads(data.decode())
    if data["usernameExists"] and data["validPassword"]:
        print("Login Success")
    else:
        print("Login Failed")

