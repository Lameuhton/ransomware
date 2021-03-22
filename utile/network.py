import socket
import ipaddress
import pickle
HEADERSIZE = 10
buffersize = 2048

def start_net_serv_client():
    # création d'un socket
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # IPv4 & TCP

    # Liaison de du socket sur l'ip 0.0.0.0 (local) et le port 8380
    s.bind(("0.0.0.0", 8380))
    
    # Permet au serveur d'attendre une connexion 
    s.listen(0)

    # accepter une connexion
    conn, addr = s.accept()
    # return:
            # conn : est un nouvel objet socket utilisable pour envoyer et recevoir des données sur la connexion
            # addr : adresse lié à l'autre socket de connexion; adresse du client
    print(f"Connected to {ipaddress.IPv4Address(addr[0])}:{addr[1]}")
    return conn


def connect_to_serv():
    # Création du socket
    socket_serv = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # IPv4 & TCP
    print(socket_serv)
    # Se connecte au serveur d'ip "localhost" avec comme port 8380
    socket_serv.connect(("localhost", 8380))
    return socket_serv


def send_message(socket_serv, string_data):
    # envoie du message en local sur le port 8380
    convert_bytes = pickle.dumps(string_data)
    convert_bytes = bytes(f"{len(convert_bytes):010d}", 'utf-8') + convert_bytes
    socket_serv.sendto(convert_bytes, ("127.0.0.1", 8380))


def receive_message(socket):
    # Attend de recevoir une donnée qui sera séparé en :
        # data : les données
        # addr: le duo addresse:port

    header_from_message, addr = socket.recvfrom(HEADERSIZE)
    data, addr = socket.recvfrom(int(header_from_message))
    unpickled = pickle.loads(data)
    return unpickled

