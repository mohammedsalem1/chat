import socket
import threading

IP = "127.0.0.1"
PORT = 5555

def receive_messages(client_socket):
    while True:  #infinite loop
        try:
            # Receive server message
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
            
        except:
            # If an error occurs, close the client socket and exit the thread
            client_socket.close()
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    
    # Start receive thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    
    while True:
        # Send message to server
        message = input()
        
        if message == "list":
            # Send request for list of connected clients to server
            client_socket.sendall(message.encode("utf-8"))
            
        else:
            # Send message to server to broadcast to all connected clients
            client_socket.sendall(message.encode("utf-8"))

start_client()