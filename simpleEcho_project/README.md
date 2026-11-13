# TCP Echo Server and Client

## Project overview

This project demonstrates a simple conversation between two Python programs
using TCP. A client connects to a server, sends text, and receives the same
data back as an echo. The server uses Python's built-in `socket` module; no
additional packages are required.

The work has progressed from a basic one-client demonstration in Phase 1 to a
persistent, logged server in Phase 2. This README records what each phase
achieved, how the current version works, and possible future improvements.

## Project journey

### Phase 1: Basic TCP echo

The first version established the basic client-server communication:

- The server created an IPv4 TCP socket with `AF_INET` and `SOCK_STREAM`.
- It bound to `127.0.0.1:8888` and listened for a connection.
- It accepted one client, received data, and sent the same bytes back.
- The client connected to that address, let the user enter messages, and
  displayed received echoes.

This phase proved that a client and server could exchange data over TCP. The
server handled only one client connection: after that client disconnected,
the server closed and had to be started again. The original client also
closed as soon as the user entered `exit`, without waiting to display that
message's echo.

### Phase 2: Persistent server with logging

The current version builds on Phase 1:

- Both programs now use `127.0.0.1:5000`.
- The server continues listening after a client disconnects and returns to
  `accept()` to wait for another client.
- Clients are handled sequentially, one complete session at a time; this
  version does not serve multiple clients concurrently.
- The server logs when it starts listening and when a client connects, sends
  data, receives an echo, and disconnects. It also reports connection errors.
- The client waits for the echo before ending a session when the user enters
  `exit`.
- Comments in the server explain the main steps of the implementation.

## How the current version works

```text
Start server
    |
Create IPv4 TCP socket and bind to 127.0.0.1:5000
    |
Listen and wait in accept()
    |
Client connects -> log connection
    |
Receive data -> log received text -> send the same bytes back
    |                                      |
    +---------------- repeat --------------+
    |
Client disconnects -> close client socket -> log disconnection
    |
Return to accept() and wait for the next client
```

The server binds to localhost, so it is available only from the same computer.
TCP data is not encrypted. The server logs received message text, so do not
send sensitive information through this demonstration.

## Run the current version

1. Open a terminal in this folder and start the server:

   ```powershell
   python server1.py
   ```

2. Open another terminal in this folder and start the client:

   ```powershell
   python client1.py
   ```

3. Enter text to see it echoed. Enter `exit` to end the client session. Start
   `python client1.py` again to connect another client. Press `Ctrl+C` in the
   server terminal to stop the server.

## Example client interaction

```text
Connected to server! Type 'exit' to quit.

Enter message: Hello!
Echo from server: Hello!
Enter message: exit
Echo from server: exit
```

## Example Phase 2 server log

Example output from two clients handled in sequence. Timestamps and client
ports vary between runs.

```text
05:33:44 INFO Listening on 127.0.0.1:5000
05:33:44 INFO Connected: ('127.0.0.1', 64251)
05:33:44 INFO Received from ('127.0.0.1', 64251): First session
05:33:44 INFO Echoed 13 bytes to ('127.0.0.1', 64251)
05:33:44 INFO Received from ('127.0.0.1', 64251): exit
05:33:44 INFO Echoed 4 bytes to ('127.0.0.1', 64251)
05:33:44 INFO Disconnected: ('127.0.0.1', 64251)
05:33:45 INFO Connected: ('127.0.0.1', 64252)
05:33:45 INFO Received from ('127.0.0.1', 64252): Second session
05:33:45 INFO Echoed 14 bytes to ('127.0.0.1', 64252)
05:33:45 INFO Received from ('127.0.0.1', 64252): exit
05:33:45 INFO Echoed 4 bytes to ('127.0.0.1', 64252)
05:33:45 INFO Disconnected: ('127.0.0.1', 64252)
```

## Possible future development

These are ideas for future phases; they are not implemented in the current
project:

1. **Concurrent clients:** handle multiple client sessions at the same time
   with threads or asynchronous I/O.
2. **More robust protocol:** define message framing and limits so larger or
   partial TCP messages are handled predictably.
3. **Improved error handling and tests:** add automated tests for normal
   exchanges, disconnects, and network errors.
4. **Configurable settings:** allow the host, port, and log level to be set
   without editing the source code.
5. **Security for network use:** add authentication and encrypted transport
   before allowing connections beyond localhost.
