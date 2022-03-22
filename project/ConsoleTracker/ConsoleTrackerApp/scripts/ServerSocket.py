#!/usr/bin/env python3

import socket
import selectors
from socket import AF_INET, SOCK_STREAM
from selectors import EVENT_READ, EVENT_WRITE
from types import SimpleNamespace
import json
import sys

HOST = '127.0.0.1'
PORT = 5073


class ServerSocket:
    """A socket implementation for communication from ConsoleTracker to any External Applications"""

    def __init__(self):
        """
        Attributes
        ----------
        msg_queue: Holds messages 
        connection_id: connection id (Unique)
        socket_recievers: dict holding connection ids for django, external
        lsock: the server socket
        sel: selector to allows effiecient concurrency
        """
        self.msg_queue = []
        self.connection_id = 0
        self.socket_recievers = {"django": None, "external": None}

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
            try:
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
            # close on Ctrl-C
            except KeyboardInterrupt:
                sys.exit(0)
            # disconnect all sockets and return for restarting server
            except ConnectionError:
                events = self.sel.select()
                for key, _ in events:
                    self.sel.unregister(key.fileobj)
                self.lsock.close()
                return

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
        data = SimpleNamespace(addr=addr, cid=self.connection_id)
        self.connection_id += 1
        events = EVENT_READ | EVENT_WRITE
        self.sel.register(conn, events, data=data)

    def read_connection(self, sock, data):
        """Reads from a client socket

	    Parameters
        ----------
        sock: Socket
            The client socket
        data: SimpleNamespace
            An object holding data specific to socket: address, external, cid
        """
        recv_data = sock.recv(1024)
        if recv_data:
            print("Recieved: ", recv_data.decode())
            dcd_recv_data = json.loads(recv_data.decode())
            if 'conn_type' in dcd_recv_data.keys():
                if dcd_recv_data['conn_type'] == 1:
                    self.socket_recievers["django"] = data.cid
                elif dcd_recv_data['conn_type'] == 2:
                    self.socket_recievers["external"] = data.cid
            else:
                if 'id' not in dcd_recv_data.keys():
                    dcd_recv_data['id'] = data.cid
                    dcd_recv_data['state'] = "request"
                else:
                    dcd_recv_data['state'] = "response"
                if 'dest' in dcd_recv_data.keys():
                    self.msg_queue.append(dcd_recv_data)
                    print("Adding msg to queue = ", dcd_recv_data)
                else:
                    print("Ignoring message. No dest specified")
        elif data.cid in self.socket_recievers:
            pass
        else:
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
            An object holding data specific to socket: address, external, cid
	    """

        if len(self.msg_queue) > 0:
            msg = None
            if data.cid == self.socket_recievers["django"] or data.cid == self.socket_recievers["external"]:
                msg = self.get_message(data, "request")
            else:
                msg = self.get_message(data, "response")

            if msg is not None:
                sock.send(json.dumps(msg).encode())
                print("Sent to cid {c}:".format(c=data.cid), msg)

    def get_message(self, data, state):
        """Retrieves a response for a client if there exists one.

        Parameters
        ----------
        data: SimpleNamespace
            An object holding data specific to socket: address, external, cid
        """
        msg = None
        to_Django = False
        to_External = False

        if state == "request":
            if data.cid == self.socket_recievers["django"]:
                to_Django = True
            elif data.cid == self.socket_recievers["external"]:
                to_External = True

        for i in self.msg_queue:
            if i["state"] == state and ((i["id"] == data.cid) or (to_Django and i["dest"] == "django") or (
                    to_External and i["dest"] == "external")):
                msg = i
                self.msg_queue.remove(i)
                return msg
        return msg


if __name__ == "__main__":
    # restart the server whenever a client disconnects
    while True:
        try:
            server = ServerSocket()
            server.start()
        except KeyboardInterrupt:
            sys.exit(0)
        except ConnectionError:
            pass
