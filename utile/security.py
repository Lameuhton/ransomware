from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.number import getRandomInteger
import utile.network as net


def AES_GCM_encrypt(plain_text, DiffieHellman_key):
    """
    Cette fonction chiffre les données via la méthode AES-256 GCM
    :param plain_text: texte, dictionnaire, liste à chiffrer
    :param DiffieHellman_key: mot de passe utilisé pour chiffrer la donnée.
           (Se nomme DiffieHellman_key car ici le mot de passe utilsé sera un hash généré par cette fonction)
    :return: un dictionnaire contenant le cipher texte, salt, nonce et tag
    """
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
    """
    Cette fonction déchiffre les données via la méthode AES-256 GCM
    :param enc_dict: Dictionnaire contenant le cipher texte, salt, nonce et tag
            Si c'est généré par la fonction AES_GCM_encrypt de ce module pas de soucis.
            Sinon il faut mettre les données sous cette forme :
                {'cipher_text': 'xxxxx','salt': 'xxxxx','nonce': 'xxxxx','tag': 'xxxxx'}
    :param DiffieHellman_key: Mot de passe utilisé pour déchiffrer la donnée.
                      (Se nomme DiffieHellman_key car ici le mot de passe utilsé sera un hash généré par cette fonction)
    :return: retourne la donné dans son état initial (STR, liste, dictionnaire, ...)
    """
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


def Diffie_Hellman_exchange_key(socket, g_and_p=None):
    """
    Cette fonction permet de s'envoyer un mot de passe secret via un canal non sécurisé.
    Grâce à de multiples calculs et envois sur le réseau, les données calculées auront le même résultat dans les deux
    programmes mais pas à la vue d'une personne malveillante qui écouterait sur le réseau (wireshark?)

    :param socket: socket du client
    :param g_and_p:   liste contenant g et p
                    - Valeur de base = None
                        si None: s'attend à recevoir les données g et p. Si timeout de 10s arrêt de la fonction
                        Si g_and_p est donné: envoi g et p au destinataire
    :return: Si timeout: None
            Sinon: le secret commun sous forme d'un hash 256
    """
    # Si  g et p ont été envoyés
    if g_and_p:
        # envoi g et p vers le destinataire
        net.send_message(socket, g_and_p)
        # décompose g et p pour les utiliser dans le code
        g, p = g_and_p

    # Si g et p n'ont pas été envoyés
    else:
        # tentative de recevoir le message
        try:
            socket.settimeout(10)
            g, p = net.receive_message(socket)
        # Si rien reçu au bout de 10 secondes : retourne un message d'erreur et renvoi None

        except:
            print(f'[+] Aucunes valeurs de g et p ont été trouvées au bout de 10 secondes\n')
            return None

    # génération d'un chiffre aléatoire secret (peinture générée)
    secret_number = getRandomInteger(12)

    # Création d'une clé (mélange de la couleur commune + couleur générée)
    public_key = (g ** secret_number) % p

    # Envoie de la clé vers le destinataire
    net.send_message(socket, public_key)

    # Reception de la clé
    dest_public_key = net.receive_message(socket)

    # Création du secret commun grâce aux clés reçues
    compute_key = (dest_public_key ** secret_number) % p

    common_secret = hashlib.sha256(str(compute_key).encode()).hexdigest()
    return common_secret
