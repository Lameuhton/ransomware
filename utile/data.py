import sqlite3


def connect_to_DB(path="../serveur_cles/data/victims.sqlite"):
    '''
    :param path:chemin vers l'endroit où se trouve la bd
    :return:retourne la connexion et le curseur pour exécuter les commande sql
    '''
    connection = None
    cursor = None

    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        print("Connexion établie")

    except sqlite3.Error as e:
        print(f"Une erreur est survenue dans la connexion: {e}")

    return connection, cursor



def insert(table, value,conn = None, cursor= None):
    '''
    :param table:table dans laquelle il faut ajouter des valeurs
    :param value:valeur à ajouter dans la table
    :return:la commande sql insert
    '''
    query = f"INSERT INTO {table} ("

    for x in value:
        query += x+", "
    query = query[0:-2]+") VALUES ("

    for x in value:
        query += str(value[x])+", "
    query = query[0:-2]+")"

    if conn and cursor:
        result = execute_query(conn, cursor)
        return result

    else:
        return query



def update(table_name, tuple_name, new_value, id_tuple=None, conn = None, cursor= None):
    '''
    cette fonction creer une requête de type update avec ou sans condition
    :param table_name:nom table à mettre à jour
    :param tuple_name:nom tuple à mettre à jour
    :param new_value:nouvelle valeur pour le(s) tuple(s)
    :param id_tuple:id utilisé dans la condition
    :return:
    '''
    if id_tuple:
        query = f"UPDATE {table_name} SET {tuple_name} = '{new_value}' WHERE id = {id_tuple} "

    else:
        query = f"UPDATE {table_name} SET {tuple_name} = '{new_value}'"

    if conn and cursor:
        result = execute_query(conn, cursor)
        return result

    else:
        return query



def select(request, nom_table, condition=None, conn = None, cursor= None):
    '''
    cette fonction s'occupe de creer une requête sql qui return un string si conn et cursor si ne sont pas renseigné
    pour l'utiliser plus tard ou l'executer directement si le conn et cursor sont renseigné
    :param request:si request est une liste, il va séparer les éléments correctement (si[os,hash]--> select os, hash from...)
    :param nom_table:nom de la table à selectionner (from victims....)
    :param condition:renseigne la condition WHERE si non renseigné --> ignoré
    :return: si con et cursor renseigné: execution la commande sql
                                  sinon: retourne la commande sql en string
    '''

    query = f"SELECT "

    if type(request) is list:
        for x in request:
            query += x + ", "
        query = query[0:-2]
    else:
        query += request

    if condition:
        query += " FROM " + str(nom_table) + " WHERE " + condition
    else:
        query += " FROM " + str(nom_table)
    if conn and cursor:
        result = execute_query(conn, cursor)
        return result

    else:
        return query




def get_victim_history(id_victim=None,conn = None, cursor= None):
    '''
    cette fonction construit une commande sql qui demande l'historique des changements d'état d'une victime du ransomware.
    :param id_victim:renseigne l'id de la victim dont on veut l'historique
    :return:l'historique de la victime
    '''
    query = f"FROM Victims LEFT JOIN States ON Victims.{id_victim} = States.{id_victim} ORDER BY 'datetime' DESC"
    if conn and cursor:
        result = execute_query(conn, cursor)
        return result

    else:
        return query


def execute_query(connection, cursor, query):
    '''
    cette fonction execute les commandes sql
    :param connection:bjet sqlite relative à la connection de la bd (carte d'identité)
    :param cursor:afin d'exécuter nos requêtes, nous allons utiliser le cursor recupéré en faisant appel à la fonction:
    connection = sqlite3.connect(path)
    :param query:est la commande sql à executer
    :return:si con et cursor renseigné: execution la commande sql
                                 sinon: retourne la commande sql en string
    '''
    result = None
    try:
        cursor.execute(query)  # execute la commande sql
        connection.commit()

        if (query[0:6] == "SELECT"):  # detecte si c'est un "select"
            result = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"Erreur survenue dans l'execution de la requête: {e}")

    return result


def disconnect_from_DB(connection):
    '''
    cette fonction s'occupe de déconnecter la bd
    :param connection: objet sqlite relative à la connection de la bd (carte d'identité)
    '''
    try:
        connection.close()
        print('Déconnexion éffectuée')

    except sqlite3.Error as e:
        print(f"Une erreur est survenue dans la déconnexion: {e}")#detecte l'erreur à la deconnection