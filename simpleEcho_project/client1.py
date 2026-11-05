import socket

# Setup server connection details
HOST = '127.0.0.1'
PORT = 8888

# Create client socket and connect
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to server! Type 'exit' to quit.\n")

while True:
    message = input("Enter message: ")
    
    # Send message to server
    client.sendall(message.encode())
    
    if message.lower() == 'exit':
        break
        
    # Receive echo back from server
    data = client.recv(1024)
    print("Echo from server:", data.decode())

client.close()