import pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import json
import os


# Connexion au serveur
# serv, gp = net.connect_to_serv()
# ----------------------------------------------------------


def lire_fichier(path_file):
    file = open(path_file, "r")
    content = file.read()
    file.close()

    return content


def choix_action():
    """
    Cette fonction, lorsqu'elle est appelée, affiche un menu et demande à l'utilisateur d'entrer le choix
    correspondant. Elle retourne un entier entre 1 et 7 qui est le choix de la personne.
    :return: int, le numéro du choix de l'utilisateur
    """

    menu = "\nGESTION DES CONFIGURATIONS\n" \
           "==========================\n" \
           "1) Charger une configuration\n" \
           "2) Afficher la configuration courante\n" \
           "3) Modifier ou ajouter un paramètre à la configuration courante\n" \
           "4) Supprime un paramètre de la configuration courante\n" \
           "5) Créer une nouvelle configuration courante\n" \
           "6) Sauvegarder la configuration courante\n" \
           "7) Quitter\n" \
           "Votre choix (de 1 à 7): "

    choix = int(input(menu))

    # Vérifie que le choix entré est bien entre 1 et 7
    while choix > 7 or choix < 1:
        print("-----------------------------------------")
        print("Veuillez entrer un chiffre entre 1 et 7!")
        print("-----------------------------------------")
        choix = int(input(menu))

    return int(choix)


def load_config(name, path="./"):
    """
    Cette fonction charge une configuration
    :param path: chemin où le fichier doit être chargé
    :param name: str, le nom du fichier de configuration qu'il faudra ouvrir
    :return: dict, contient le contenu du fichier de configuration sous forme de dictionnaire
    """

    if os.path.isfile(f"{path}{name}.cfg"):
        # Ouvre le fichier cfg correspondant, lis son contenu, le stocke et récumère l'iv
        file = open(f"{path}{name}.cfg", "rb")
        iv = file.read(16)
        content_crypted = file.read()

        if content_crypted != b"":  # Si le fichier n'est pas vide

            # Ouvre le fichier key correspondant, lis son contenu et le stocke
            file = open(f"{path}{name}.key", "rb")
            key_config = file.read()

            # Decrypte le contenu qui a été récupéré du fichier cfg avec la clé et l'iv qui ont été récupérés du
            # fichier key et config
            content_decrypted = decrypt(content_crypted, key_config, iv)

            print("\nConfiguration chargée")

        else:  # Si le fichier est vide
            content_decrypted = {}
            print("\nConfiguration chargée")
    else:
        print(
            "\n ERREUR: Ce fichier de configuration n'existe pas! "
            "Veuillez le créer (choix  5) pour pouvoir le charger.")
        content_decrypted = None

    return content_decrypted


def print_config(contenu_config):
    """
    Cette fonction sert à afficher dans la console la configuration que l'utilisateur à demandé au moyen du paramètre
    num_config.
    :param contenu_config: dict, le contenu de la configuration courante chargée
    """
    print(contenu_config)


def set_config(contenu_config, action, param, value=None):
    """
    Cette fonction sert, selon les choix de l'utilisateur, à supprimer un paramètre d'une configuraiton, modifier une
    valeur déjà présente,
    ou ajouter une valeur.
    :param contenu_config: dict, contenu de la configuration courante chargée
    :param action: l'action que l'utilisateur veut faire sur le paramètre de la config: supprimer ou ajouter/modifier
    :param param: le paramètre que l'utilisateur veut supprimer/modifier/ajouter
    :param value: si l'utilisateur veut ajouter ou modifier, la valeur par laquelle le paramètre va être changé
    """

    if action == 1:  # Si action est a 1, on ajoute/modifie dans le fichier
        contenu_config[param] = value

    elif action == 2:  # Si action est a 2, on supprime une valeur du fichier
        contenu_config.pop(param)


