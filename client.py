import utile.network as net
import utile.message as message

socket, gp = net.connect_to_serv()
net.send_message(socket, message.set_message('CHANGE_STATE', ['4', ['DECRYPT']]))

while True:
    data = net.receive_message(socket)
    print(data)