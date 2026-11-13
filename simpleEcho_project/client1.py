import socket

# Setup server connection details
HOST = '127.0.0.1'
PORT = 5000
# Create client socket and connect
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to server! Type 'exit' to quit.\n")

while True:
    message = input("Enter message: ")
    
    # Send message to server
    client.sendall(message.encode("utf-8"))

    # Receive echo back from server
    data = client.recv(1024)
    if not data:
        print("Server disconnected.")
        break
    print("Echo from server:", data.decode("utf-8", errors="replace"))

    if message.lower() == 'exit':
        break

client.close()
