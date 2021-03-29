import utile.network as net
import utile.message as message
import utile.data as data

socket=net.start_net_serv_client()

while True:
    recv_data = net.receive_message(socket)

    message_type = message.get_message_type(recv_data)

    if message_type == 'LIST_REQ':
        pass

    elif message_type == 'VICTIM':
        pass

    elif message_type == 'LIST_END':
        pass

    elif message_type == 'HIST_REQ':
        pass

    elif message_type == 'HIST_RESP':
        pass

    elif message_type == 'HIST_END':
        pass

    elif message_type == 'CHGSTATE':
        pass

