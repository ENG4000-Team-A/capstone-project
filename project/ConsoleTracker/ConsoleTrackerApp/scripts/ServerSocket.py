#!/usr/bin/env python3

import socket
import selectors
from socket import AF_INET, SOCK_STREAM
from selectors import EVENT_READ, EVENT_WRITE
from types import SimpleNamespace
import json

HOST = '127.0.0.1'
PORT = 5073


class ServerSocket:
    """A socket implementation for communication from ConsoleTracker to any External Applications"""

    def __init__(self):
        """
        Attributes
        ----------
        msg_queue: Holds messages to sent to external app
        response_queue: Holds reponse messages from external app
        msg_id: message id (Unique)
        lsock: the server socket
        sel: selector to allows effiecient concurrency
        """
        self.msg_queue = []
        self.response_queue = []
        self.msg_id = 0

        self.external_found = False
        self.sel = selectors.DefaultSelector()

        self.lsock = socket.socket(AF_INET, SOCK_STREAM)
        self.lsock.bind((HOST, PORT))
        self.lsock.listen()
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, EVENT_READ, data=None)

    def start(self):
        """Main function starting the socket server"""
        print("Starting server...")
        while True:
            events = self.sel.select(timeout=None)
            for key, mask in events:
                sock = key.fileobj
                if key.data is None:
                    self.accept_client(sock)
                else:
                    data = key.data
                    if mask & EVENT_READ:
                        self.read_connection(sock, data)
                    if mask & EVENT_WRITE:
                        self.write_to_connection(sock, data)

    def accept_client(self, sock):
        """Handles a new client to the socket

        Parameters
        ----------
        sock: Socket
            The client socket
        """
        conn, addr = sock.accept()
        print('Accepted connection from', conn, addr)
        conn.setblocking(False)
        data = SimpleNamespace(addr=addr, external=False, mid=self.msg_id) if self.external_found else SimpleNamespace(
            addr=addr, external=True)
        self.msg_id += 1
        self.external_found = True
        events = EVENT_READ | EVENT_WRITE
        self.sel.register(conn, events, data=data)

    def read_connection(self, sock, data):
        """Reads from a client socket

	Parameters
        ----------
        sock: Socket
            The client socket
        data: SimpleNamespace
            An object holding data specific to socket: address, external, message_id
        """
        recv_data = sock.recv(1024)
        if recv_data:
            dcd_recv_data = json.loads(recv_data.decode())
            if data.external:
                print("External Client Response:", dcd_recv_data)
                self.response_queue.append(dcd_recv_data)
            else:
                dcd_recv_data['mid'] = data.mid
                self.msg_queue.append(dcd_recv_data)
        elif not data.external:
            print('Closing connection to', data.addr)
            self.sel.unregister(sock)
            sock.close()

    def write_to_connection(self, sock, data):
        """Writes to a client socket

	Parameters
        ----------
        sock: Socket
            The client socket
        data: SimpleNamespace
            An object holding data specific to socket: address, external, message_id
	"""
        if data.external and len(self.msg_queue) > 0:
            msg = self.msg_queue.pop()
            sock.send(json.dumps(msg).encode())
            print("Sent to external:", msg)
        elif not data.external:
            response = self.get_message(data)
            if response is not None:
                print('Sent to client', response)
                sock.send(json.dumps(response).encode())

    def get_message(self, data):
        """Retrieves a response for a client if there exists one.

        Parameters
        ----------
        data: SimpleNamespace
            An object holding data specific to socket: address, external, message_id
        """
        response = None
        for i in self.response_queue:
            if i["mid"] == data.mid:
                response = i
                self.response_queue.remove(i)
                return response
        return response


if __name__ == "__main__":
    config_data = None
    with open('config.json', 'r') as f:
        config_data = json.load(f)
    print(config_data['external_client_ipv4'])

    server = ServerSocket()
    server.start()
