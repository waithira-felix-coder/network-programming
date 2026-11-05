# TCP Echo Client and Server

This demonstration uses Python's built-in `socket` module; no packages need to
be installed. The server binds to `127.0.0.1` on port `6789`, a development
port in the requested range. Binding to localhost keeps the demo available
only on this computer. The server handles multiple clients at the same time,
with a separate connection for each client.

## Client privacy

Each client receives only the messages sent on its own connection; the server
does not forward one client's messages to another client or print message
contents in its logs. This is connection isolation, not encryption. The demo
uses plain TCP and is intended for localhost development, not sending sensitive
information over a network.

## Run the demonstration

1. Open a terminal in this folder and start the server:

   ```powershell
   python server.py
   ```

2. Open a second terminal in the same folder and start a client:

   ```powershell
   python client.py
   ```

3. Open additional terminals and run `python client.py` in each one. Type a
   message in any client to see its own echo. Type `quit` to end that client;
   press `Ctrl+C` in the server terminal to stop the server.

Example client output:

```text
Connected to 127.0.0.1:6789. Enter 'quit' to exit.
Message: Hello, server!
Echo: Hello, server!
```
