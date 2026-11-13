# TCP Echo Server and Client

## Project overview

This project demonstrates a simple conversation between two Python programs
using TCP. A client connects to a server, sends text, and receives the same
data back as an echo. The server uses Python's built-in `socket` module; no
additional packages are required.

The project has progressed from a basic one-client demonstration in Phase 1,
to a persistent, logged server in Phase 2, and concurrent client handling in
Phase 3. This README records each phase, how the current version works, and
possible future improvements.

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

Phase 2 improved the basic echo server:

- Both programs moved to `127.0.0.1:5000`.
- The server continues listening after a client disconnects and returns to
  `accept()` to wait for another client.
- At this stage, it handled clients sequentially, one complete session at a
  time.
- The server logs when it starts listening and when a client connects, sends
  data, receives an echo, and disconnects. It also reports connection errors.
- The client waits for the echo before ending a session when the user enters
  `exit`.
- Comments in the server explain the main steps of the implementation.

### Phase 3: Concurrent client handling

The current version adds concurrent client sessions:

- The server starts a separate background thread for each accepted client.
- The main server thread immediately returns to `accept()`, so a connected
  client that is idle does not prevent other clients from connecting and
  exchanging data.
- Each handler receives and echoes data only on its own client socket, then
  closes that socket when the client disconnects.
- Logging continues to identify each client's address and connection events.

This simple thread-per-client approach is intended for a local learning
demonstration. It does not impose a maximum number of client threads.

## How the current version works

```text
Start server
    |
Create IPv4 TCP socket and bind to 127.0.0.1:5000
    |
Listen and wait in accept() (main thread)
    |
Client connects -> start a handler thread -> return to accept()
                         |
              Receive and echo data for that client
                         |
              Client disconnects -> close its socket
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

3. Enter text to see it echoed. Enter `exit` to end that client session.
   To test concurrency, open more terminals and run `python client1.py` in
   each. Keep one client connected while sending a message from another;
   each client should receive its own echo without waiting for the others.
   Press `Ctrl+C` in the server terminal to stop the server.

## Example client interaction

```text
Connected to server! Type 'exit' to quit.

Enter message: Hello!
Echo from server: Hello!
Enter message: exit
Echo from server: exit
```

## Example Phase 3 server log

Example output from two clients connected at the same time. The events from
their handler threads can appear interleaved. Timestamps and client ports vary.

```text
12:00:00 INFO Listening on 127.0.0.1:5000
12:00:05 INFO Started client handler thread for ('127.0.0.1', 51001)
12:00:05 INFO Connected: ('127.0.0.1', 51001)
12:00:06 INFO Received from ('127.0.0.1', 51001): Hello from client 1
12:00:06 INFO Echoed 19 bytes to ('127.0.0.1', 51001)
12:00:07 INFO Started client handler thread for ('127.0.0.1', 51002)
12:00:07 INFO Connected: ('127.0.0.1', 51002)
12:00:08 INFO Received from ('127.0.0.1', 51002): Hello from client 2
12:00:08 INFO Echoed 19 bytes to ('127.0.0.1', 51002)
12:00:10 INFO Disconnected: ('127.0.0.1', 51002)
12:00:12 INFO Disconnected: ('127.0.0.1', 51001)
```

## Possible future development

These are ideas for future phases; they are not implemented in the current
project:

1. **Bounded client resources:** limit active client threads or use a bounded
   worker pool to protect the server when many clients connect.
2. **More robust protocol:** define message framing and limits so larger or
   partial TCP messages are handled predictably.
3. **Graceful shutdown:** stop accepting clients and close active sessions
   cleanly when the server is stopped.
4. **Improved error handling and tests:** add automated tests for normal
   exchanges, disconnects, and network errors.
5. **Configurable settings:** allow the host, port, and log level to be set
   without editing the source code.
6. **Security for network use:** add authentication and encrypted transport
   before allowing connections beyond localhost.
