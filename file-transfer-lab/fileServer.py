#! /usr/bin/env python3

import os, socket

# Server Environment Variables
listenAddr = "127.0.0.1"
listenPort = 50001
path = "file-transfer-lab/server_dump/"
debug = False

# Global ?
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
       os.write(2, "[X] File Already Exists\n".encode())
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

    while not error:
        try:
            # wait until incoming connection request
            os.write(1,"[-] Waiting for incoming requests......\n".encode())
            conn, addr = s.accept()
            os.write(1,f"[+] Connected by client: {addr}\n".encode())
            # Retrieve File Name
            fileName = conn.recv(1024).decode()
            os.write(1,f"[+] File Name Present: {fileName}\n".encode())

            # Accept Incoming Text (Automate)
            data = conn.recv(100000).decode()
            if data:
                # Write to remote directory, check if file already exists
                _write_to_file(fileName=fileName,data=data)

            if debug:
                os.write(1,f"[?] Status 200: Received Data ({data})\n".encode())
                os.write(1,f"[?] Sending Data: {data}\n".encode())

            conn.close()
        except Exception as e:
            os.write(2,f"[X] Status 500: Server Exception={e}\n".encode())
            error = True


if __name__ == "__main__":
    run_server()


