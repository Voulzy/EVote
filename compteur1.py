import socket
import ssl
import protocol
from config import N_CHOICE, P, port_compteur_1_c, port_compteur_1_v
crtfile ='Voteur_1.cert'
key_file='Voteur_1.key'
cafile= 'myCA.cert'



def receiv_client(port,context) :
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) as sock:
		sock.bind(('127.0.0.1',port))
		sock.listen(10)
		with context.wrap_socket(sock, server_side=True) as ssock:
			conn, addr = ssock.accept()
	data=protocol.recv_array(conn)
	return data

def compteur_exchange(port,context,vecteur):
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) as sock:
		sock.bind(('127.0.0.1',port))
		sock.listen(10)
		with context.wrap_socket(sock, server_side=True) as ssock:
			conn, addr = ssock.accept()
	data=protocol.recv_array(conn)
	protocol.send_array(conn,vecteur)
	return data
if __name__ == "__main__":
	context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
	context.load_cert_chain(crtfile,keyfile=key_file)
	context.load_verify_locations(cafile=cafile)
	context.verify_mode=ssl.CERT_REQUIRED
	vecteur_addition=receiv_client(port_compteur_1_v,context)
	print(vecteur_addition)
	vecteur_soustraction=compteur_exchange(port_compteur_1_c,context,vecteur_addition)
	print((vecteur_soustraction+vecteur_addition)%23)
