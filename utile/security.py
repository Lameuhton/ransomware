from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import utile.network as net
import secrets

def AES_GCM_encrypt(plain_text, DiffieHellman_key):
    # Generation du SALT
    salt = get_random_bytes(AES.block_size)

    # Generation d'une clé grâce au mot de passe
    private_key = hashlib.scrypt(
        DiffieHellman_key.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    # création d'un objet cypher servant à encrypter les données avec la méthode GCM
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # récupération du texte chiffré et d'un tag
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))

    # Retourne un dictionnaire contenant toutes les informations nécessaires
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }


def AES_GCM_decrypt(enc_dict, DiffieHellman_key):
    # decode le dictionnaire avec base64 (retour vers la forme binaire)
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])

    # Generation d'une clé grâce au mot de passe
    private_key = hashlib.scrypt(
        DiffieHellman_key.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    # réation d'un objet cypher servant à encrypter les données
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decryptage du message
    decrypted = bytes.decode(cipher.decrypt_and_verify(cipher_text, tag))

    return decrypted

def Diffie_Hellman_exchange_key(socket):

    # Chiffre publiques (Peinture commune)
    g = 9
    p = 1001

    # génération d'un chiffre aléatoire secret (peinture générée)
    secret_number = secrets.randbits(12)

    # Création d'une clé (mélange de la couleur commune + couleur générée)
    public_key = (g**secret_number) % p

    # Envoie de la clé vers le destinataire
    net.send_message(socket, public_key)

    # Reception de la clé
    dest_public_key = net.receive_message(socket)

    # Création du secret commun grâce aux clés reçues
    compute_key = (dest_public_key ** secret_number) % p
    common_secret = hashlib.sha256(str(compute_key).encode()).hexdigest()
    return common_secret
