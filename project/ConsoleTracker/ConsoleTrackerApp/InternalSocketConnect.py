from datetime import timedelta
import json
import socket


# Used to send a request to socket
class InternalSocket:
    def __init__(self):
        self.host = '127.0.0.1'  # The server's hostname or IP address
        self.port = 5073  # The port used by the server

    def send_request(self, username, password):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.settimeout(5)
                s.connect((self.host, self.port))
                s.sendall("{{\"msg\": \"{m}\", \"username\": \"{u}\", \"password\": \"{p}\",\"dest\": \"external\"}}"
                        .format(m="Sending username & password", u=username, p=password).encode())
                data = s.recv(1024)
                data = json.loads(data.decode())
            except socket.timeout:
                data = {}
        # Return the json data no matter what for now because we just want to show the json object data
        # in the response after whatever login scenario occurred. Later on will have conditions for true and false
        return data

    def update_time(self, username, timeBalance, timeDelta):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.settimeout(5)
                s.connect((self.host, self.port))
                s.sendall(
                    "{{\"dest\": \"external\", \"msg\": \"{m}\", \"username\": \"{u}\", \"timeBalance\": {tb}, "
                    "\"timeDelta\": {td}}} "
                    .format(m="timer_update", u=username, tb=timeBalance, td=timeDelta).encode())
                data = s.recv(1024)
                data = json.loads(data.decode())
            except socket.timeout:
                data = {}
        # Return the json data no matter what for now because we just want to show the json object data
        # in the response after whatever login scenario occurred. Later on will have conditions for true and false
        return data
