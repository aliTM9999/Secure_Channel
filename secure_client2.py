import socket
import threading
import hashlib
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1",12345))

password = input("Enter password: ")

concatenatedKeyToSend = password+"From client to server"
concatenatedKeyToRec = password+"From server to client"
concatenatedKeyToSendAuth = password+"Auth client to server"
concatenatedKeyToRecAuth = password+"Auth server to client"

keyToSend = hashlib.sha256(concatenatedKeyToSend.encode())
keyToRec = hashlib.sha256(concatenatedKeyToSend.encode())
keyToSendAuth = hashlib.sha256(concatenatedKeyToSendAuth.encode())
keyToRecAuth = hashlib.sha256(concatenatedKeyToRecAuth.encode())



name = input("Enter a username: ")

def receiveData():
    s.send(name.encode('utf-8'))
    while True:
        try:
            
            message = s.recv(1024).decode('utf-8')
           
            print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            s.close()
            break

def sendData():
    while True:
        msg = '{}> {}'.format(name, input(''))
        s.send(msg.encode('utf-8'))


rec_thread = threading.Thread(target=receiveData)
rec_thread.start()

w_thread = threading.Thread(target=sendData)
w_thread.start()






#socket code inspired by NeuralNine.org