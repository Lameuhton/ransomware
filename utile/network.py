import socket
import ipaddress


def start_net_serv_client():
    buffersize = 2048

    # create socket en UDP
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # IPv4 et TCP

    # bind socket to address and port
    s.bind(("0.0.0.0", 8380))

    s.listen(0)

    # listen for data forever and reply with moyen
    conn, addr = s.accept()
    print(f"Connected to {ipaddress.IPv4Address(addr[0])}:{addr[1]}")
    return conn, addr, buffersize

def connect_to_serv():
    # coding: utf8
    import socket

    # Variables de travail
    buffersize = 2048

    # create socket
    socket_serv = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # IPv4 et TCP

    socket_serv.connect(("localhost", 8380))
    return socket_serv, buffersize

def send_message(socket_serv):
    message = input()
    # create bytes object Str --> Bytes
    msg = str.encode(message)

    # send message
    socket_serv.sendto(msg, ("127.0.0.1", 8380))


def receive_message(socket, buffersize):
    data, addr = socket.recvfrom(buffersize)
    message = data.decode()
    if message == 'quit':
        print(f"Au-revoir")
    else:
        print(f"{message}")
