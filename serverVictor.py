import socket
import ssl
import protocol
from threading import Thread 
from socketserver import ThreadingMixIn 

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print("[+] New server socket thread started for " + ip + ":" + str(port))
        
 
    def run(self): 
        while True : 
	        data = protocol.recv_array(conn)
	        print("Server received data:", data)
	        MESSAGE = input("Multithreaded Python server : Enter Response from Server/Enter exit:")
	        if MESSAGE == 'exit':
	           break
	        conn.send(MESSAGE.encode())  # echo 
host="127.0.0.1"
port=11662
crtfile ='Voteur_1.cert'
key_file='Voteur_1.key'
cafile= 'myCA.cert'
ThreadCount = 0




context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(crtfile,keyfile=key_file)
context.load_verify_locations(cafile=cafile)
context.verify_mode=ssl.CERT_REQUIRED
compteur1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
compteur1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
try:
	compteur1.bind((host,port))
except socket.error as e:
	print(str(e))
threads = []
ssock = context.wrap_socket(compteur1, server_side=True)
while True:
	ssock.listen(5)
	(conn, (ip,port))= ssock.accept()
	newthread = ClientThread(ip,port)
	print("SSL established. Peer:{}".format(conn.getpeercert()))
	newthread.start()
	threads.append(newthread)

for t in threads:
	t.join()
		