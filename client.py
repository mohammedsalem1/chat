import socket
import threading

IP = "127.0.0.1"
PORT = 5555
MAX_CLIENTS = 5

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    # Add new client to list
    clients.append(conn)
    
    while True:
        try:
            # Receive client message
            message = conn.recv(1024).decode("utf-8")
            
            if message == "list":
                # Send list of connected clients to the client that requested it
                conn.sendall(str(clients).encode("utf-8"))
                
            else:
                # Broadcast message to all connected clients
                for client in clients:
                    if client != conn:
                        client.sendall(message.encode("utf-8"))
                        
        except:
            # Remove disconnected client from list
            clients.remove(conn)
            print(f"[DISCONNECTION] {addr} disconnected.")
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(MAX_CLIENTS)
    
    print(f"[SERVER] listening on {IP}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

start_server()