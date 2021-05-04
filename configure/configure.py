from utile import config
from utile import network as net
from utile import message as mess

# Connexion au serveur
serv, gp = net.connect_to_serv()
#----------------------------------------------------------

def choix_action():
    """Cette fonction, lorsqu'elle est appelée, affiche un menu et demande à l'utilisateur d'entrer le choix
    correspondant. Elle retourne un entier entre 1 et 7 qui est le choix de la personne. """

    menu = "\nGESTION DES CONFIGURATIONS\n" \
           "===================\n" \
           "1) Liste des victimes du ransomware\n" \
           "2) Historique des états\n" \
           "d'une victime\n" \
           "3) Renseigner le payement de rançon d'une victime\n" \
           "4) Quitter\n" \
           "Votre choix: "

    choix = int(input(menu))

    # Vérifie que le choix entré est bien entre 1 et 7
    while choix > 7 or choix < 1:
        print("-----------------------------------------")
        print("Veuillez entrer un chiffre entre 1 et 7!")
        print("-----------------------------------------")
        choix = int(input(menu))

    return choix



#----------------------------------------------------------
# Affiche une première fois le menu et stocke le choix
num_choix = choix_action()

# Boucle tant que l'utilisateur ne choisi pas le quatrième choix (quitter)
while num_choix != 7:

    if num_choix == 1:


    if num_choix == 2:

    if num_choix == 3:

    if num_choix == 4:

    if num_choix == 5:

    if num_choix == 6:

    # Redemande l'action pour savoir si on doit quitter la boucle et quitter ou s'il faut faire autre chose
    num_choix = choix_action()
