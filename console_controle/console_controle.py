import sqlite3
#from ..utile import network
from ..utile import data
#from ..utile import message

# NOTE
#___________________________________________
# La fonction "data.recup_data_victime" serait la fonction que Gaetan fera dans le module Data pour me retourner les infos des victimes à l'aide de requêtes SQL.
# J'ai imaginé qu'e cette fonction aurait 2 paramètres, le premier "choix", et le deuxième "id_victime" et celui-ci serait à None par défaut si sa valeur n'est pas fournie lors de l'appel de la fonction.
# Le paramètre "choix" aurait soit la valeur 1, soit la valeur 2 lorsque j'appelle la fonction
# Si la valeur est a 1, la fonction devra me renvoyer exactement ce qu'il me faut à afficher pour le choix 1, si elle est a 2, je fournirai alors une valeur au paramètre "id_victime"
#___________________________________________

def choix_action():
    #Cette fonction, lorsqu'elle est appelée, affiche un menu et demande à l'utilisateur d'entrer le choix correspondant.
    #Elle retourne un entier entre 1 et 4 qui est le choix de la personne.

    menu = "CONSOLE DE CONTRÔLE\n===================\n1) Liste des victimes du ransomware\n2) Historique des états d'une victime\n3) Renseigner le payement de rançon d'une victime\n4) Quitter\nVotre choix: "
    choix = int(input(menu))

    #Vérifie que le choix entré est bien entre 1 et 4
    while choix > 4 or choix < 1:
        print("-----------------------------------------")
        print("Veuillez entrer un chiffre entre 1 et 4!")
        print("-----------------------------------------")
        choix = int(input(menu))

    return choix

def afficher_liste_victime(new_data_victimes):

    print("LISTING DES VICTIMES DU RANSOMWARE")
    print("___________________________________")
    print("num  id             type        disques        statut     nb. de fichiers")

    #Affichage des victimes avec un format + ajout d'un numéro pour chaque victime
    form = "{0:5}{1:15}{2:12}{3:15}{4:11}{5:30}"
    for i, val in enumerate(new_data_victimes):
        val.insert(0, str(i + 1))
        print(form.format(*val))

    return

def afficher_historique_victime(new_data_victimes):

    #Demande du numéro de la victime
    nb_victime = len(new_data_victimes)
    num_victime = int(input(f"Entrez le numéro de la victime (entre 1 et : {nb_victime}"))

    #Vérification de l'input de l'utilisateur
    while 1 > num_victime > nb_victime:
        print(f"Erreur: veuillez entrer un nombre entre 1 et {nb_victime}")
        num_victime = int(input(f"Entrez le numéro de la victime (entre 1 et : {nb_victime}"))

    #Récupération de l'id de la victime grâce au num que l'utilisateur à entré
    for i in new_data_victimes:
        if i[0] == str(num_victime):
            id_victime = int(i[1])

    #Appel de la fonction qui retournera les infos de la victime précise grâce à l'id
    data_victimes = data.recup_data_victime(2,id_victime)

    print("HISTORIQUE DES ETATS D'UNE VICTIME")
    print("___________________________________")


    form = "{0:11}{1:9} - {2:14} - {3:20}"
    for val in data_victimes:
        print(form.format(*val))

    return

def afficher_rancon_victime():
    print(" j'ai affiché les rancons des victimes")
    return


data_victimes = None

#Affiche une première fois le menu et stocke le choix
num_choix = choix_action()

#Boucle tant que l'utilisateur ne choisi pas le quatrième choix (quitter)
while num_choix != 4:

    #Premier choix:
    if num_choix == 1:
        #Appelle la fonction qui ira récupérer les infos des victimes dans la bdd
        data_victimes = data.recup_data_victime(1)
        # A partir de data_victimes, création d'une nouvelle liste de listes (et plus de tuple) avec les infos des victimes
        new_data_victimes = []
        for val in data_victimes:
            new_data_victimes.append(list(val))

        afficher_liste_victime(new_data_victimes)

    #Deuxième choix, ne s'affiche QUE si l'utilisateur a déjà fait le choix 1 avant, sinon affiche une erreur:
    elif num_choix == 2:
        if data_victimes != None:
            afficher_historique_victime(new_data_victimes)
        else:
            print("\nERREUR : Veuillez d'abord lister les victimes!\n")

    #Troisième choix:
    elif num_choix == 3:
        afficher_rancon_victime()

    num_choix = choix_action()


exit()



