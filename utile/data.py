import sqlite3
connexion = sqlite3.connect("../serveur_cles/data/victims.sqlite")  #BDD dans le fichie

curseur = connexion.cursor()  #Récupération d'un curseur
list=[]

curseur.executescript("""--ajouter dans la bd--
--INSERT INTO victims(,  , , ) VALUES (,"","",":/","257889654123"); --
""")

#chercher dans la bd
#python
def recup_data_victim(numero, id=None):
    if numero ==1
    curseur.execute("SELECT * FROM enter")
    resultats = curseur.fetchall()
    for resultat in resultats:
    list.append(resultat)
    return resultat

connexion.close()  #Déconnexion
