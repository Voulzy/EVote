import numpy as np
import socket
from threading import Thread

from config import N_CHOICE, N_VOTERS, P
        
def send_vote(addr, port, mess):
    # Connection au vérificateur
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # On essaye de se connecter au vérificateur
    print('Waiting for connection...')
    try:
        ClientSocket.connect((addr, port))
    except socket.error as e:
        print(str(e))
    
    ClientSocket.send(mess.encode('utf-8'))
    Response = ClientSocket.recv(2048)
    print(Response.decode('utf-8'))
    
    ClientSocket.close()
    
def send_votes(addr, ports, mess):
    
    assert len(ports) == len(mess), "Erreur. Vous n'envoyez pas tous les votes ou trop de votes"
    
    # On envoie tous les votes nécessaires
    for i in range(len(ports)):
        send_vote(addr, ports[i], mess[i])
    
def vote(candID: int):
    # Set vote vector and mask vector for each voter
    V = np.zeros(N_CHOICE, dtype=int)
    M = np.random.randint(P, size=N_CHOICE)
    
    # Etape du vote
    V[candID] = 1
    
    # Etape du masque
    for i in range(N_CHOICE):
        V[i] = (V[i] - M[i]) % P
    
    # On encode pour pouvoir transmettre
    V = np.array_str(V)
    M = np.array_str(M)
    
    print(V, M)
    return (V, M)    

if __name__ == "__main__":
    
    # Set ports
    host = socket.gethostname()
    ports = (1233, 1232)
    
    # Count voters
    i = 0
    
    while i < N_VOTERS:
        Input = input('Vote for your candidate (input number from 0 to {}): '.format(N_CHOICE - 1))
        assert 0 <= int(Input) and int(Input) < N_CHOICE, "Your vote is not valid"
        
        # On effectue le vote
        votes = vote(int(Input))
        
        # On crée le thread pour le votant et on envoie les votes
        voter = Thread(target=send_votes, args=(host, ports, votes))
        voter.start()
        voter.join()
        
        # A voté
        print("Voter number {} has voted".format(i + 1))
        i += 1
        
    
    

     