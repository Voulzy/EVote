import socket
import ssl
import numpy as np
import protocol
import sys
from config import N_CHOICE, P


def createVote(vote):
	V=np.zeros(N_CHOICE, dtype=int)
	V[int(vote)]=1
	M = np.random.randint(P, size=N_CHOICE)
	for i in range(N_CHOICE):
		V[i] = (V[i] - M[i])%P
	return (V,M)


def sendVote(i):
	crtfile='Voteur_{}.cert'.format(i)
	key_file='Voteur_{}.key'.format(i)
	cafile='myCA.cert'
	port1=11662
	port2=11555
	host='127.0.0.1'
	compteur1='Votant n°1'
	compteur2='Compteur n°2'
	print('Candidat1 = [1],Candidat2 = [2],Candidat3 = [3],Candidat4 = [4],Candidat5 = [5]')
	MESSAGE = input("tcpClientA: Enter message/ Enter exit:") 


	context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
	context.load_cert_chain(crtfile,keyfile=key_file)
	context.load_verify_locations(cafile=cafile)
	context.verify_mode=ssl.CERT_REQUIRED

	s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	so= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	conn=context.wrap_socket(s,server_side=False,server_hostname=compteur1)
	con=context.wrap_socket(so,server_side=False,server_hostname=compteur2)
	try:
		conn.connect((host,port1))
		con.connect((host,port2))
	except socket.error as e:
		print(str(e))
	print("SSL established. Peer:{}".format(conn.getpeercert()))
	while MESSAGE != 'exit':
		(vote,masque) = createVote(MESSAGE)
		protocol.send_array(conn,vote)   #ENVOI A COMPTEUR 1 
		protocol.send_array(con,masque)  # ENVOI A COMPTEUR 2
		data = conn.recv(2000)
		dat = con.recv(2000)
		print("received data compteur1",data)
		print("received data compteur2",dat)
		MESSAGE = input("Enter exit")
	conn.close()

if __name__ == '__main__':
	sendVote(1)
