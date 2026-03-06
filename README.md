# SocketEcho GUI

A Python TCP client-server chat application with a desktop GUI, multi-client support, and ACK-based echo responses.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![TCP Sockets](https://img.shields.io/badge/Networking-TCP-success)
![GUI](https://img.shields.io/badge/Interface-Tkinter-orange)

## Overview

**SocketEcho GUI** is a computer networks project built with Python sockets and Tkinter. It includes:

- a **GUI server** that accepts multiple client connections
- a **GUI client** that lets users send messages interactively
- **TCP-only communication**
- an **ACK echo response** for every message sent by a client
- graceful connection termination when a client sends `exit`

This project is well suited for:
- a **Computer Networks assignment**
- a **GitHub portfolio project**
- a beginner-friendly example of **TCP socket programming with a GUI**

## Features

- TCP sockets only
- Desktop GUI for both server and client
- Multiple clients can connect to the server at the same time
- Server echoes each client message back with `ACK` appended
- Each client can disconnect by sending `exit`
- Simple, interactive interface for demos and presentations

## Screenshots

### Server GUI

![Server GUI](assets/screenshots/server_gui_preview.png)

### Client GUI

![Client GUI](assets/screenshots/client_gui_preview.png)

### Multi-Client Demo

![Multi Client Demo](assets/screenshots/multi_client_demo.png)

## Project Structure

```text
SocketEcho-GUI/
├── Client.py
├── Server.py
├── README.md
├── .gitignore
└── assets/
    └── screenshots/
        ├── client_gui_preview.png
        ├── multi_client_demo.png
        └── server_gui_preview.png
```

## Requirements

- Python 3.x
- Tkinter

Tkinter is included with most standard Python installations.

## How to Run

### 1. Start the server

```bash
python Server.py
```

Then click **Start Server**.

### 2. Start one or more clients

```bash
python Client.py
```

Then click **Connect**.

### 3. Chat

- Type any message and click **Send**
- The server replies with the same message plus `ACK`
- Type `exit` to close that client's connection

## Example

Client sends:

```text
hello
```

Server replies:

```text
hello ACK
```

## How It Works

1. The server opens a TCP socket and listens for incoming client connections.
2. Each client connects to the server using a TCP socket.
3. The server handles multiple clients using threads.
4. When a client sends a message, the server sends the same message back with `ACK`.
5. When the client sends `exit`, the server closes that client's connection.

## Why This Project Is Good for GitHub

- clear networking concept
- visual desktop interface
- easy to run locally
- demonstrates sockets, threading, and GUI programming
- suitable for coursework and portfolio use

## Suggested Repository Settings

**Repository name**
```text
SocketEcho-GUI
```

**Short description**
```text
A Python TCP client-server chat application with a Tkinter GUI, multi-client support, and ACK-based echo responses.
```

## Demo Tips for Your GitHub Repo

- Pin this repository on your GitHub profile
- Add the screenshots in the README
- Include a short screen recording later for a stronger portfolio presentation
- Mention that the project was built for a Computer Networks course

## Author

**Roy Pushpak**

GitHub: [@roypushpak](https://github.com/roypushpak)
