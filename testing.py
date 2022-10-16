import socket
import threading
import hashlib
import time

mac= hashlib.sha256("Message".encode())

toEncrypt = mac.hexdigest() + "Message"

print(mac.hexdigest())
print(toEncrypt[0:64])

print(toEncrypt[64:])