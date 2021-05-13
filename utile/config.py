from utile import network as net
from utile import message as mess
import json
import glob
import os
from cryptography.fernet import Fernet


# Connexion au serveur
# serv, gp = net.connect_to_serv()
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


def load_config(name):
    """
    Cette fonction charge une configuration
    :param name: str, le nom du fichier de configuration qu'il faudra ouvrir
    :return: dict, contient le contenu du fichier de configuration sous forme de dictionnaire
    """

    if os.path.isfile(f"../configure/config/{name}.cfg"):
        # Ouvre le fichier cfg correspondant, lis son contenu et le stocke
        file = open(f"../configure/config/{name}.cfg", "r")
        content = file.read()

        if content != "": # Si le fichier n'est pas vide

            # Transforme le contenu (au format json) en dictionnaire
            content = json.loads(content)

            new_content = content.encode("UTF-8")

            # Ouvre le fichier key correspondant, lis son contenu et le stocke
            file = open(f"../configure/config/{name}.key", "rb")
            key_config = file.read()

            print("\nConfiguration chargée")

            # Decrypte le contenu qui a été récupéré du fichier cfg avec la clé qui a été récupérée du fichier key
            content_decrypted = decrypt(new_content, key_config)

        else: # Si le fichier est vide
            content_decrypted = {}
            print("\nConfiguration chargée")
    else:
        print("\n ERREUR: Ce fichier de configuration n'existe pas! Veuillez le créer (choix  5) pour pouvoir le charger.")
        content_decrypted = None


    return content_decrypted

def print_config(contenu_config):
    """
    Cette fonction sert à afficher dans la console la configuration que l'utilisateur à demandé au moyen du paramètre num_config.
    :param contenu_config: dict, le contenu de la configuration courante chargée
    """
    print(contenu_config)

def set_config(contenu_config,action,param,value=None):
    """
    Cette fonction sert, selon les choix de l'utilisateur, à supprimer un paramètre d'une configuraiton, modifier une valeur déjà présente,
    ou ajouter une valeur.
    :param contenu_config: dict, contenu de la configuration courante chargée
    :param action: l'action que l'utilisateur veut faire sur le paramètre de la config: supprimer ou ajouter/modifier
    :param param: le paramètre que l'utilisateur veut supprimer/modifier/ajouter
    :param value: si l'utilisateur veut ajouter ou modifier, la valeur par laquelle le paramètre va être changé
    """

    if action == 1: #Si action est a 1, on ajoute/modifie dans le fichier
        contenu_config[param] = value

    elif action == 2: #Si action est a 2, on supprime une valeur du fichier
        contenu_config.pop(param)

