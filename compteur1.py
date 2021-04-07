import socket
import ssl
import protocol
from config import N_CHOICE, P, port_compteur_1_c, port_compteur_1_v
import asyncio
import pickle
from OpenSSL import crypto
import sys
import time
import os
crtfile ='Voteur_0.cert'
key_file='Voteur_0.key'
nbVotants=int(sys.argv[1])
cafile= 'myCA.cert'
data=[0,0,0,0,0,0,0,0,0,0]
vote=[]
pubkeys = []
didvote = []
dico_a = {}

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
			print("Le client a terminé la connexion")
			break
		size=int.from_bytes(size_bytes,byteorder='big')
		try:
			data1= await reader.readexactly(size)
			writer.close()
		except asyncio.IncompleteReadError:
			print('Problème de lecture')
			break
		dico_a[pub_key_dico]=pickle.loads(data1)
		print("On as recu : ",pickle.loads(data1))
		break;

def compteur_exchange(port,context,vecteur):
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) as sock:
		sock.bind(('127.0.0.1',port))
		sock.listen(10)
		with context.wrap_socket(sock, server_side=True) as ssock:
			conn, addr = ssock.accept()
	data=protocol.recv_array(conn)
	protocol.send_array(conn,vecteur)
	time.sleep(1)
	conn.close()
	sock.close()
	return data

def get_public_keys(i):
	for j in range(3,i+2):
		file_path = os.path.join(os.getcwd(),'Voteur_{}.cert').format(j-1)
		f = open(file_path,'r')
		cert = f.read()
		crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
		pubKeyObject = crtObj.get_pubkey()
		pubKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM,pubKeyObject)
		pubkeys.append(pubKeyString)

def compare_dico(own_dico,other_dico):
	tab=[]
	for key in other_dico.keys():
		if not key in own_dico :
			tab.append(key)
	for i in tab:
		del other_dico[i]
		print("On enleve un vote")
	tab=[]
	for key in own_dico.keys():
		if not key in other_dico :
			tab.append(key)
	for i in tab:
		print("On enleve un vote")
		del own_dico[i]
	return own_dico, other_dico

def comptage_vote(own_dico,other_dico):
	vecteur_1=[0,0,0,0,0,0,0,0,0,0]
	vecteur_2=[0,0,0,0,0,0,0,0,0,0]
	for valeurs in own_dico.values():
		vecteur_1+=valeurs
	for valeurs in other_dico.values():
		vecteur_2+=valeurs
	return (vecteur_1+vecteur_2)%23

async def main():
	get_public_keys(nbVotants)
	context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
	context.load_cert_chain(crtfile,keyfile=key_file)
	context.load_verify_locations(cafile=cafile)
	context.verify_mode=ssl.CERT_REQUIRED
	loop_1=asyncio.get_event_loop()
	test=1
	await asyncio.start_server(lambda r,w : handle_client(r,w,data),'127.0.0.1',port_compteur_1_v,ssl=context)
	await asyncio.sleep(10)
	vecteur_random=compteur_exchange(port_compteur_1_c,context,dico_a)	
	dico, other_dico = compare_dico(dico_a,vecteur_random)
	print("Resultat final :")
	print(comptage_vote(dico,other_dico))


if __name__ == "__main__":
	loop=asyncio.get_event_loop()
	loop.run_until_complete(main())