def create_config(name, path="./"):
    """
    Cette fonction créée un fichier de configuration et un fichier qui stockera la clé (fichiers vides)
    :param path: chemin où le fichier doit être créé
    :param name: str, le nom du fichier de configuration qu'il faudra ouvrir
    """

    # Si la suite, ajouter un paramètre type_system à la fonction
    # config = configparser.ConfigParser()
    # if type_system == 'WORKSTATION':
    #     config['VICTIM'] = {'DISKS' : [],
    #                         'PATHS' : [],
    #                         'FILE_EXT': [],
    #                         'FREQ' : '120',
    #                         'KEY' : None,
    #                         'STATE' : 'INITIALIZE'
    #                         }
    # elif type_system == 'SERVER':
    #     config['VICTIM'] = {'DISKS': [],
    #                         'PATHS': [],
    #                         'FILE_EXT': [],
    #                         'FREQ': '60',
    #                         'KEY': None,
    #                         'STATE': 'INITIALIZE'
    #                         }

    fichier1 = open(f"{path}{name}.cfg", "w")
    fichier1.write("")

    fichier2 = open(f"{path}{name}.key", "w")
    fichier2.write("")


def save_config(contenu_config, name, path='./'):
    """
    Cette fonction transformera le dictionnaire pris en paramètre (le contenu de la configuration courante)
    en foramt json, pour pouvoir le crypter et remplacer ce qu'il y a dans le fichier de configuration par ces valeurs.
    :param path: chemin où le fichier va être sauvegardé
    :param contenu_config: dict, contenu de la configuration courante chargée
    :param name: str, le nom du fichier de configuration qu'il faudra ouvrir
    """

    # Encrypte le contenu avec la fonction encrypt() et récupère le contenu, la clé et l'iv
    encrypted_content, key, iv = encrypt(contenu_config)

    # Ouvre le fichier cfg courant et remplace son contenu par, d'abord l'iv, puis le contenu crypté
    fichier = open(f"{path}{name}.cfg", "wb")
    fichier.write(iv)
    fichier.write(encrypted_content)

    # Ouvre le fichier key courant et remplace son contenu par la nouvelle clé générée en même temps que le contenu
    # chiffré
    fichier = open(f"{path}{name}.key", "wb")
    fichier.write(key)


def encrypt(contenu_config):
    # Génère une nouvelle clé random de 32 bytes
    key = get_random_bytes(32)
    # Créée un objet cipher avec la clé et le mode AES CBC (puisque l'iv n'est pas donné, il est généré aléatoirement)
    cipher = AES.new(key, AES.MODE_CBC)

    content = json.dumps(contenu_config)

    # Mets le contenu à la bonne taille avec pad, puis chiffre le contenu avec l'objet cipher
    # Le contenu chiffré est en bytes
    encrypted_content_bytes = cipher.encrypt(pad(pickle.dumps(content), AES.block_size))
    # print(encrypted_content_bytes)

    # Récupère l'iv (généré aléatoirement) de l'objet cipher et le transforme en str pour qu'il soit "lisible"
    iv = cipher.iv
    # Transforme le contenu chiffré en str (précédement en bytes)
    encrypted_content = encrypted_content_bytes
    # Ajoute l'iv au contenu chiffré (pour le déchiffrer plus tard)
    content = encrypted_content

    return content, key, iv


def decrypt(contenu_config, key, iv):
    # Récupère l'iv et le contenu, et les décode du base64

    content_crypted = contenu_config
    # print(content_crypted)

    # Crée un nouvel objet cipher avec la clé et l'iv, et décrypte le message grâce à celui-ci
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    decrypted_content = pickle.loads(unpad(cipher.decrypt(content_crypted), AES.block_size))
    # print(decrypted_content)
    # Désérialise le contenu
    content = json.loads(decrypted_content)

    # print(key)
    # decrypted_message_json = f.decrypt(contenu_config)
    # decrypted_message = json.loads(decrypted_message_json)

    return content


