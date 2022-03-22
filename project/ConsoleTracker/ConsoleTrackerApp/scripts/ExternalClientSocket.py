#!/usr/bin/env python3

import json
import random  # Random val generator
import socket
import string
import sys

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

# represents the time remining in a users account
time_db = {
    "chris354": 300,
    "eric123": 450,
    "daven634": 60
}

# TODO: refactor to seperate the different messages recieved
# outer while loop for restarting client
# inner for reading socket
while True:
    try:
        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((HOST, PORT))
        initMsg = {"conn_type": 2}
        s.sendall(json.dumps(initMsg).encode())
        while True:
            try:
                data = s.recv(1024)
                if data:
                    print(data)
                    data = json.loads(data.decode())
                    data["dest"] = "django"
                    # seperate the message types
                    if data["msg"] == "timer_update":
                        if data["username"] in time_db:
                            time_db[data["username"]] -= data["time"]
                            print(time_db)
                    else:
                        if data["username"] in user_db:  # Check if username exists
                            if user_db[data["username"]] == data["password"]:  # Is password correct?
                                data["usernameExists"] = True
                                data["validPassword"] = True
                                data["firstName"] = "Chris"
                                data["lastName"] = "Smith"
                                data["phoneNumber"] = 6475128443
                                data["timeRemaining"] = 5.344
                            else:  # Password is incorrect
                                data["usernameExists"] = True
                                data["validPassword"] = False
                        else:  # Username does not exist
                            data["usernameExists"] = False
                            data["validPassword"] = False
                    s.sendall(json.dumps(data).encode())
                else:                
                    # only reached if serversocket is closed
                    # break loop to restart client
                    break
            except socket.timeout:
                pass
    except KeyboardInterrupt:
        print("Socket closed.")
        s.close()
        sys.exit(0)
    except ConnectionError:
        print("Connection Lost. Reconnecting..")
        s.close()
