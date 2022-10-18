import socket
import threading
import hashlib
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

#hashing
mac= hashlib.sha256("Message".encode())

toEncrypt = mac.hexdigest() + "Message"

print(mac.hexdigest())
print(toEncrypt[0:64])

print(toEncrypt[64:])

#encrypting
#salt = b'\x15\xb3@\x90\x14\xbdD\xe3\xc8P\xd8\xab\x90T\x0b\xf30\x8f\x90\xc5\x0b\xb3\xf0[\xdbqZ\x06\xcf\xb5\xa4Y'
salt = get_random_bytes(32)
key = PBKDF2("password",salt, dkLen=32)
cipher = AES.new(key, AES.MODE_CBC)
data = b'My message123456321321'

ciphertext= cipher.encrypt(pad(data, AES.block_size))
print(ciphertext)


#decrypting

cipher2 = AES.new(key, AES.MODE_CBC, cipher.iv)
plaintext =unpad(cipher2.decrypt(ciphertext), AES.block_size)
print(plaintext.decode())