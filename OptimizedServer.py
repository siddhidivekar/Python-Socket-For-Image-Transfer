# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 13:12:47 2019

@author: hoang
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 11:54:19 2019

@author: hoang

@description: This server code aims to transfer the files in fileList to client via socket

"""

import socket
from os import listdir
from re import findall
from utility import wait_for_acknowledge

"""Global Var"""
buff_size = 1024
fileList = [file for file in listdir() if findall(r'.jpg',file) != []]  #include all .jpg photos in that directory
#fileList = ['jihyo.jpg','dami.jpg','uju.jpg']   #images to be sent over to client

#initiate connection    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (socket.gethostname(), 2019)  #change here for sending to another machine in LAN
s.bind(server_addr)
s.listen(5)

client, address = s.accept()
print(f"Connection from {address} has been established!")

#Send message to client to notify about sending image
print("Server sending command: \"Start sending image.\"")
client.sendall(bytes("Start sending image." ,"utf-8"))

#wait for reply from client
print("Server is now waiting for acknowledge from client.")
ack_from_client = wait_for_acknowledge(client,"ACK")
if ack_from_client != "ACK":
    raise ValueError('Client does not acknowledge command.')

#Send message to client to notify about sending image
imgCount = len(fileList)
print("Server sends the number of images to be transfered client.")
client.sendall(bytes(str(imgCount) ,"utf-8"))

#wait for reply from client
print("Server is now waiting for acknowledge from client.")
ack_from_client = wait_for_acknowledge(client,"ACK")
if ack_from_client != "ACK":
    raise ValueError('Client does not acknowledge img count.')
    

print("Server will now send the images.",end='')
for file in fileList:
    
    img = open(file, 'rb')
    b_img = img.read()
    imgsize = len(b_img)        
    client.sendall(bytes(str(imgsize) ,"utf-8"))
    print(f"\t sending image {file} size of {imgsize}B.")
    
    print("Server is now waiting for acknowledge from client.")
    ack_from_client = wait_for_acknowledge(client,"ACK")
    if ack_from_client != "ACK":
        raise ValueError('Client does not acknowledge img size.')
    client.sendall(b_img)
    img.close()
    print(f"Image {file} sent!")
    
    print("Server is now waiting for acknowledge from client.")
    ack_from_client = wait_for_acknowledge(client,"ACK")
    if ack_from_client != "ACK":
        raise ValueError('Client does not acknowledge image transfer completion.')

 
print("All images sent.\nClosing connection.")
client.close()
