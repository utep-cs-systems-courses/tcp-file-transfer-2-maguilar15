#! /usr/bin/env python3

import os, socket
from lib.framedSock import framedReceive
from lib.Color import Color as c

from lib.params import parseParams

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50000"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


paramMap = parseParams(switchesVarDefaults)

server_address, usage = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

from threading import Thread, Lock
from framedSocket import EncapFramedSock
from fileServer import write_to_file

class Server(Thread):
    def __init__(self,socketFamily):
        Thread.__init__(self)
        self.lock = Lock()
        self.fsock = EncapFramedSock(socketFamily)

    def run(self):
        # Error Flag, Server On
        debug = False
        self.lock.acquire()
        try:
            # wait until incoming connection request
            os.write(1, f"{c.F_LightCyan}[-] Waiting for incoming requests......\n".encode())

            os.write(1, f"{c.OKGREEN}[+] Connected by client: {self.fsock.addr}\n".encode())

            # Retrieve File Name
            fileName = self.fsock.sock.recv(1024).decode()
            os.write(1, f"{c.OKGREEN}[+] File Name Received: {fileName}\n".encode())

            # Accept Incoming Text (Automate)
            data = self.fsock.sock.recv(100000).decode()

            # Process Message
            if data:
                # write to remote directory, check if file already exists
                write_to_file(fileName=fileName, data=data)

            if debug:
                os.write(1, f"{c.B_LightYellow}[?] Status 200: Received Data ({data})\n".encode())
                os.write(1, f"{c.B_LightYellow}[?] Sending Data: {data}\n".encode())
            self.fsock.sock.close()
            self.lock.release()
        except Exception as e:
            os.write(2, f"{c.F_Red}[X] Status 500: Server Exception={e}\n".encode())




if __name__ == "__main__":
    server = server_address.split(":")
    socketFamily = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketFamily.bind((server[0], int(server[1])))
    socketFamily.listen(1)
    while True:
        server = Server(socketFamily)
        server.start()
