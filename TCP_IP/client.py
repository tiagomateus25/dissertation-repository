#!/usr/bin/env python3

import socket
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.56.42', 10000) # ESP's ip address
# server_address = ('192.168.56.237', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

while True:
    # sock.connect(server_address)
    data = sock.recv(1024)
    print('Value received: ', data.decode('utf8'))
