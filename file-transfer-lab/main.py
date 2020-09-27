#! /usr/bin/env python3

import os, sys

import fileClient

if __name__ == "__main__":

    fileDirectory = fileClient.make_file_map()
    print(f"File Directory: {fileDirectory}\n")

    while 1:
        os.write(1,"> ".encode())
        prompt = os.read(0,128).decode().strip().replace("\n","")

        parse = prompt.split()
        try:
            if "exit" in parse:
                sys.exit(1)
            if "put" not in parse:
                os.write(2, "Missing put in command \n".encode())
            else:
                fileClient.send_file(filename=parse[1])
        except ConnectionRefusedError as e:
            os.write(2,"Disconnected from server ,but client still online ;)\n".encode())
        except Exception as e:
            os.write(2,f"File does not exist. Please check client_dump directory for available files={fileDirectory}\n".encode())