import socket
import ssl
import numpy as np
import protocol
from config import port_compteur_1_v, port_compteur_2_v
crtfile='Voteur_2.cert'
key_file='Voteur_2.key'
cafile='myCA.cert'

port=11662
host='localhost'
hostname_c1="Votant n 1"
hostname_c2="Votant n 3"
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
    print("SSL established. Peer:{}".format(conn.getpeercert()))
    protocol.send_array(conn,vecteur)


if __name__ == "__main__":
    # Le choix du candidat par le votant est aléatoire. Ceci pourra être changé plus tard
    # Doit être compris entre 0 et P - 1 pour ensuite pouvoir parcourir les listes
    context=ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(crtfile,keyfile=key_file)
    context.load_verify_locations(cafile=cafile)
    context.verify_mode=ssl.CERT_REQUIRED
    v1=generer_vecteur_vote(10)
    random=generer_vecteur_random(10,23)
    final_add=addition_vecteur(v1,random,23)
    print(final_add)
    send_compteur(port_compteur_1_v,final_add,context,hostname_c1)
    #send_compteur(port_compteur_2_v,-random,context,hostname_c2)

