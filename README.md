# Messaging console application
An intranet messaging application for a Python Course at ECAM

## How to setup

### Windows 
Add Python to your path variable

### Linux
- Launch ServerApp.py on a machine that will serve as a server

- Launch ClientApp.py on a machine that will be a client with the command

```python ClientApp.py server_name server_port pseudo```

server_name: name of the machine that serves as a server (Ex: "DESKTOP-UPJ8DL0")
server_port: port du serveur (default: 5001)
pseudo: your pseudo (optionnal)

- If your didn't put a pseudo in the command when launching a client server, you will need to do it nowµ

- Your are now connected to the server and can talk to other online users

## Commands
### List of commands in  ClientApp.py
- /users : list of connected clients
- /join user : ask to open a session with a user (must be online)
- /accept user : accept request from a user to open a session (a new window will open)
- /exit : exit the application and disconnect from the server

### List of commands in chat
- /exit : closes the chat


## What is missing
- Port P2P is not random (hardcoded for test purposes)

- No error handling
