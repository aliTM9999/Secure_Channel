import socket
import threading
import hashlib
import time


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
password = hashlib.sha256(input("Enter password: ").encode()).hexdigest()
s.bind(("127.0.0.1", 12345))
s.listen()

print("Server running, waiting for connections")


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
        newmac = xor_on_strings(mac.hexdigest(),password)
        timecounter = time.time()
        
        toEncrypt = newmac + messageToBroadCast + str(timecounter).ljust(18)
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

            timecounter = time.time()

            mac= hashlib.sha256(stringToSend.encode())
            newmac = xor_on_strings(mac.hexdigest(),password)

            toEncrypt = newmac + stringToSend+ str(timecounter).ljust(18)
            broadcast(toEncrypt,connection)
            names.remove(name)

def xor_on_strings(string1, string2):
    return "".join(chr(ord(x)^ord(y)) for x,y in zip(string1,string2))


receiveData()


#socket code inspired by NeuralNine.org