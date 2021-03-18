import socket
import ipaddress
import pickle

buffersize = 2048

def start_net_serv_client():
    # création d'un socket
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # IPv4 & TCP
    print(s)

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
    return conn, addr, buffersize

def connect_to_serv():
    # Création du socket
    socket_serv = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # IPv4 & TCP
    print(socket_serv)
    # Se connecte au serveur d'ip "localhost" avec comme port 8380
    socket_serv.connect(("localhost", 8380))
    return socket_serv, buffersize

def send_message(socket_serv, msg):
    # encodage du fichier via pickle
    data_string = pickle.dumps(msg)
    # envoie du message en local sur le port 8380
    socket_serv.sendto(data_string, ("127.0.0.1", 8380))


def receive_message(socket, buffersize):

    # Attend de recevoir une donnée qui sera séparé en :
        # data : les données
        # addr: le duo addresse:port
    data, addr = socket.recvfrom(buffersize)

    # Décode le message (qui est reçu en Bytes)
        # Bytes -> String
    message = pickle.loads(data)

    # Partie du code servant à quitter le serveur / le client
    # (sera peut-être enlevé en fonction des problèmes / besoins)
    return message

