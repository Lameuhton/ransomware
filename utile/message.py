import json, pickle, base64

def set_message(msg):
    """
    Cette fonction va transformer un message/dictionnaire en :
    1.      Format JSON
    2.      Chiffrer en base64 (récupérer hash, key etc ?)
    3.      Transformer en Binaire pour être prêt à être envoyé via network
    """
    # encodage du fichier via pickle
    data_string = pickle.dumps(msg)
    pass

def get_message(data):
    """
    Cette fonction va transformer un message chiffré et en binaire en
    1.      Retransformer en "str" via pickle
    2.      déchiffrer via base 64
    3.      retransformer en dictionnaire python via JSON
    """
    # Décode le message (qui est reçu en Bytes)
    # Bytes -> String
    message = pickle.loads(data)
    pass

