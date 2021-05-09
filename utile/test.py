import sys
import socket
from datetime import datetime
import hashlib
import psutil

for partition in psutil.disk_partitions():
    print(partition.device)