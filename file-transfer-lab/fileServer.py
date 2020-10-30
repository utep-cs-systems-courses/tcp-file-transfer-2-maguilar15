#! /usr/bin/env python3

import os, socket
from lib.Color import Color as c

from lib.params import parseParams
from lib.framedSock import framedReceive, framedSend

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50000"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


paramMap = parseParams(switchesVarDefaults)

server_address, usage = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()


# Server Environment Variables
path = "file-transfer-lab/server_dump/"
debug = False

# Global
defaultFilePath = os.path.join(os.getcwd(),path)

def list_files(server_file_path:str=defaultFilePath):
    os.chdir(server_file_path)
    return f"{dict(enumerate(os.listdir()))}"


def write_to_file(fileName:str, data:str):
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


def run_server(server_address:str):
    hostname, port = server_address.split(":", 2)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((hostname, int(port)))
    s.listen(1)

    # Error Flag, Server On
    error = False

    while not error:
        rc = os.fork()
        if not rc:
            try:
                # wait until incoming connection request
                os.write(1,f"{c.F_LightCyan}[-] Waiting for incoming requests......\n".encode())
                conn, addr = s.accept()
                os.write(1,f"{c.OKGREEN}[+] Connected by client: {addr}\n".encode())
                # Retrieve File Name
                fileName = framedReceive(conn, False)
                os.write(1,f"{c.OKGREEN}[+] File Name Received: {fileName.decode()}\n".encode())

                # Accept Incoming Text
                data = framedReceive(conn, False)

                # Process Message
                if data:
                    fileName = fileName.decode("utf-8")
                    data = data.decode("utf-8")
                    # write to remote directory, check if file already exists
                    write_to_file(fileName=fileName, data=data)

                if debug:
                    os.write(1,f"{c.B_LightYellow}[?] Status 200: Received Data ({data})\n".encode())
                    os.write(1,f"{c.B_LightYellow}[?] Sending Data: {data}\n".encode())

                conn.close()
            except Exception as e:
                os.write(2,f"{c.F_Red}[X] Status 500: Server Exception={e}\n".encode())
                error = True
        else:
            os.write(1, f"{c.OKGREEN}[-] Exit Code: {os.wait()}\n".encode())


if __name__ == "__main__":
    run_server(server_address=server_address)


