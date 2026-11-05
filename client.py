import socket
import threading

# ============================================================
# TCP CHAT CLIENT
# ============================================================

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client_socket):
    """
    Continuously receive messages from the server.

    This runs in a separate thread so the client can
    receive messages while the user is typing.
    """

    while True:

        try:
            data = client_socket.recv(4096)

            if not data:
                print("\n[SERVER] Connection closed.")
                break

            message = data.decode("utf-8")

            # Username negotiation happens before chat begins.
            if message.strip() == "USERNAME_REQUIRED":
                continue

            print(message, end="")

        except ConnectionResetError:
            print("\n[ERROR] Server reset the connection.")
            break

        except ConnectionAbortedError:
            print("\n[ERROR] Connection was aborted.")
            break

        except UnicodeDecodeError:
            print("\n[ERROR] Received invalid data from server.")
            continue

        except OSError:
            print("\n[ERROR] Connection to server lost.")
            break

    print("\nDisconnected from server.")


def start_client():

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        # ----------------------------------------------------
        # Connect to server
        # ----------------------------------------------------
        print("=" * 50)
        print("              TCP CHAT CLIENT")
        print("=" * 50)
        print(f"Server: {HOST}")
        print(f"Port:   {PORT}")
        print("=" * 50)

        try:
            client_socket.connect((HOST, PORT))

        except ConnectionRefusedError:
            print("\n[ERROR] Could not connect to the server.")
            print(
                "Make sure server.py is running "
                "before starting the client."
            )
            return

        except TimeoutError:
            print("\n[ERROR] Connection timed out.")
            return

        except OSError as error:
            print(f"\n[ERROR] Network error: {error}")
            return

        print("Connected to server.\n")

        # ----------------------------------------------------
        # Receive username request
        # ----------------------------------------------------
        try:
            response = client_socket.recv(1024)

        except OSError as error:
            print(f"[ERROR] Could not communicate with server: {error}")
            return

        if not response:
            print("[ERROR] Server closed the connection.")
            return

        # ----------------------------------------------------
        # Request username
        # ----------------------------------------------------
        while True:

            username = input("Enter your username: ").strip()

            if not username:
                print("Username cannot be empty.")
                continue

            if len(username) > 20:
                print("Username must be 20 characters or less.")
                continue

            break

        client_socket.sendall(
            username.encode("utf-8")
        )

        # ----------------------------------------------------
        # Receive welcome message
        # ----------------------------------------------------
        welcome = client_socket.recv(4096)

        if not welcome:
            print("[ERROR] Server closed the connection.")
            return

        welcome_message = welcome.decode("utf-8")

        if welcome_message.startswith("ERROR:"):
            print(welcome_message)
            return

        print(welcome_message)

        # ----------------------------------------------------
        # Start receiving thread
        # ----------------------------------------------------
        receive_thread = threading.Thread(
            target=receive_messages,
            args=(client_socket,),
            daemon=True
        )

        receive_thread.start()

        # ----------------------------------------------------
        # Main user input loop
        # ----------------------------------------------------
        while True:

            try:
                message = input("> ").strip()

            except (KeyboardInterrupt, EOFError):
                print("\nDisconnecting...")
                break

            if not message:
                continue

            try:
                client_socket.sendall(
                    message.encode("utf-8")
                )

            except (BrokenPipeError, ConnectionResetError):
                print("\n[ERROR] Server connection was lost.")
                break

            except OSError as error:
                print(f"\n[ERROR] Failed to send message: {error}")
                break

            if message.lower() == "/quit":
                break

    except KeyboardInterrupt:
        print("\nClient interrupted.")

    except UnicodeEncodeError:
        print("\n[ERROR] Message contains unsupported characters.")

    except OSError as error:
        print(f"\n[ERROR] Client error: {error}")

    finally:

        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        try:
            client_socket.close()
        except OSError:
            pass

        print("Client closed.")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    start_client()