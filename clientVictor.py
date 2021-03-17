import socket
import ssl
import numpy as np
import protocol
import sys
crtfile='Voteur_2.cert'
key_file='Voteur_2.key'
cafile='myCA.cert'

port=11662
host='127.0.0.1'
hostname='Votant n°1'
print('Candidat1 = [1],Candidat2 = [2],Candidat3 = [3],Candidat4 = [4],Candidat5 = [5]')
MESSAGE = input("tcpClientA: Enter message/ Enter exit:") 


context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(crtfile,keyfile=key_file)
context.load_verify_locations(cafile=cafile)
context.verify_mode=ssl.CERT_REQUIRED

s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
conn=context.wrap_socket(s,server_side=False,server_hostname=hostname)
try:
	conn.connect((host,port))
except socket.error as e:
	print(str(e))
print("SSL established. Peer:{}".format(conn.getpeercert()))
while MESSAGE != 'exit':
	conn.send(MESSAGE.encode())
	data = conn.recv(2000)
	print("received data",data)
	MESSAGE = input("Enter exit")
conn.close()

