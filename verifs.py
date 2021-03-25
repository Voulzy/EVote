import asyncio
import numpy as np

from voters import Vot
from config import N_CHOICE, N_VOTERS, P

# TODO
# Pour l'instant fonctionne sans aucune connection SSL. Le vecteur Vot a été crée dans voters.py,
# mais dans la réalité il devra venir par une connexion

def receive_vote(checkID: int, voterID: int):
    # Incomplet pour l'instant
    vote_value = Vot[voterID][checkID]
    return vote_value

# Regroupe tous les votes reçus et les somme
def regroup_votes(checkID: int):
    
    voteCID = np.zeros(N_CHOICE, dtype=int)
    for voterID in range(N_VOTERS):
        voteCID = np.add(voteCID, receive_vote(checkID, voterID))
        
    return voteCID

# TODO
# On choisit C1 qui reçoit les votes de C2. Les variables voteC1 et voteC2 sont des listes qui
# contienent les vecteurs de vote brouillés

def check_vote(voteC1, voteC2):
    
    voteResults = np.zeros(N_CHOICE, dtype=int)
    for i in range(N_CHOICE):
        voteResults[i] = (voteC1[i] + voteC2[i]) % P

    return voteResults

if __name__ == "__main__":
    
    # C1 et C2 regoupent leurs votes
    voteC1 = regroup_votes(0)
    voteC2 = regroup_votes(1)
    
    # C1 et C2 additionnent leurs votes (modulo P)
    electResults = check_vote(voteC1, voteC2)
    
    # Debuggage
    print(voteC1)
    print(voteC2)
    
    print(electResults)
    
    