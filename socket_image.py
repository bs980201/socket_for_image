# coding=UTF-8
import socket
import sys
from thread import *
import serial
import time

# ser = serial.Serial('COM11', 9600)

HOST = '172.16.1.204'   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
while 1:
    s.listen(10)
    print 'Socket now listening'
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1]) 
    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        command = conn.recv(128)
        if command == 'g':
            reply = 'bye'
            conn.sendall(reply)
            # while 1:
            #     try:
            #         print ser.readline()
            #         time.sleep(1)
            #     except ser.SerialTimeoutException:
            #         print('Data could not be read')
        elif command == 'z':
            reply = 'bye'
            conn.sendall(reply)
        if not command:
            break
    conn.close()
s.close()