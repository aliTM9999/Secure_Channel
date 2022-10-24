import socket
import threading
import hashlib
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
def xor_on_strings(string1, string2):
    return "".join(chr(ord(x)^ord(y)) for x,y in zip(string1,string2))
#hashing
mac= hashlib.sha256("Message".encode())
time1= time.time()
print(time1)

toEncrypt = mac.hexdigest() + str(time1) + "Message"

print(mac.hexdigest())
print(toEncrypt[0:64])

print(toEncrypt[64:82])

#encrypting
#salt = b'\x15\xb3@\x90\x14\xbdD\xe3\xc8P\xd8\xab\x90T\x0b\xf30\x8f\x90\xc5\x0b\xb3\xf0[\xdbqZ\x06\xcf\xb5\xa4Y'
salt = get_random_bytes(32)
key = PBKDF2("password",salt, dkLen=32)
cipher = AES.new(key, AES.MODE_CBC)
data = b'ali has joined the room'


password = "dad"

messageToBroadCast = "{} has joined the room".format('ali')
mac= hashlib.sha256(messageToBroadCast.encode())
#newmac = xor_on_strings(mac.hexdigest(),password)
timecounter = time.time()
        
toEncrypt = mac.hexdigest() + messageToBroadCast + str(timecounter).ljust(18)
ciphertext= cipher.encrypt(pad(toEncrypt.encode(), 16))
print("cipher "+str(ciphertext))


#decrypting

cipher2 = AES.new(key, AES.MODE_CBC, cipher.iv)
plaintext =unpad(cipher2.decrypt(ciphertext), 16)
print(plaintext.decode())


print(time.time())

message = "2f77668a9dfbf8d5848b9eeb4a7145ca94c6ed9236e4a773f6dcafa5132b2f91HEYITSMETABARNAK1666487655.3067904"

if(1666489999.00000> float(message[-18:])):
    print("error")




