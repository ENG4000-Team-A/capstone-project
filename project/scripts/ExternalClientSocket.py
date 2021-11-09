#!/usr/bin/env python3

import socket, json, sys, signal
import string
import random  # Random val generator

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5073  # The port used by the server


# Generate Dummy Authentication Key
def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Dummy User Values to check for authentication
user_db = {
    "chris354": "greet984;d",
    "eric123": "redBlue35j/",
    "daven634": "56509jeanHHH"
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1024)
        if data:
            print(data)
            data = json.loads(data.decode())
            if data["username"] in user_db:  # Check if username exists
                if user_db[data["username"]] == data["password"]:  # Is password correct?
                    data["response"] = data["username"] + " logged in successfully. Here is your authentication " \
                                                          "code " + id_generator()
                else:  # Password is incorrect
                    data["response"] = "Password entered was incorrect for " + data["username"] + ". Please try again"
            else:  # Username does not exist
                data["response"] = "Username " + data["username"] + " doesnt exist. Please try again"
            s.sendall(json.dumps(data).encode())
