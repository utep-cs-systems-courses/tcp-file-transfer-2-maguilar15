# TCP-File Transfer 

### Project Structure 

* **client/** 
    * ```client.py```
        * python client. 
* **client_dump/** 
    * Directory containing all files that the *client.py* can send. 
* **server/** 
    * ```server.py``` 
        * Server handling connections and saving files. 
* **server/server_dump** 
    * Directory containing all files sent through *client.py*. Essentially the file server. 
* **main.py** 
    * Terminal Prompt, for specifying file to transfer to *server.py*.  
