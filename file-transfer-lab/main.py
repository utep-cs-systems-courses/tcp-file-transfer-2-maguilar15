#! /usr/bin/env python3

import os, sys

import fileClient

from lib.params import parseParams

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50000"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


paramMap = parseParams(switchesVarDefaults)

server, usage = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()


if __name__ == "__main__":

    fileDirectory = fileClient.make_file_map()
    os.write(1,f"File Directory: {fileDirectory}\n".encode())

    while 1:
        # Shell Prompt
        os.write(1,"tcp > ".encode())
        prompt = os.read(0,128).decode().strip().replace("\n","")
        # Parsing String
        parse = prompt.split()
        # Input Sanitization
        try:
            if "exit" in parse:
                os.write(2,"Exiting tcp file transfer prompt\n".encode())
                sys.exit(1)
            elif "ls" in parse:
                os.write(2,f"{fileDirectory}\n".encode())
            elif "put" not in parse:
                os.write(2, f"Missing put in command. Format: `put localFileName remoteFileName`\n".encode())
            elif "put" in parse and len(parse) <= 1:
                os.write(2,f"Follow the format: `put localFileName remoteFileName`\nPlease type a filename available from the client_dump directory: directory={fileDirectory}\n".encode())
            elif "put" in parse and len(parse) <= 2:
                os.write(2,f"Follow the format: `put localFileName remoteFileName`\nPlease specify name to store file remotely on the server\n".encode())
            else:
                fileClient.send_file(serverAddress=server,filenameHostMachine=parse[1],filenameRemoteMachine=parse[2])

        except ConnectionRefusedError:
            os.write(2, f"Disconnected from server, but client still online ;)\n".encode())
        except Exception as e:
            os.write(2,f"File does not exist. Please check client_dump directory for available files={fileDirectory}, exception={e}\n".encode())