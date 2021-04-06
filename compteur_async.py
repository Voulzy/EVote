import socket
import ssl
import protocol
from config import N_CHOICE, P, port_compteur_1_c, port_compteur_1_v
import asyncio
from asn1crypto import pem, x509
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
async def handle_client(reader,writer,data1):
	global data

	print("Handle 1")
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
		else:
			print("Not allowed")
			break
		try : 
			size_bytes = await reader.readexactly(4)
			#if not size_bytes:
			#	print("Connection end")
			#	break
		except BrokenPipeError:
			print("Le client a terminé la connexion")
			break
		size=int.from_bytes(size_bytes,byteorder='big')
		print(size)
		try:
			data1= await reader.readexactly(size)
			writer.close()
			#if not size_bytes:
			#	print('Connection terminated with {}')
			#	break
		except asyncio.IncompleteReadError:
			print('Problème de lecture')
			break
		print(data)
		data+=pickle.loads(data1)
		print(data)
		break;
async def handle_compteur(reader,writer,vote1,sum_random):
	global vote	
	try : 
		size_bytes = await reader.readexactly(4)
		if not size_bytes:
			print("Connecion end")
			
	except asyncio.IncompleteReadError:
		print("Connection end")
		
	size=int.from_bytes(size_bytes,byteorder='big')
	print(size)
	try:
		data1= await reader.readexactly(size)
		if not size_bytes:
			print('Connection terminated with {}')
			
	except asyncio.IncompleteReadError:
		print('Connection terminated with {}')
		
	print(data)
	data+=pickle.loads(data1)
	print(data)
#               reader.close()
	vote=protocol_async.cast_array(vote)
	writer.write(vote_to_send)
	await writer.drain()



#def receiv_client(port,context) :
#	with socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) as sock:
#		sock.bind(('127.0.0.1',port))
#		sock.listen(10)
#		with context.wrap_socket(sock, server_side=True) as ssock:
#			conn, addr = ssock.accept()
#	data=protocol.recv_array(conn)
#	return data

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
	return data

def get_public_keys(i):
	for j in range(3,i+1):
		file_path = os.path.join(os.getcwd(),'Voteur_{}.cert').format(j-1)
		f = open(file_path,'r')
		cert = f.read()
		crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
		pubKeyObject = crtObj.get_pubkey()
		pubKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM,pubKeyObject)
		pubkeys.append(pubKeyString)

async def main():
	get_public_keys(nbVotants)
	print(pubkeys)
	context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
	context.load_cert_chain(crtfile,keyfile=key_file)
	context.load_verify_locations(cafile=cafile)
	context.verify_mode=ssl.CERT_REQUIRED
	loop_1=asyncio.get_event_loop()
	test=1
	await asyncio.start_server(lambda r,w : handle_client(r,w,data),'127.0.0.1',port_compteur_1_v,ssl=context)
	await asyncio.sleep(10)
	print(data)
	vecteur_random=compteur_exchange(port_compteur_1_c,context,data)	
	print ((data+vecteur_random)%23)
#	await asyncio.start_server(lambda r,w : handle_compteur(r,w,vote,data,),'127.0.0.1',port_compteur_1_c,ssl=context)
	#loop.run_until_complete(coroutine_2)
#	await asyncio.sleep(5)
	#server_voteur=loop.run_until_complete(coroutine_client)
#       server_compteur=loop.run_until_complete(coroutine)
	#loop.run_forever()

if __name__ == "__main__":
	#context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
	#context.load_cert_chain(crtfile,keyfile=key_file)
	#context.load_verify_locations(cafile=cafile)
	#context.verify_mode=ssl.CERT_REQUIRED
	loop=asyncio.get_event_loop()
	#test=1
	#coroutine_client = await  asyncio.start_server(lambda r,w : handle_client(r,w,test),'127.0.0.1',port_compteur_1_v,ssl=context,loop=loop)
#	coroutine_compteur = asyncio.start_server(handle_compteur,'127.0.0.1',port_compteur_1_c,ssl=context,loop=loop)
	#server_voteur=loop.run_until_complete(coroutine)
#	server_compteur=loop.run_until_complete(coroutine)
	#loop.create_task(main())
	loop.run_until_complete(main())
	#vecteur_addition=receiv_client(port_compteur_1_v,context)
	#print(vecteur_addition)
	#vecteur_soustraction=compteur_exchange(port_compteur_1_c,context,vecteur_addition)
	#print((vecteur_soustraction+vecteur_addition)%23)
#	server_context()
