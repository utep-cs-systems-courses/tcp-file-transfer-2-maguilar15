#! /usr/bin/env python3

import os

import sys
import socket, re

from client import client

if __name__ == "__main__":

    fileDirectory = client.make_file_map()
    print(f"Choose a number for TCP file transfer: {fileDirectory}\n")

    while 1:
        os.write(1,"> ".encode())
        prompt = os.read(0,128).decode().strip().replace("\n","")
        #client.send_message_to_server(prompt)

        try:
            client.send_file(filename=fileDirectory[int(prompt)])
        except Exception as e:
            os.write(2,f"Only numbers accepted right now, exception={e}\n".encode())