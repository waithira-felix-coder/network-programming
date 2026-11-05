import socket
import threading
from datetime import datetime

# ============================================================
# TCP CHAT SERVER
# ============================================================

HOST = "127.0.0.1"
PORT = 5000

# Stores connected clients:
# {
#     username: socket
# }
clients = {}

# Lock protects the clients dictionary when multiple
# threads access it at the same time.
clients_lock = threading.Lock()


def timestamp():
    """Return the current time in HH:MM:SS format."""
    return datetime.now().strftime("%H:%M:%S")


def send_message(client_socket, message):
    """Send a UTF-8 message safely to a client."""
    try:
        client_socket.sendall(message.encode("utf-8"))
        return True
    except (ConnectionResetError, BrokenPipeError, OSError):
        return False


def broadcast(message, exclude_username=None):
    """
    Send a message to all connected clients.

    exclude_username can be used to prevent the sender
    from receiving their own message.
    """
    with clients_lock:
        connected_clients = list(clients.items())

    for username, client_socket in connected_clients:

        if username == exclude_username:
            continue

        if not send_message(client_socket, message):
            remove_client(username, client_socket)


def remove_client(username, client_socket):
    """Safely remove a client from the connected clients list."""

    with clients_lock:
        if clients.get(username) == client_socket:
            del clients[username]

    try:
        client_socket.close()
    except OSError:
        pass


