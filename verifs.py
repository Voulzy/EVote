import asyncio
import numpy as np

import voters
from config import N_CHOICE, P

# TODO
# Recevoir V et M des votants dans receive_vote (voterID servira à identifier les threads votants)
# Ecire deux scripts différents pour chaque vérificateur ?
# Il faudra un vérficateur "chef" pour faire la somme finale

async def receive_vote(checkID: int, voterID: int) -> bool:
    # Incomplet pour l'instant
    vote_value = await voters.vote()
    
    return True

# TODO
# Choisir qui parmi C1 ou C2 va recevoir la liste de l'autre vérificateur pour les sommer

async def check_vote(voteC1, voteC2):
    voteResults = np.zeros(N_CHOICE, dtype=int)
    for i in range(N_CHOICE):
        voteResults[i] = (voteC1 + voteC2) % P
    
    return voteResults