import numpy as np
import random
from threading import Thread

from config import N_CHOICE, P

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
      
    print(V, M)
    # return (V, M)    
    
if __name__ == "__main__":
    # Le choix du candidat par le votant est aléatoire. Ceci pourra être changé plus tard
    # Doit être compris entre 0 et P - 1 pour ensuite pouvoir parcourir les listes
    choice = random.randint(1, N_CHOICE) - 1
    
    v = Thread(target=vote, args=(choice, ))
    v.start()
    v.join()
    
     