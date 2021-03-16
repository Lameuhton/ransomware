

list_victim_req = { 'LIST_REQ': None }

list_victim_resp = {
    'VICTIM': 'id',
    'HASH': 'hash' ,
    'OS': 'type',
    'DISKS': 'disks',
    'STATE': 'state',
    'NB_FILES': 'nb_files'
}

list_victim_end = { 'LIST_END': None }

history_req = {
    'HIST_REQ': 'id'
}

history_resp = {
    'HIST_RESP': 'id',
    'TIMESTAMP': 'timestamp',
    'STATE': 'state',
    'NB_FILES': 'nb_files'
}

history_end = {
    'HIST_END': id
}
