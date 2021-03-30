import sqlite3


def connect_to_DB(path="../serveur_cles/data/victims.sqlite"):

    connection = None
    cursor = None

    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        print("Connexion établie")

    except sqlite3.Error as e:
        print(f"Une erreur est survenue dans la connexion: {e}")

    return connection, cursor

# a = create_connection(path)
# execute_query (create_connection(path), "Select * from victims")


def execute_query(connection, cursor, query):
    result = None
    try:
        cursor.execute(query)
        connection.commit()
        print('[SQL]La requete a ete executee')

        if (query[0:6] == "SELECT"):
            print('[SQL]Requete SELECT OK')
            result = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"Erreur survenue dans l'execution de la requête: {e}")
        
    return result


# ajoute des valeurs dans _db
def insert(nom_table, value):
    # Insert into victim (value)
    string = f"INSERT INTO {nom_table} ("

    for x in value:                        # ici on récupère le nom de la value
        string += x+", "                   #
    string = string[0:-2]+") VALUES ("     #

    for x in value:
        string += str(value[x])+", "
    string = string[0:-2]+")"

    return string

# fait un selct dans _db


def select(request, nom_table, condition=None):

    string = f"SELECT "

    if type(request) is list:
        for x in request:
            string += x + ", "
        string = string[0:-2]
    else:
        string += request

    if condition:
        string += " FROM " + str(nom_table) + " WHERE " + condition
    else:
        string += " FROM " + str(nom_table)

    return string


# définin la liste de _victim => ajoute
#
# -- Ajouter 2 lignes de contenu sans définir de valeur pour `id`
# INSERT INTO `client` (`nom`, `email`) VALUES ('Paul', 'paul@example.com');
# INSERT INTO `client` (`nom`, `email`) VALUES ('Sandra', 'sandra@example.com');


# garde un historique de _db

# ( pour le dernier etat => Grace au dernier etat on peut trouver le)
# datetime decroissant(order par datetime descendants 0, 1)


def get_victim_history(id_victim):

    # 'datetime' entre quote ?
    string = f"FROM Victims LEFT JOIN States ON Victims.{id_victim} = States.{id_victim} ORDER BY 'datetime' DESC"

    return string

# update

# Changer la valeur d'un tuple


def update(table_name, tuple_name, new_value, id_tuple=None):

    if id_tuple:
        string = f"UPDATE {table_name} SET {tuple_name} = '{new_value}' WHERE id = {id_tuple} "

    else:
        string = f"UPDATE {table_name} SET {tuple_name} = '{new_value}'"

    return string


def disconnect_from_DB(connection):
    try:
        connection.close()  # Déconnexion
        print('Déconnexion éffectuée')

    except sqlite3.Error as e:
        print(f"Une erreur est survenue dans la déconnexion: {e}")