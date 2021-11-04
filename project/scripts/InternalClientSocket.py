#!/usr/bin/env python3

import socket, json, argparse
from argparse import RawTextHelpFormatter
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5073        # The port used by the server

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument("-m", "--message", help="Message to send.")
args = parser.parse_args()
msg = args.message if args.message is not None else "sample message"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall("{{\"msg\": \"{m}\"}}".format(m=msg).encode())
    print("Sent:", msg)
    data = s.recv(1024)
    print("Recieved:", data.decode())

