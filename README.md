# TCP Chat Client and Server

A Python-based TCP client-server application developed for the **Network Programming** group assignment.

## 1. Project Overview

The project demonstrates TCP socket programming by allowing multiple clients to connect to a central server, identify themselves with usernames, and exchange messages.

The server listens on:

```text
127.0.0.1:5000
```

Each connected client is handled independently using Python threads.

## 2. Features

- TCP client-server communication
- Multiple simultaneous clients
- Username identification
- Broadcast messaging
- Connection and disconnection notifications
- Message timestamps
- `/help` command
- `/users` command
- `/time` command
- `/quit` command
- Duplicate username validation
- Graceful client/server disconnection
- Network and connection error handling

## 3. Technologies

- **Python 3**
- Python `socket` module
- Python `threading` module
- TCP/IP
- IPv4

No external Python packages are required.

## 4. Project Structure

```text
tcp-chat/
│
├── server.py       # TCP server
├── client.py       # TCP client
└── README.md       # Project documentation
```

## 5. How to Run

### Step 1 — Start the server

Open Terminal 1:

```bash
python server.py
```

The server will display:

```text
Server address: 127.0.0.1
Server port:    5000
Protocol:       TCP
Status:         Listening
```

### Step 2 — Start a client

Open Terminal 2:

```bash
python client.py
```

Enter a username when prompted.

### Step 3 — Start additional clients

Open Terminal 3 or more terminals and run:

```bash
python client.py
```

Each client must use a unique username.

## 6. Available Commands

| Command | Purpose |
|---|---|
| `/help` | Display available commands |
| `/users` | Display connected users |
| `/time` | Display server time |
| `/quit` | Disconnect from the server |

Any message that is not a command is broadcast to the other connected clients.

## 7. Example

Client 1:

```text
> Hello everyone
[19:30:15] You: Hello everyone
```

Client 2 receives:

```text
[19:30:15] Felix: Hello everyone
```

Checking connected users:

```text
> /users

1. Felix
2. Brian
```

## 8. TCP Communication Model

The server follows:

```text
socket()
   ↓
bind()
   ↓
listen()
   ↓
accept()
   ↓
recv()
   ↓
send()
   ↓
close()
```

The client follows:

```text
socket()
   ↓
connect()
   ↓
send()
   ↓
recv()
   ↓
close()
```

## 9. Presentation Demonstration

During the presentation, demonstrate:

1. Start the TCP server.
2. Connect two or more clients.
3. Give each client a unique username.
4. Send messages between clients.
5. Run `/users`.
6. Run `/time`.
7. Run `/help`.
8. Disconnect a client using `/quit`.
9. Show the server's connection/disconnection logs.
10. Explain how TCP provides reliable, connection-oriented communication.

## 10. Learning Objective

The project demonstrates practical understanding of:

- TCP socket programming
- Client-server architecture
- IP addresses and ports
- TCP connections
- Concurrent client handling
- Message transmission
- Application-layer commands
- Network error handling