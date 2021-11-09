import socket
import json
import threading

# CONSTANTS
SERVER_IP_ADDRESS = socket.gethostbyname("")
SERVER_PORT = 5050
SERVER_ADDRESS = (SERVER_IP_ADDRESS, SERVER_PORT)
BUFFER_SIZE = 4096
FORMAT = "utf8"

# GLOBALS
clients = set()
clients_lock = threading.Lock()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def setup():
    try:
        server.bind(SERVER_ADDRESS)
        print("bind complete")
    except Exception:
        print("Couldn't get server ip address")

def broadcastMessages(message, connection):
    for client in clients:
        if connection != client:
            client.sendall(bytes(message, FORMAT))
            print("sendin' messages to client")

def handleClient(connection):
    try:
        connected = True
        while connected:
            message = connection.recv(BUFFER_SIZE).decode(FORMAT)
            if not message:
                break
            print("received message")
            broadcastMessages(message, connection)
    finally:
        with clients_lock:
            clients.remove(connection)
        connection.close()

def startAClientThread(connection):
    client_thread = threading.Thread(target=handleClient, args=(connection,))
    client_thread.start()
    print("started")

def acceptConnections():
    print("Listening for connections")
    while True:
        client_connection, client_address = server.accept()
        with clients_lock:
            clients.add(client_connection)
        print("staring new thread for new connection")
        startAClientThread(client_connection)

def closeServer():
    server.close()

def start():
    setup()
    print("Started Server - 200")
    server.listen()
    acceptConnections()


start()