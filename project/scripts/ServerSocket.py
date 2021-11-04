#!/usr/bin/env python3

import socket
import selectors
import time
import types
import json
HOST = '127.0.0.1'
PORT = 5073

EXTERNAL_FOUND = False
MSG_QUEUE = []
RESPONSE_QUEUE = []
ID = 0

'''
Barebones implementation of a socket. Need to rewrite as a class, use ssl, etc.
Run this file. Then ExternalClient, then InternalClient.

'''
def accept_wrapper(sel,sock):
    global EXTERNAL_FOUND, EXTERNAL_SOCK, ID
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', conn, addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, external=False, uid=ID) if EXTERNAL_FOUND else types.SimpleNamespace(addr=addr, external=True)
    EXTERNAL_FOUND = True
    ID +=1
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def get_msg(data):
    global RESPONSE_QUEUE
    response = None
    for i in RESPONSE_QUEUE:
        if i["uid"] == data.uid:
            response = i
            RESPONSE_QUEUE.remove(i)
            return response
    return response

def service_connection(sel,key, mask):
    global MSG_QUEUE, RESPONSE_QUEUE
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            dcd_recv_data = json.loads(recv_data.decode())
            if data.external:
                print("external response:", dcd_recv_data)
                RESPONSE_QUEUE.append(dcd_recv_data)
            else:
                dcd_recv_data['uid'] = data.uid
                MSG_QUEUE.append(dcd_recv_data)
        elif not data.external:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.external:
            if len(MSG_QUEUE) > 0:
                msg = MSG_QUEUE.pop()
                sent = sock.send(json.dumps(msg).encode())
                print("Sent to external:", msg)
        else:
            response = get_msg(data)
            if response is not None:
                print('echoing', response, 'to', data.addr)
                sent = sock.send(json.dumps(response).encode())  # Should be ready to write

def main():
    sel = selectors.DefaultSelector()

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print('listening on', (HOST, PORT))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(sel,key.fileobj)
            else:
                service_connection(sel, key, mask)

if __name__ == "__main__":
    main()
