import socket
import ipaddress
import pickle
from Cryptodome.Util.number import getPrime
from random import randint

HEADERSIZE = 10


def start_net_serv_client(adresse="localhost", port=8380):
    """
    Cette fonction crée un serveur socket écoutant pour une connexion
    :param adresse: adresse sur laquelle le serveur se lie (de base localhost)
    :param port: port sur lequelle il se lie (de base 8380)
    :return: le socket du destinataire // est un nouvel objet socket utilisable pour envoyer et recevoir des
            données sur la connexion
    """
    # création d'un socket
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # IPv4 & TCP

    # Liaison de du socket sur l'ip localhost (local) et le port 8380
    s.bind((adresse, port))

    # Permet au serveur d'attendre une connexion 
    s.listen(0)

    # accepter une connexion et reçoit le socket ainsi que l'adresse du destinataire
    conn, addr = s.accept()
    print(f"Connected to {ipaddress.IPv4Address(addr[0])}:{addr[1]}")
    return conn


def connect_to_serv(adresse="localhost", port=8380, secured=True):
    """
    Cette fonction crée un socket qui se connectera à un serveur
    :param adresse: l'adresse du serveur sur lequelle se connecter (de base localhost)
    :param port: port du serveur sur lequelle se connecter (de base 8380)
    :param secured: Permet de générer les nombres g et p utile pour la méthode Diffie Hellman (valeur de base True)
                    si appellé avec comme valeur None => net.connect_to_serv(secured=None) la génération sera ignorée
    :return: Si secured = True :
                                retourne son propre socket ainsi qu'un dictionnaire contenant g et p
             Si secured = None :
                                retourne son propre socket
    """
    try:
        # Création du socket
        socket_serv = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # IPv4 & TCP

        # Se connecte au serveur d'ip "localhost" avec comme port 8380
        socket_serv.connect((adresse, port))

         # Génération d'un chiffre g et un nombre premier p
        if secured:
            dict_g_p = [randint(9, 99), getPrime(12)]
            return socket_serv, dict_g_p
        else:
            return socket_serv

    except socket.error as e:
        print(f'[+] Impossible de se connecter :\n    {e}') # Retourne une erreur si la connexion ne fonctionne pas
        return None, None


def send_message(socket_serv, string_data, adresse="127.0.0.1", port=8380):
    """
    Cette fonction permet de convertir un message en binaire via le module pickle puis d'envoyer celui ci vers un autre
    socket.
    Une fois le message transformé, il va rajouter une entête de 10 octet permettant de connaitre la taille du message
    message envoyé dans le format b'0000000026\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bstring_data\x94.'
    :param socket_serv: socket du client
    :param string_data: données à envoyer (str, list, dictionnaire) à transformer en bytes
    :param adresse: adresse sur laquelle envoyer le message
    :param port: port sur lequelle envoyer le message
    """
    convert_bytes = pickle.dumps(string_data)  # Transforme le message en binaire

    # Ajoute une entête de 10 octets renseignant sur la taille du message
    convert_bytes = bytes(f"{len(convert_bytes):010d}", 'utf-8') + convert_bytes

    # Envoi du message
    socket_serv.sendto(convert_bytes, (adresse, port))


def receive_message(socket):
    """
    Cette fonction permet de recevoir un message.
    L'entête créée dans "send_message()" permet de limiter la charge réseau
    La fonction va d'abord recevoir les 10 premiers caractères du message. Ces données indiqueront la taille du message.
    Ensuite, la fonction décide de recevoir le reste du message qui à comme longueur pile poile le nombre de caractère
    qu'il faut recevoir
    :param socket: socket du client
    :return: le message retourné en str, dictionnaire, liste, ...
    """

    # Reçoit en prioprité les 10 premiers octets étant l'entête renseignant sur la taille exacte du message
    header_from_message, addr = socket.recvfrom(HEADERSIZE)

    # Reçoit le message avec la taille exacte du message pour limiter la charge réseau
    data, addr = socket.recvfrom(int(header_from_message))

    # Remet le message dans sa forme initiale (STR, liste, dictionnaire, ...)
    unpickled = pickle.loads(data)

    return unpickled
