import socket
import time
import pickle
from Crypto.Util.number import getPrime
from random import randint

# CONSTANTE
HEADERSIZE = 10


def start_net_serv_client(adresse="localhost", port=8380):
    """
    Cette fonction crée un serveur socket écoutant pour une connexion
    En effet, celui ne permet que créer un serveur et d'écouter, il faudra ensuite
    ajouter une ligne de type "conn, addr = socket_serv.accept()" permettant
    d'avoir un meilleur contrôle sur le serveur.
    :param adresse: adresse sur laquelle le serveur se lie (de base localhost)
    :param port: port sur lequelle il se lie (de base 8380)
    :return: le socket du serveur
    """
    # création d'un socket
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # IPv4 & TCP

    # Liaison de du socket sur l'ip localhost (local) et le port 8380
    s.bind((adresse, port))

    # Permet au serveur d'attendre une connexion 
    s.listen(0)
    return s


def connect_to_serv(adresse="localhost", port=8380, timeout=60, secured=True):
    """
    Cette fonction crée un socket qui se connectera à un serveur
    :param timeout:
    :param adresse: l'adresse du serveur sur lequelle se connecter (de base localhost)
    :param port: port du serveur sur lequelle se connecter (de base 8380)
    :param secured: Permet de générer les nombres g et p utile pour la méthode Diffie Hellman (valeur de base True)
                    si appellé avec comme valeur None => net.connect_to_serv(secured=None) la génération sera ignorée
    :return: Si secured = True :
                                retourne son propre socket ainsi qu'un dictionnaire contenant g et p
             Si secured = None :
                                retourne son propre socket
    """
    # Création du socket
    socket_serv = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # IPv4 & TCP
    while True:
        try:
            # Se connecte au serveur avec l'ip et le port fourni
            socket_serv.connect((adresse, port))
            # Génération d'un chiffre g et un nombre premier p utile pour diffie Hellman (si secured est True)
            if secured:
                dict_g_p = [randint(9, 99), getPrime(12)]
                return socket_serv, dict_g_p
            else:
                return socket_serv

        except socket.error as e:
            print(f'[+] Impossible de se connecter. Nouvel essai dans {timeout} secondes:\n    {e}')
            # Retourne une erreur si la connexion ne fonctionne pas
            # attend X secondes avant de réassayer une connexion
            time.sleep(timeout)
            continue


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


def receive_message(conn):
    """
    Cette fonction permet de recevoir un message.
    L'entête créée dans "send_message()" permet de limiter la charge réseau
    La fonction va d'abord recevoir les 10 premiers caractères du message. Ces données indiqueront la taille du message.
    Ensuite, la fonction décide de recevoir le reste du message qui à comme longueur pile poile le nombre de caractère
    qu'il faut recevoir
    :param conn: socket du client
    :return: le message retourné en str, dictionnaire, liste, ...
    """

    # Reçoit en prioprité les 10 premiers octets étant l'entête renseignant sur la taille exacte du message
    header_from_message, addr = conn.recvfrom(HEADERSIZE)
    # Reçoit le message avec la taille exacte du message pour limiter la charge réseau
    data, addr = conn.recvfrom(int(header_from_message))

    # Remet le message dans sa forme initiale (STR, liste, dictionnaire, ...)
    unpickled = pickle.loads(data)

    return unpickled


def CloseCon(conn):
    """
    Cette fonction permet de se déconnecter de la machine distante
    :param conn: socket du client
    """
    # Bloque la communication
    conn.shutdown(1)
    # Détruit le socket
    conn.close()
