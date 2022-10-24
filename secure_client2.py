import socket
import threading
import hashlib
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
password = hashlib.sha256(input("Enter password: ").encode()).hexdigest()
encryptor = AES.new(password[:32].encode(), AES.MODE_CBC)
s.connect(("127.0.0.1",12345))


name = input("Enter a username: ")

def receiveData():


    s.send(name.encode('utf-8'))

    previousTime = 0.00000000
    while True:
        #try:
            
            messageReceived = s.recv(1024).decode('utf-8')
            
            message = decrypt(messageReceived)

            mac = message[0:64]
            computedMac = hashlib.sha256(message[64:-18].encode()).hexdigest()
            newmac = xor_on_strings(computedMac,password)
            if(mac != newmac):
                print("MACs DO NOT MATCH: " + mac + " vs "+newmac)

            elif(previousTime>= float(message[-18:])):
                print("TIME PROBLEM:   previous time is "+str(previousTime)+" vs   message time "+message[-18:])
            else:

                print(message[64:-18])
                previousTime=float(message[-18:])
                
                
        #except:
            #Close Connection When Error
           #print("An error occured!")
            #s.close()
           #break

def sendData():
    
    while True:
        typed = input('')
        if( typed != ''):

            #have the message counter be the time
            mesCounter = time.time()
                        
            msg = '{}> {}'.format(name, typed) 

            #xor with password
            
            mac= hashlib.sha256(msg.encode()) 
            newmac = xor_on_strings(mac.hexdigest(),password)

            toEncrypt = newmac + msg + str(mesCounter).ljust(18)


            s.send(encrypt(toEncrypt).encode('utf-8'))

def xor_on_strings(string1, string2):
    return "".join(chr(ord(x)^ord(y)) for x,y in zip(string1,string2))

def encrypt(str1):

    toEncrypt = bytes(str1, 'utf-8')
    ciphertext = encryptor.encrypt(pad(toEncrypt,16))
    return str(ciphertext)

def decrypt(str1):

    decryptor = AES.new(password[:32].encode(), AES.MODE_CBC, encryptor.iv)
    plaintext = unpad(decryptor.decrypt(str1.encode()), 16)
    return plaintext.decode()





rec_thread = threading.Thread(target=receiveData)
rec_thread.start()

w_thread = threading.Thread(target=sendData)
w_thread.start()






#socket code inspired by NeuralNine.org