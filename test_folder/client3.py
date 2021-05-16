import utile.config as config
# Lors de l'appel de cette fonction, create_config créera (dans le dossier des configurations),
# un fichier serveur_frontal.cfg vide ainsi qu'un fichier serveur_frontal.key contenant la clé pour le déchiffrer et récupérer son contenu
#name ="workstation"
#config.create_config(name)

# ______________________________________________________
# Dans le cas où tu veux lire le contenu du fichier de  (et qu'il est pas vide):

# Ouvre le fichier cfg correspondant, lis son contenu et le stocke
file = open(f"../configure/config/{'serveur'}.cfg", "rb")
content = file.read()

# Ouvre le fichier key correspondant, lis son contenu et le stocke
file = open(f"../configure/config/{'serveur'}.key", "rb")
key_config = file.read()

# Décrupte le contenu grâce à la clé, content_decrypted est un dictionnaire
content_decrypted = config.decrypt(content, key_config)

print(content_decrypted)
#________________________________________________________-

# Dans le cas où tu veux ajouter un truc dedans

#config.set_config('serveur', 1,"DISKS",['z:', 'y:'])

workstation= {'DISKS': ['z:', 'y:'],'PATHS': ['tests_1', 'tests_2'],'FILE_EXT': ['.jpg', '.png', '.txt', '.avi', '.mp4', '.mp3', '.pdf' ], 'FREQ': 120, 'KEY': None,'STATE': 'INITIALIZE'}