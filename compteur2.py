import socket
import ssl
import protocol
from config import N_CHOICE, P, port_compteur_1_c, port_compteur_2_v
import asyncio
from OpenSSL import crypto
import sys
import os
import pickle
import time
crtfile ='Voteur_1.cert'
key_file='Voteur_1.key'
cafile= 'myCA.cert'
hostname="Votant n 0"
nbVotants=int(sys.argv[1])
data=[0,0,0,0,0,0,0,0,0,0]
pubkeys = []
didvote = []
dico_a = dict()

async def handle_client(reader,writer,data1):
	global data
	pub_key_dico=''
	while True :
		pub= writer.get_extra_info('ssl_object')
		der= pub.getpeercert(binary_form=True)
		crtObj = crypto.load_certificate(crypto.FILETYPE_ASN1, der)
		pubKeyObject = crtObj.get_pubkey()
		pubKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM, pubKeyObject)
		if pubKeyString in pubkeys:
			if pubKeyString in didvote:
				print("Already voted")
				break
			else:
				print("Allowed")
				didvote.append(pubKeyString)
				pub_key_dico=pubKeyString
		else:
			print("Not allowed")
			break
		try : 
			size_bytes = await reader.readexactly(4)
		except BrokenPipeError:
			print("Connection terminer par le client")
			break
		size=int.from_bytes(size_bytes,byteorder='big')
		try:
			data1= await reader.readexactly(size)
			writer.close()
		except asyncio.IncompleteReadError:
			print('Probleme de lecture')
			break
		
		data+=pickle.loads(data1)
		dico_a[pub_key_dico]=pickle.loads(data1)
		print("On as recu : ",pickle.loads(data1))
		writer.close()
		break

	



def receiv_client(port,context) :
	with socket.socket(socket.AF_INET,spcket.SOCK_STREAM,0) as sock:
		sock.bind(('127.0.0.1',port))
		sock.listen(10)
		with context.wrap_socket(sock, server_side=True) as ssock:
			conn, addr = ssock.accept()
	data=protocol.recv_array(conn)
	return data

def compteur_exchange(port,context,vecteur,dico):
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
	conn=context.wrap_socket(s,server_side=False,server_hostname=hostname)
	conn.connect(('localhost',port))
	protocol.send_array(conn,vecteur)
	data = protocol.recv_array(conn)
	real_vote=compare_votes(data,vecteur)
	dico_sort=compare_dico(dico,real_vote)
	vecteur_votes=get_sum_votes(dico_sort)
	data=protocol.recv_array(conn)
	protocol.send_array(conn,vecteur_votes)
	s.close()
	return data,vecteur_votes

def get_public_keys(i):
	for j in range(3,i+2):
		file_path = os.path.join(os.getcwd(),'Voteur_{}.cert').format(j-1)
		f = open(file_path,'r')
		cert = f.read()
		crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
		pubKeyObject = crtObj.get_pubkey()
		pubKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM,pubKeyObject)
		pubkeys.append(pubKeyString)

def compare_votes(own,other):
	real_vote=[]
	for i in own : 
		for j in other :
			if(i==j):
				real_vote.append(i)
	return real_vote

def compare_dico(own_dico,real_vote):
	tab=[]
	for key in own_dico.keys():
		if not key in real_vote :
			tab.append(key)
	for i in tab:
		del own_dico[i]
		print("On enleve un vote")
	return own_dico
def get_sum_votes(own_dico):
	vecteur_1=[0,0,0,0,0,0,0,0,0,0]
	for valeurs in own_dico.values():
		vecteur_1+=valeurs
	return vecteur_1

def verification_vote(vecteur,dico) :
	i=sum(vecteur)
	return i==len(dico)

async def main():
	get_public_keys(nbVotants)
	context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
	context.load_cert_chain(crtfile,keyfile=key_file)
	context.load_verify_locations(cafile=cafile)
	context.verify_mode=ssl.CERT_REQUIRED
	#loop_1=asyncio.get_event_loop()
	await asyncio.start_server(lambda r,w : handle_client(r,w,data),'127.0.0.1',port_compteur_2_v,ssl=context)
	await asyncio.sleep(10)
	context_c=ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
	context_c.load_cert_chain(crtfile,keyfile=key_file)
	context_c.load_verify_locations(cafile=cafile)
	context_c.verify_mode=ssl.CERT_REQUIRED
	other_votes,own_votes=compteur_exchange(port_compteur_1_c,context,didvote,dico_a)	
	resultat=(other_votes+own_votes)%23
	if (verification_vote(resultat,dico_a)):
		print("Resultat final :")
		print(resultat)
	else : 
		print("Il y a eu une triche")

if __name__ == "__main__":
	loop=asyncio.get_event_loop()
	loop.run_until_complete(main())

