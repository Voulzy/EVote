import socket
import ssl
import numpy as np
import protocol
crtfile='Voteur_2.cert'
key_file='Voteur_2.key'
cafile='myCA.cert'

port=11662
host='localhost'
hostname='Votant n°1'

context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(crtfile,keyfile=key_file)
context.load_verify_locations(cafile=cafile)
context.verify_mode=ssl.CERT_REQUIRED

s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
conn=context.wrap_socket(s,server_side=False,server_hostname=hostname)
conn.connect((host,port))
print("SSL established. Peer:{}".format(conn.getpeercert()))
x=np.zeros(10)
x[5]=1
protocol.send_array(conn,x)

