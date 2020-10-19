#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os
#sys.path.append("../framed-echo/")
from lib.framedSock import framedSend, framedReceive


# All files client will send are here
files = os.path.join(os.getcwd(), "file-transfer-lab/client_dump/")


def make_file_map():
    return dict(enumerate(list(os.listdir(files))))


def send_file(serverAddress:str, filenameHostMachine:str,filenameRemoteMachine:str):
    # connect to socket
    sock = _connect_to_server(serverAddress)
    # send filename for archiving on the file server
    path = files + filenameHostMachine
    # Send Message
    framedSend(sock,filenameRemoteMachine)
    # Get file byte size and write to file
    fileByteSize = os.path.getsize(path)
    with open(path, "rb") as f:
        byte = f.read(fileByteSize)
        #s.send(bytes(byte.decode(),"utf-8"))
        framedSend(sock,byte.decode())
    #framedReceive(s,1)
    f.close()
    os.write(1,f"Sent File Byte Size: {fileByteSize}\n".encode())


def _connect_to_server(server:str):
    """
    Returns valid socket.
    :param server:
    :return: socket connection.
    """
    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        os.write(2,f"Can't parse server:port from environment variable HOSTNAME: {server}".encode())
        sys.exit(1)

    addrFamily = socket.AF_INET
    socktype = socket.SOCK_STREAM
    addrPort = (serverHost, serverPort)

    s = socket.socket(addrFamily, socktype)
    if s is None:
        os.write(2,'could not open socket'.encode())
        sys.exit(1)

    s.connect(addrPort)

    if s is None:
        os.write(2,'could not open socket'.encode())
        sys.exit(1)

    return s

