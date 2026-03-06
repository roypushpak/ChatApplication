# Chat Application

A Python TCP client-server chat application with a desktop GUI, multi-client support, and ACK-based echo responses.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![TCP Sockets](https://img.shields.io/badge/Networking-TCP-success)
![GUI](https://img.shields.io/badge/Interface-Tkinter-orange)

## Overview

**Chat Application** is a computer networks project built with Python sockets and Tkinter. It includes:

- a **GUI server** that accepts multiple client connections
- a **GUI client** that lets users send messages interactively
- **TCP-only communication**
- an **ACK echo response** for every message sent by a client
- graceful connection termination when a client sends `exit`

## Features

- TCP sockets only
- Desktop GUI for both server and client
- Multiple clients can connect to the server at the same time
- Server echoes each client message back with `ACK` appended
- Each client can disconnect by sending `exit`
- Simple, interactive interface for demos and presentations

## Project Structure

```text
SocketEcho-GUI/
├── Client.py
├── Server.py
├── README.md
├── .gitignore
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
