#!/usr/bin/env python3

import argparse
import json
import socket
from argparse import RawTextHelpFormatter

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5073  # The port used by the server

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument("-m", "--messageType", help="MessageType to send.")
parser.add_argument("-u", "--username", help="Username to send.")
parser.add_argument("-p", "--timeBalance", help="timeBalance to send.")
args = parser.parse_args()

messageType = 1
username = "chris354"
timeBalance = 200

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall("{{\"messageType\": \"{m}\", \"username\": \"{u}\", \"timeBalance\": \"{t}\"}}"
              .format(m=messageType, u=username, t=timeBalance).encode())
    print("Sent dummy request with username : " + username + ", timeBalance : " + str(timeBalance))
