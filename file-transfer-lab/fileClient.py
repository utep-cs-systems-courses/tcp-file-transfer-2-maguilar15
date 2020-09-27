#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../framed-echo/")

# Environment Variable
server_address = "127.0.0.1:50001"

# All files client will send are here
files = os.path.join(os.getcwd(), "file-transfer-lab/client_dump/")

def make_file_map():
    return dict(enumerate(list(os.listdir(files))))


def send_file(filename:str):
    # connect to socket
    s = _connect_to_server()
    # send filename for archiving on the file server
    path = files + filename
    s.send(bytes(filename, "utf-8"))
    # Get file byte size and write to file
    fileByteSize = os.path.getsize(path)
    with open(path, "rb") as f:
        byte = f.read(fileByteSize)
        s.send(bytes(byte.decode(),"utf-8"))
    f.close()
    os.write(1,f"Sent File Byte Size: {fileByteSize}\n".encode())


def send_buffer(sock, buf):
    while len(buf):
        print(f"trying to send <{buf}>...")
        nbytes = sock.send(buf)
        print(f" {nbytes} bytes sent, {len(buf) - nbytes} bytes remain")
        buf = buf[nbytes:]


def _connect_to_server(server:str=server_address):
    """
    Returns valid socket.
    :param server:
    :return: socket.
    """
    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    addrFamily = socket.AF_INET
    socktype = socket.SOCK_STREAM
    addrPort = (serverHost, serverPort)

    s = socket.socket(addrFamily, socktype)
    if s is None:
        print('could not open socket')
        sys.exit(1)

    s.connect(addrPort)

    if s is None:
        print('could not open socket')
        sys.exit(1)

    return s


def send_message_to_server(message:str,encoding:str="utf-8"):
    s = _connect_to_server()

    outMessage = bytes(message,encoding=encoding)

    print("sending '%s'" % message)
    send_buffer(s, outMessage)

    data = s.recv(1024).decode()
    print("Received '%s'" % data)

    print("sending '%s'" % message)
    send_buffer(s, outMessage)

    # No more output
    s.shutdown(socket.SHUT_WR)

    # Closing Socket
    s.close()

