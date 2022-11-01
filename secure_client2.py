import socket
import threading
import hashlib

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1",12345))

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






