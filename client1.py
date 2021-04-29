import utile.network as net
import utile.message as mess


socket, gp = net.connect_to_serv()

net.send_message(socket, mess.set_message('HISTORY_REQ', [4]))
print(net.receive_message(socket), 'ehh')
