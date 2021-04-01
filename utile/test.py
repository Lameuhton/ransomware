import sqlite3
connexion = sqlite3.connect("../serveur_cles/data/victims.sqlite")  #BDD dans le fichie

curseur = connexion.cursor()  #Récupération d'un curseur
list=[]

curseur.executescript("""--ajouter dans la bd--
INSERT INTO victims VALUES (1,"linux","hash","e:/","257889654123");
""")

#chercher dans la bd
#python

connexion.close()  #Déconnexion