import json, pickle, base64
def set_message(msg):
    """
    Cette fonction va transformer un message/dictionnaire en :
    1.      Format JSON
    2.      Chiffrer en base64 (récupérer hash, key etc ?)
    3.      Transformer en Binaire pour être prêt à être envoyé via network
    """
    # Conversion en JSON
    converted_json = json.dumps(msg)
    # encodage du fichier via pickle
    convert_bytes = pickle.dumps(converted_json)
    # encodage via base64
    encoded = base64.b64encode(convert_bytes)
    return encoded

def get_message(data):
    """
    Cette fonction va transformer un message chiffré et en binaire en
    1.      Retransformer en "str" via pickle
    2.      déchiffrer via base 64
    3.      retransformer en dictionnaire python via JSON
    """
    # Conversion d'encodé aux bytes
    decoded = base64.b64decode(data)
    # Conversion de bytes vers JSON
    to_json = pickle.loads(decoded)
    # conversion de json vers python
    to_python = json.loads(to_json)
    return to_python

x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}
