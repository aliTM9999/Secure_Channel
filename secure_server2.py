import socket
import threading
import hashlib
import time


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(("127.0.0.1", 12345))
s.listen()

print("Server running, waiting for connections")

password = input("Enter password: ")

concatenatedKeyToSend = password+"From client to server"
concatenatedKeyToRec = password+"From server to client"
concatenatedKeyToSendAuth = password+"Auth client to server"
concatenatedKeyToRecAuth = password+"Auth server to client"

keyToSend = hashlib.sha256(concatenatedKeyToSend.encode())
keyToRec = hashlib.sha256(concatenatedKeyToSend.encode())
keyToSendAuth = hashlib.sha256(concatenatedKeyToSendAuth.encode())
keyToRecAuth = hashlib.sha256(concatenatedKeyToRecAuth.encode())





connections = []
names = []

def receiveData():
    global mesCount
    while True:
        connection, addr = s.accept()
        print(str(addr)+" has connected to chatroom.")

        connections.append(connection)
        name = connection.recv(1024).decode('utf-8')
        names.append(name)
        
        messageToBroadCast = "{} has joined the room".format(name)
        mac= hashlib.sha256(messageToBroadCast.encode())

        toEncrypt = mac.hexdigest() + messageToBroadCast
        broadcast(toEncrypt,connection)
        thr = threading.Thread(target=handle, args=(connection,))
        thr.start()


def broadcast(msg, sender):
    
    for connection in connections:


        if(connection != sender):

            connection.send(msg.encode('utf-8'))

  


def handle(connection):
    while True:
        try:
            msg = connection.recv(1024)
            broadcast(msg.decode('utf-8'), connection)

        except:
            i = connections.index(connection)
            connections.remove(connection)
            connection.close()
            name = names[i]
            stringToSend = name + " has left the room"
            broadcast(stringToSend,connection)
            names.remove(name)

receiveData()


#socket code inspired by NeuralNine.org