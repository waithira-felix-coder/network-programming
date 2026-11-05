import socket

# Setup host and port
HOST = '127.0.0.1'
PORT = 8888

# Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server is listening...")

# Accept a client connection
conn, addr = server.accept()
print(f"Connected to client: {addr}")

while True:
    # Receive data from client
    data = conn.recv(1024)
    if not data:
        break
    
    print("Received:", data.decode())
    
    # Echo the same data back
    conn.sendall(data)

conn.close()
server.close()