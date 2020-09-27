#! /usr/bin/env python3

import os, socket

# Server Environment Variables
listenAddr = "127.0.0.1"
listenPort = 50001
path = "file-transfer-lab/server/server_dump/"
debug = False

# Global ?
defaultFilePath = os.path.join(os.getcwd(),path)


def list_files(server_file_path:str=defaultFilePath):
    os.chdir(server_file_path)
    return f"{dict(enumerate(os.listdir()))}"

def _write_to_file(fileName:str,data:str):
    try:
        filePath = defaultFilePath + fileName
        with open(filePath, "wb") as f:
            f.write(bytes(data, encoding="utf-8"))
        f.close()
    except Exception as e:
        print(f"Failed to writing to file : exception={e}, filepath = {defaultFilePath + fileName}, data={data}")


def run_server(hostname:str=listenAddr,port:int=int(listenPort)):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Standby for connection
    s.bind((hostname, port))
    # Allow 1 client connection
    s.listen(1)

    # Error Flag
    error = False

    while not error:
        try:
            # wait until incoming connection request
            conn, addr = s.accept()
            os.write(1,f"Connected by client: {addr}\n".encode())
            # Retrieve File Name
            fileName = conn.recv(1024).decode()
            print(f"File Name Present: {fileName}\n")
            while 1:
                # Accept Incoming Text
                data = conn.recv(100000).decode()
                if not data:
                    break

                # Write to remote directory
                _write_to_file(fileName=fileName,data=data)

                if debug:
                    os.write(1,f"Status 200: Received Data ({data})\n".encode())
                    os.write(1,f"Sending Data: {data}\n".encode())

            conn.close()
        except Exception as e:
            os.write(2,f"Server Exception: {e}\n".encode())
            error = True


if __name__ == "__main__":
    run_server()


