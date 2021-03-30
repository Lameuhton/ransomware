import sqlite3


def create_connection(path):

    connection = None
    cursor = None

    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        print("Connexion établie")

    except sqlite3.Error as e:
        print(f"Une erreur est survenue : {e}")

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
        print(f"Erreur rencontree : {e}")
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


def select(request, nom_table, condition):

    string = f"SELECT "

    if type(request) is list:
        for x in request:
            string += x + ", "
        string = string[0:-2]
    else:
        string += request

    if not (condition == " "):
        string += " FROM " + str(nom_table) + " WHERE " + condition
    else:
        string += " FROM " + str(nom_table)

    return string


# définin la liste de _victim => ajoute
#
# -- Ajouter 2 lignes de contenu sans définir de valeur pour `id`
# INSERT INTO `client` (`nom`, `email`) VALUES ('Paul', 'paul@example.com');
# INSERT INTO `client` (`nom`, `email`) VALUES ('Sandra', 'sandra@example.com');

def get_list_victims(table_name = "Victims"):

    string = f"SELECT * FROM {table_name}"

    return(string)

# garde un historique de _db

# ( pour le dernier etat => Grace au dernier etat on peut trouver le)
# datetime decroissant(order par datetime descendants 0, 1)


def get_victim_history(id_victim):

    # 'datetime' entre quote ?
    string = f"FROM Victims LEFT JOIN States ON Victims.{id_victim} = States.{id_victim} ORDER BY 'datetime' DESC"

    return(string)


# change status ? n'est plus attacable


def change_status(id_tuple, new_value):

    string = f"UPDATE states SET states = '{new_value}' WHERE id = {id_tuple} "  # Ajouter le fait que on ajoute une date dans states
    return(string)

# update

# Changer la valeur d'un tuple


def update(table_name, id_tuple, tuple_name, new_value):
    
    string = f"UPDATE {table_name} SET {tuple_name} = '{new_value}' WHERE id = {id_tuple} "

    return(string)
