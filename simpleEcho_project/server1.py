import logging
import socket
import threading

# Address and port where the server waits for local clients.
HOST = "127.0.0.1"
PORT = 5000
# Maximum number of bytes read from a client in each receive operation.
BUFFER_SIZE = 1024


def handle_client(connection, address):
    """Echo data for one client until it disconnects."""
    # Record that this client has started a session.
    logging.info("Connected: %s", address)

    try:
        # Keep this connection open and process messages until the client closes it.
        while True:
            data = connection.recv(BUFFER_SIZE)
            # An empty byte string means the client closed its connection.
            if not data:
                break

            # Decode a readable copy for the log; echo the original bytes unchanged.
            message = data.decode("utf-8", errors="replace")
            logging.info("Received from %s: %s", address, message)

            # Send all received bytes back to this same client.
            connection.sendall(data)
            logging.info("Echoed %d bytes to %s", len(data), address)
    except (ConnectionAbortedError, ConnectionResetError, OSError) as error:
        # Report network errors without stopping the server's accept loop.
        logging.warning("Connection error with %s: %s", address, error)
    finally:
        # Always release this client's socket and record the end of its session.
        connection.close()
        logging.info("Disconnected: %s", address)


def main():
    # Include the time, severity, and message in each log entry.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )

    # Create an IPv4 TCP socket; the with block closes it when the server exits.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Restrict access to this computer, then start accepting connections.
        server.bind((HOST, PORT))
        server.listen()
        logging.info("Listening on %s:%d", HOST, PORT)

        try:
            # Accept clients continuously and give each connection its own worker thread.
            while True:
                connection, address = server.accept()
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(connection, address),
                    daemon=True,
                )
                try:
                    client_thread.start()
                except RuntimeError:
                    connection.close()
                    raise
                logging.info("Started client handler thread for %s", address)
        except KeyboardInterrupt:
            # Let Ctrl+C stop the server with a clear log message.
            logging.info("Server stopped.")


# Run the server only when this file is started directly.
if __name__ == "__main__":
    main()
