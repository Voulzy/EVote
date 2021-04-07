import socket
import ssl
import os
import numpy as np
import protocol
from config import port_compteur_1_v, port_compteur_2_v
import time
from threading import Thread
import os.path
crtfile='Voteur_2.cert'
key_file='Voteur_2.key'
cafile='myCA.cert'

port=11662
host='localhost'
hostname_c1="Votant n 0"
hostname_c2="Votant n 1"
def generer_vecteur_vote(taille):
    x=np.zeros(taille)

    x[np.random.randint(taille, size=1)]=1
    return x

      
def generer_vecteur_random(taille,p):
    return np.random.randint(p, size=taille)

def addition_vecteur(vecteur_1,vecteur_2,modulo):
    return (vecteur_1 + vecteur_2) % modulo

def soustraction_vecteur(vecteur_1,vecteur_2,modulo):
    return (vecteur_1 - vecteur_2) % modulo

def send_compteur(port,vecteur,context,hostname):
    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    conn=context.wrap_socket(s,server_side=False,server_hostname=hostname)
    conn.connect(('localhost',port))
    print("Connexion établie avec le comteur (adresse,port):{}".format(conn.getpeername()))
    data=protocol.cast_array(vecteur)
    conn.send(data)
    

def send_votes(crtfile,key_file):
    context=ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(crtfile,keyfile=key_file)
    context.load_verify_locations(cafile=cafile)
    context.verify_mode=ssl.CERT_REQUIRED
    v1=generer_vecteur_vote(10)
    random=generer_vecteur_random(10,23)
    final_add=soustraction_vecteur(v1,random,23)
    send_compteur(port_compteur_1_v,random,context,hostname_c1)
    print("On as envoyé le vecteur ",random)
    send_compteur(port_compteur_2_v,final_add,context,hostname_c2)
    print("On as envoyé le vecteur ",final_add)

if __name__ == "__main__":
    # Le choix du candidat par le votant est aléatoire. Ceci pourra être changé plus tard
    # Doit être compris entre 0 et P - 1 pour ensuite pouvoir parcourir les listes
#    context=ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
 #   context.load_cert_chain(crtfile,keyfile=key_file)
  #  context.load_verify_locations(cafile=cafile)
   # context.verify_mode=ssl.CERT_REQUIRED
   # v1=generer_vecteur_vote(10)
   # random=generer_vecteur_random(10,23)
   # final_add=addition_vecteur(v1,random,23)
   # print(final_add)
   # send_compteur(port_compteur_2_v,final_add,context,hostname_c2)
   # send_compteur(port_compteur_1_v,-random,context,hostname_c1)
   # time.sleep(2)
    i=0
    path=os.getcwd()
    while i < 3 : 
        print (f'Voteur_{i+2}')
        voter = Thread(target=send_votes,args=(os.path.join(path,f'Voteur_{i+2}.cert'),os.path.join(path,f'Voteur_{i+2}.key')))
        voter.start()
        voter.join()
        time.sleep(0.5)
        i+=1
        