def handle_client(client_socket, client_address):
    """Handle communication with one client."""

    username = None

    try:
        # ----------------------------------------------------
        # Request username
        # ----------------------------------------------------
        send_message(
            client_socket,
            "USERNAME_REQUIRED\n"
        )

        data = client_socket.recv(1024)

        if not data:
            return

        username = data.decode("utf-8").strip()

        # ----------------------------------------------------
        # Validate username
        # ----------------------------------------------------
        if not username:
            send_message(
                client_socket,
                "ERROR: Username cannot be empty.\n"
            )
            return

        if len(username) > 20:
            send_message(
                client_socket,
                "ERROR: Username must be 20 characters or less.\n"
            )
            return

        # ----------------------------------------------------
        # Check duplicate username
        # ----------------------------------------------------
        with clients_lock:
            if username in clients:
                send_message(
                    client_socket,
                    "ERROR: Username already in use.\n"
                )
                return

            clients[username] = client_socket

        # ----------------------------------------------------
        # Successful connection
        # ----------------------------------------------------
        print(
            f"[{timestamp()}] "
            f"{username} connected from {client_address}"
        )

        send_message(
            client_socket,
            "\n"
            "========================================\n"
            "       WELCOME TO TCP CHAT SERVER\n"
            "========================================\n"
            f"Welcome, {username}!\n"
            "Type /help to see available commands.\n"
            "========================================\n\n"
        )

        # Inform other users
        broadcast(
            f"[{timestamp()}] "
            f"Server: {username} joined the chat.\n",
            exclude_username=username
        )

        # ----------------------------------------------------
        # Main communication loop
        # ----------------------------------------------------
        while True:

            try:
                data = client_socket.recv(1024)

            except ConnectionResetError:
                print(
                    f"[{timestamp()}] "
                    f"{username} connection was reset."
                )
                break

            except OSError:
                print(
                    f"[{timestamp()}] "
                    f"Network error with {username}."
                )
                break

            # Empty data means the client disconnected
            if not data:
                break

            try:
                message = data.decode("utf-8").strip()
            except UnicodeDecodeError:
                send_message(
                    client_socket,
                    "ERROR: Message must be valid UTF-8 text.\n"
                )
                continue

            # Ignore empty messages
            if not message:
                continue

            # ------------------------------------------------
            # COMMAND: /help
            # ------------------------------------------------
            if message.lower() == "/help":

                help_message = (
                    "\n"
                    "============= AVAILABLE COMMANDS =============\n"
                    "/help   - Display available commands\n"
                    "/users  - Display connected users\n"
                    "/time   - Display server time\n"
                    "/quit   - Disconnect from the server\n"
                    "==============================================\n"
                )

                send_message(client_socket, help_message)

            # ------------------------------------------------
            # COMMAND: /users
            # ------------------------------------------------
            elif message.lower() == "/users":

                with clients_lock:
                    usernames = list(clients.keys())

                users_message = (
                    "\n"
                    "============= CONNECTED USERS =============\n"
                )

                if usernames:
                    for index, name in enumerate(usernames, start=1):
                        users_message += f"{index}. {name}\n"
                else:
                    users_message += "No users connected.\n"

                users_message += "============================================\n"

                send_message(client_socket, users_message)

            # ------------------------------------------------
            # COMMAND: /time
            # ------------------------------------------------
            elif message.lower() == "/time":

                send_message(
                    client_socket,
                    f"Server time: {timestamp()}\n"
                )

            # ------------------------------------------------
            # COMMAND: /quit
            # ------------------------------------------------
            elif message.lower() == "/quit":

                send_message(
                    client_socket,
                    "Goodbye! You have been disconnected.\n"
                )
                break

            # ------------------------------------------------
            # NORMAL CHAT MESSAGE
            # ------------------------------------------------
            else:

                formatted_message = (
                    f"[{timestamp()}] "
                    f"{username}: {message}\n"
                )

                print(formatted_message.strip())

                # Broadcast message to everyone except sender
                broadcast(
                    formatted_message,
                    exclude_username=username
                )

                # Send confirmation to sender
                send_message(
                    client_socket,
                    f"[{timestamp()}] You: {message}\n"
                )

    except UnicodeDecodeError:
        print(
            f"[{timestamp()}] Invalid data received "
            f"from {client_address}."
        )

    except OSError as error:
        print(
            f"[{timestamp()}] Network error for "
            f"{username or client_address}: {error}"
        )

    except Exception as error:
        # Last-resort protection so one client cannot
        # crash the entire server.
        print(
            f"[{timestamp()}] Unexpected error "
            f"for {username or client_address}: {error}"
        )

    finally:
        # ----------------------------------------------------
        # Clean up client connection
        # ----------------------------------------------------
        if username is not None:

            remove_client(username, client_socket)

            print(
                f"[{timestamp()}] "
                f"{username} disconnected."
            )

            broadcast(
                f"[{timestamp()}] "
                f"Server: {username} left the chat.\n"
            )

        else:
            try:
                client_socket.close()
            except OSError:
                pass


def start_server():
    """Create and start the TCP server."""

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # Allows the server to restart quickly after stopping.
    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)

        print("=" * 50)
        print("             TCP CHAT SERVER")
        print("=" * 50)
        print(f"Server address: {HOST}")
        print(f"Server port:    {PORT}")
        print("Protocol:       TCP")
        print("Status:         Listening")
        print("=" * 50)
        print("Waiting for clients...\n")

        while True:

            try:
                client_socket, client_address = server_socket.accept()

                # Create a separate thread for each client.
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )

                client_thread.start()

            except OSError as error:
                print(
                    f"[{timestamp()}] "
                    f"Error accepting client: {error}"
                )

    except OSError as error:

        if getattr(error, "errno", None) in (98, 10048):
            print(
                f"[ERROR] Port {PORT} is already in use."
            )
            print(
                "Close the program using the port or "
                "choose another port."
            )
        else:
            print(
                f"[ERROR] Could not start server: {error}"
            )

    except KeyboardInterrupt:
        print("\nServer shutting down...")

    finally:
        server_socket.close()

        # Close all connected clients.
        with clients_lock:
            connected_clients = list(clients.values())
            clients.clear()

        for client_socket in connected_clients:
            try:
                client_socket.close()
            except OSError:
                pass

        print("Server stopped.")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    start_server()