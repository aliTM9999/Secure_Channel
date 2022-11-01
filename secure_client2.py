import socket
import threading
import hashlib
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
password = hashlib.sha256(input("Enter password: ").encode()).hexdigest()
s.connect(("127.0.0.1",12345))


name = input("Enter a username: ")

def receiveData():


    s.send(name.encode('utf-8'))

    previousTime = 0.00000000
    while True:
        try:
            
            message = s.recv(1024).decode('utf-8')

            mac = message[0:64]
            computedMac = hashlib.sha256(message[64:-18].encode()).hexdigest()
            newmac = xor_on_strings(computedMac,password)#####################################################################
            if(mac != newmac):
                print("MACs DO NOT MATCH: " + mac + " vs "+newmac)

            elif(previousTime>= float(message[-18:])):
                print("TIME PROBLEM:   previous time is "+str(previousTime)+" vs   message time "+message[-18:])
            else:

                print(message[64:-18])
                previousTime=float(message[-18:])
                
                
        except:
            #Close Connection When Error
            print("An error occured!")
            s.close()
            break

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
        
            s.send(toEncrypt.encode('utf-8'))

def xor_on_strings(string1, string2):
    return "".join(chr(ord(x)^ord(y)) for x,y in zip(string1,string2))


rec_thread = threading.Thread(target=receiveData)
rec_thread.start()

w_thread = threading.Thread(target=sendData)
w_thread.start()






