# TCP-File Transfer 

### Requirements 

Your assignment is to write `fileClient.py` and `fileServer.py` which can transfer a file ("put localName remoteName") from a client to the server. Your programs should: 

* be in the file-transfer-lab subdir
* work with and without the proxy
* support multiple clients simultaneously using `fork()`
* gracefully deal with scenarios such as: 
    * zero length files
    * ~~user attempts to transmit a file which does not exist~~
    * ~~file already exists on the server~~
    * ~~the client or server unexpectedly disconnect~~
* optional (unless you're taking this course for grad credit): be able to request ("get") files from server

