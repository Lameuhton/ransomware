import utile.network as net
import utile.message as mess

socket, gp = net.connect_to_serv(port=8381)
net.send_message(socket, mess.set_message('LIST_VICTIMS_REQ'))
print(net.receive_message(socket))



