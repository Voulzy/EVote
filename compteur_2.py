import socket
import ssl
import time
import protocol
from config import port_compteur_2_v, port_compteur_1_c
crtfile ='Voteur_3.cert'
key_file='Voteur_3.key'
cafile= 'myCA.cert'
hostname="Votant n 1"
port=11662

def receiv_client(port,context) :
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) as sock:
		sock.bind(('127.0.0.1',port))
		sock.listen(10)
		with context.wrap_socket(sock, server_side=True) as ssock:
			conn, addr = ssock.accept()
	data=protocol.recv_array(conn)
	return data


def compteur_exchange(port,context,vecteur):
	s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	conn=context.wrap_socket(s,server_side=False,server_hostname=hostname)
	conn.connect(('localhost',port))
	print("SSL established. Peer:{}".format(conn.getpeercert()))
	protocol.send_array(conn,vecteur)
	data=protocol.recv_array(conn)
	return data




if __name__ == "__main__":
	context_v=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
	context_v.load_cert_chain(crtfile,keyfile=key_file)
	context_v.load_verify_locations(cafile=cafile)
	context_v.verify_mode=ssl.CERT_REQUIRED
	context_c=ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
	context_c.load_cert_chain(crtfile,keyfile=key_file)
	context_c.load_verify_locations(cafile=cafile)
	context_c.verify_mode=ssl.CERT_REQUIRED
	vecteur_soustraction=receiv_client(port_compteur_2_v,context_v)
	print(vecteur_soustraction)
	time.sleep(5)
	vecteur_final=compteur_exchange(port_compteur_1_c,context_c,vecteur_soustraction)
	print((vecteur_final+vecteur_soustraction)%23)
        
