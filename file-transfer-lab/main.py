#! /usr/bin/env python3

import os, sys

import fileClient


if __name__ == "__main__":

    fileDirectory = fileClient.make_file_map()
    print(f"File Directory: {fileDirectory}\n")

    while 1:
        # Shell Prompt
        os.write(1,"tcp > ".encode())
        prompt = os.read(0,128).decode().strip().replace("\n","")
        # Parsing String
        parse = prompt.split()
        try:
            if parse is None:
                os.write(2,f"Please follow the format: put filename".encode())
            elif "exit" in parse:
                sys.exit(1)
            elif "put" not in parse:
                os.write(2, f"Missing put in command \n".encode())
            elif "put" in parse and len(parse) <= 1:
                os.write(2,f"Please type a filename available from the client_dump directory: directory={fileDirectory}\n".encode())
            else:
                fileClient.send_file(filename=parse[1])
        except ConnectionRefusedError as e:
            os.write(2,f"Disconnected from server ,but client still online ;)\n".encode())
        except Exception as e:
            os.write(2,f"File does not exist. Please check client_dump directory for available files={fileDirectory}\n".encode())