import numpy as np
import socket

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
    portC1 = 1233
    portC2 = 1232
    
    # Count voters
    i = 0
    
    while i < N_VOTERS:
        Input = input('Vote for your candidate (input number from 0 to {}): '.format(N_CHOICE - 1))
        assert 0 <= int(Input) and int(Input) < N_CHOICE, "Your vote is not valid"
        
        # On effectue le vote
        vote1, vote2 = vote(int(Input))
        
        # On envoie le vote masqué à C1
        send_vote(host, portC1, vote1)
        
        # On envoie le vote masqué à C2
        send_vote(host, portC2, vote2)
        
        # A voté
        print("Voter number {} has voted".format(i + 1))
        i += 1
        
    
    

     