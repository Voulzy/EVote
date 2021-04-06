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

async def handle_client(reader,writer,data1):
	global data
	
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
			if not size_bytes:
				print("Connecion end")
				break
		except BrokenPipeError:
			print("Connection end")
			break
		size=int.from_bytes(size_bytes,byteorder='big')
		print(size)
		try:
			data1= await reader.readexactly(size)
			writer.close()
			if not size_bytes:
				print('Connection terminated with {}')
				break
		except asyncio.IncompleteReadError:
			print('Connection terminated with {}')
			break
		print(data)
		data+=pickle.loads(data1)
		print(data)
#		reader.close()
		writer.close()
		break
	#	return
#async def handle_compteur(reader,writer,random,sum_vote):
#	random=protocol_async.cast_array(random)
#	writer.write(random)
#	await writer.drain()
#	try : 
#		size_bytes = await reader.readexactly(4)
#		if not size_bytes:
#			print("Connecion end")
			
#	except asyncio.IncompleteReadError:
#	print("Connection end")
#	break
#	size=int.from_bytes(size_bytes,byteorder='big')
#	print(size)
#	try:
#		data1= await reader.readexactly(size)
#		if not size_bytes:
#			print('Connection terminated with {}')
#			break
#	except asyncio.IncompleteReadError:
#		print('Connection terminated with {}')
#		break
#	print(data)
 #	sum_vote=pickle.loads(data1)
#	print(sum_vote)
#               reader.close()
 	
	
	



def receiv_client(port,context) :
	with socket.socket(socket.AF_INET,spcket.SOCK_STREAM,0) as sock:
		sock.bind(('127.0.0.1',port))
		sock.listen(10)
		with context.wrap_socket(sock, server_side=True) as ssock:
			conn, addr = ssock.accept()
	data=protocol.recv_array(conn)
	return data

def compteur_exchange(port,context,vecteur):
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
	conn=context.wrap_socket(s,server_side=False,server_hostname=hostname)
	conn.connect(('localhost',port))
	protocol.send_array(conn,vecteur)
	data = protocol.recv_array(conn)
	s.close()
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
	await asyncio.start_server(lambda r,w : handle_client(r,w,data),'127.0.0.1',port_compteur_2_v,ssl=context)
	await asyncio.sleep(10)
	context_c=ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
	context_c.load_cert_chain(crtfile,keyfile=key_file)
	context_c.load_verify_locations(cafile=cafile)
	context_c.verify_mode=ssl.CERT_REQUIRED
	vecteur_final=compteur_exchange(port_compteur_1_c,context_c,data)
	print((vecteur_final+data)%23)
#	reader,writer = await asyncio.open_connection('localhost',port_compteur_1_c,ssl=context_c)
#	writer.write(protocol_async.cast_array(random))
#	await writer.drain()
#	size_bytes= await reader.read_exactly(4)
#	size=int.from_bytes(size_bytes,byteorder='big')
#	vote_bytes= await reader.read_exactly(size)
#	print(pickle.loads(vote_bytes))
	
	
#	await asyncio.start_server(lambda r,w : handle_compteur(r,w,data),'127.0.0.1',port_compteur_1_c,ssl=context,loop=loop)
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