def create_config(name):
    """
    Cette fonction créée un fichier de configuration et un fichier qui stockera la clé (fichiers vides)
    :param name: str, le nom du fichier de configuration qu'il faudra ouvrir
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

    fichier1 = open(f"../configure/config/{name}.cfg", "w")
    fichier1.write("")

    generate_key(name)


def save_config(contenu_config, name):
    """
    Cette fonction transformera le dictionnaire pris en paramètre (le contenu de la configuration courante)
    en foramt json, pour pouvoir le crypter et remplacer ce qu'il y a dans le fichier de configuration par ces valeurs.
    :param contenu_config: dict, contenu de la configuration courante chargée
    :param name: str, le nom du fichier de configuration qu'il faudra ouvrir
    """

    # Transforme le dictionnaire donné en paramètre en json
    content = json.dumps(contenu_config)

    new_content = content.encode("UTF-8")

    generate_key(name)

    # Ouvre le fichier key correspondant, lis son contenu et le stocke pour récupérer la clé
    file = open(f"../configure/config/{name}.key", "rb")
    key = file.read()

    # Encrypte le contenu json
    encrypted_content = encrypt(new_content, key)

    # Ouvre le fichier cfg courant et remplace son contenu par le dictionnaire crypté
    fichier = open(f"../configure/config/{name}.cfg", "wb")
    fichier.write(encrypted_content)




def encrypt(contenu_config, key):
    encoded_content = contenu_config
    f = Fernet(key)
    encrypted_content = f.encrypt(encoded_content)

    return encrypted_content

def decrypt(contenu_config, key):
    f = Fernet(key)
    decrypted_message_json = f.decrypt(contenu_config)
    decrypted_message = json.loads(decrypted_message_json)

    return decrypted_message

def generate_key(name):
    """
    Cette fonction utilise la librairie Fernet pour générer une clé aléatoire
    qui sera la clé de déchiffrement pour les fichiers de configuration (différente pour chaque fichier),
    et la stocke dans un fichier .key créé
    :param name: le nom du fichier de configuration
    """
    key = Fernet.generate_key()
    with open(f"../configure/config/{name}.key", "wb") as key_file:
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
def main():

    # Variable qui s'occupera de vérifier si l'utilisateur à bien fait le choix 1 avant de pouvoir faire tous les autres
    ordre_choix = False

    # Affiche une première fois le menu et stocke le choix
    num_choix = int(choix_action())
    contenu_config_courante = ''
    nom_config_courante = ''

    # Boucle tant que l'utilisateur ne choisi pas le septième choix (quitter)
    while num_choix != 7:

        if num_choix == 1: # Lorsque l'utilisateur fait le premier choix

            ordre_choix = True
            print("\nChargement d'une configuration sur disque: ")
            print("=========================================")

            # On récupère le nom de la configuration à charger pour pouvoir savoir quel fichier cfg sera utilisé
            nom_config_courante = input('Entrez le nom de la configuration à charger'
                         '(stp met "console_controle", "serveur_cles" ou "serveur_frontal" bro, flemme de vérifier): ')

            # On utilise la fonction load_config qui retournera un dictionnaire avec le contenu de la configuration demandée
            contenu_config_courante = load_config(nom_config_courante)

        else:

            if num_choix == 5: # Lorsque l'utilisateur fait le cinquième choix
                nom_config_courante = input("Veuillez entrer le nom de la configuration à créer/réinitialiser: ")
                create_config(nom_config_courante)
                print("\nLa configuration courante a été créée/réinitialisée.")

            # Dans le cas où ce n'est pas le choix 1 ou 5, vérifie d'abord si le choix 1 à bien été fait avant
            # (donc qu'une configuration à bien été chargée)
            elif ordre_choix:

                if num_choix == 2: # Lorsque l'utilisateur fait le deuxième choix
                    print("\nAffichage de la configuration courante")
                    print("======================================")
                    print_config(contenu_config_courante)

                elif num_choix == 3: # Lorsque l'utilisateur fait le troisième choix
                    parametre1 = input("\nQuel paramètre voulez-vous modifier?: ")
                    value = input("\nQuelle valeur voulez-vous donner à ce paramètre?: ")
                    set_config(contenu_config_courante, 1, parametre1, value)
                    print("\nCe paramètre à bien été modifié.")

                elif num_choix == 4: # Lorsque l'utilisateur fait le quatrième choix
                    parametre2 = input("\nQuel paramètre voulez-vous supprimer?: ")
                    set_config(contenu_config_courante, 2, parametre2)
                    print("\nCe paramètre à bien été supprimé.")

                elif num_choix == 6: # Lorsque l'utilisateur fait le sixième choix
                    save_config(contenu_config_courante,nom_config_courante)
                    print("\nLa configuration courante a été sauvegardée.")

            else: # Si l'utilisateur fait un autre choix avant même d'avoir fait le choix 1, affiche une erreur
                print("\nERREUR : Veuillez d'abord charger une configuration (choix 1)!\n")

        # Redemande l'action pour savoir si on doit quitter la boucle et quitter ou s'il faut faire autre chose
        num_choix = choix_action()

    # Ferme la fenêtre lorsque le choix est 7
    print("\nFermeture de la session.")
    exit()

if __name__ == '__main__':
    main()