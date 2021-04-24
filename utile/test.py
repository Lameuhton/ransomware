from utile import network as net
from utile import security as secu


socket, gp = net.connect_to_serv(adresse="192.168.126.22", port=8350)
key=secu.Diffie_Hellman_exchange_key(socket, gp)
encrypted = net.receive_message(socket)
decrypted = secu.AES_GCM_decrypt(encrypted, key)

print(decrypted)