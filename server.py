import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

clients = []

def handle_client(client_socket):
    username = client_socket.recv(1024).decode('utf-8')
    print(f"Username: {username} has joined the chat!")
    broadcast(f"{username} has joined the chat!", client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received message from {username}: {message}")
                broadcast(f"{username}: {message}", client_socket)
            else:
                remove_client(client_socket)
                broadcast(f"{username} has left the chat!", client_socket)
                break
        except:
            continue

def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        print(f"Connection from {client_address} has been established.")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