# ----------------------------------------------------------
def main():
    # Variable qui s'occupera de vérifier si l'utilisateur à bien fait le choix 1 avant de pouvoir faire tous les autres
    ordre_choix = False

    # Affiche une première fois le menu et stocke le choix
    num_choix = int(choix_action())
    contenu_config_courante = ''
    nom_config_courante = ''

    # Boucle tant que l'utilisateur ne choisi pas le septième choix (quitter)
    while num_choix != 7:

        if num_choix == 1:  # Lorsque l'utilisateur fait le premier choix

            ordre_choix = True
            print("\nChargement d'une configuration sur disque: ")
            print("=========================================")

            # On récupère le nom de la configuration à charger pour pouvoir savoir quel fichier cfg sera utilisé
            num_config = int(input('Entrez une configuration à charger:'
                                   '1) console contrôle'
                                   '2) serveur frontal'
                                   '3) serveur de clés'
                                   'Votre choix (1, 2 ou 3): '))

            # Vérification de l'entrée
            while num_config != 1 and num_config != 2 and num_config != 3:
                print("\nERREUR! Veuillez entrer un chiffre entre 1 et 3!\n")
                num_config = int(input('Entrez une configuration à charger:'
                                       '1) console contrôle'
                                       '2) serveur frontal'
                                       '3) serveur de clés'
                                       'Votre choix (1, 2 ou 3): '))

            # Attribution du nom de la configuration courante en fonction du choix de l'utilisateur
            if num_config == 1:
                nom_config_courante = 'console_controle'
            elif num_config == 2:
                nom_config_courante = 'serveur_frontal'
            elif num_config == 3:
                nom_config_courante = 'serveur_cles'

            # On utilise la fonction load_config qui retournera un dictionnaire avec le contenu de la configuration
            # demandée
            contenu_config_courante = load_config(nom_config_courante)

        else:

            if num_choix == 5:  # Lorsque l'utilisateur fait le cinquième choix
                nom_config_courante = input("Veuillez entrer le nom de la configuration à créer/réinitialiser: ")
                create_config(nom_config_courante)
                print("\nLa configuration courante a été créée/réinitialisée.")

            # Dans le cas où ce n'est pas le choix 1 ou 5, vérifie d'abord si le choix 1 à bien été fait avant
            # (donc qu'une configuration à bien été chargée)
            elif ordre_choix:

                if num_choix == 2:  # Lorsque l'utilisateur fait le deuxième choix
                    print("\nAffichage de la configuration courante")
                    print("======================================")
                    print_config(contenu_config_courante)

                elif num_choix == 3:  # Lorsque l'utilisateur fait le troisième choix
                    parametre1 = input("\nQuel paramètre voulez-vous modifier?: ")
                    value = input("\nQuelle valeur voulez-vous donner à ce paramètre?: ")
                    set_config(contenu_config_courante, 1, parametre1, value)
                    print("\nCe paramètre à bien été modifié.")

                elif num_choix == 4:  # Lorsque l'utilisateur fait le quatrième choix
                    parametre2 = input("\nQuel paramètre voulez-vous supprimer?: ")
                    set_config(contenu_config_courante, 2, parametre2)
                    print("\nCe paramètre à bien été supprimé.")

                elif num_choix == 6:  # Lorsque l'utilisateur fait le sixième choix
                    save_config(contenu_config_courante, nom_config_courante)
                    print("\nLa configuration courante a été sauvegardée.")

            else:  # Si l'utilisateur fait un autre choix avant même d'avoir fait le choix 1, affiche une erreur
                print("\nERREUR : Veuillez d'abord charger une configuration (choix 1)!\n")

        # Redemande l'action pour savoir si on doit quitter la boucle et quitter ou s'il faut faire autre chose
        num_choix = choix_action()

    # Ferme la fenêtre lorsque le choix est 7
    print("\nFermeture de la session.")
    exit()


if __name__ == "__main__":
    main()
