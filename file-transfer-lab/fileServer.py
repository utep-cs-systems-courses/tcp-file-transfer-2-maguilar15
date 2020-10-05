#! /usr/bin/env python3

import os, socket
from lib.framedSock import framedReceive
from lib.Color import Color as c

# Environment Variable
server_address = os.getenv("HOSTNAME") if os.getenv("HOSTNAME") else "127.0.0.1:50001"
proxyEnable = ":50000" in server_address if True else False

# Server Environment Variables
listenAddr,listenPort = server_address.split(":",2)
path = "file-transfer-lab/server_dump/"
debug = False

# Global
defaultFilePath = os.path.join(os.getcwd(),path)

def list_files(server_file_path:str=defaultFilePath):
    os.chdir(server_file_path)
    return f"{dict(enumerate(os.listdir()))}"


def _write_to_file(fileName:str,data:str):
   """
   Write to file and test if it exists. If it exists throw an exception and apologize for the inconvenience.
   :param fileName: filename to test if it exists. Thie filename stored in the file server.
   :param data: data
   :return:
   """
   filePath = defaultFilePath + fileName
   if os.path.isfile(filePath):
       os.write(2, f"{c.F_Red}[X] File Already Exists\n".encode())
       return
   try:
        with open(filePath, "wb") as f:
            f.write(bytes(data, encoding="utf-8"))
        f.close()
   except Exception as e:
       print(f"[X] Failed to writing to file : exception={e}, filepath = {defaultFilePath + fileName}, data={data}")


def run_server(hostname:str=listenAddr,port:int=int(listenPort)):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Standby for connection
    s.bind((hostname, port))
    # Allow 1 client connection
    s.listen(1)

    # Error Flag, Server On
    error = False

    rc = os.fork()

    if not rc:
        while not error:

            try:
                # wait until incoming connection request
                os.write(1,f"{c.F_LightCyan}[-] Waiting for incoming requests......\n".encode())
                conn, addr = s.accept()
                os.write(1,f"{c.OKGREEN}[+] Connected by client: {addr}\n".encode())
                # Retrieve File Name
                fileName = conn.recv(1024).decode()
                os.write(1,f"{c.OKGREEN}[+] File Name Received: {fileName}\n".encode())

                # Accept Incoming Text (Automate)
                data = conn.recv(100000).decode()

                # exit
                if data == "":
                    break

                # Process Message
                if data:
                    # write to remote directory, check if file already exists
                    _write_to_file(fileName=fileName, data=data)

                if debug:
                    os.write(1,f"{c.B_LightYellow}[?] Status 200: Received Data ({data})\n".encode())
                    os.write(1,f"{c.B_LightYellow}[?] Sending Data: {data}\n".encode())

                conn.close()

            except Exception as e:
                os.write(2,f"{c.F_Red}[X] Status 500: Server Exception={e}\n".encode())
                error = True
    else:
        childProcess = os.wait()
        os.write(2,f"{c.F_Red} [X] Child Process Terminated, Code: {childProcess}\n".encode())

if __name__ == "__main__":
    run_server()


