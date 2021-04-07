import numpy as np
import random
import concurrent.futures

from config import N_CHOICE, N_VOTERS, P

def vote(candID: int):
    # Set vote vector and mask vector for each voter
    V = np.zeros(N_CHOICE, dtype=int)
    M = np.random.randint(P, size=N_CHOICE)
    
    # Etape du vote
    V[candID] = 1
    print(V)
    
    # Etape du masque
    for i in range(N_CHOICE):
        V[i] = (V[i] - M[i]) % P
      
    
    return (V, M)    
    
#if __name__ == "__main__":
    # Le choix du candidat par le votant est aléatoire. Ceci pourra être changé plus tard
    # Doit être compris entre 0 et P - 1 pour ensuite pouvoir parcourir les listes
C = [(random.randint(1, N_CHOICE) - 1) for i in range(N_VOTERS)]
    
Vot = []

# J'ai utilisé cette librairie car elle permet de récupérer la valeur retournée par le thread

for i in range(N_VOTERS):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        v = executor.submit(vote, C[i])
        Vot.append(v.result())
    



    
     