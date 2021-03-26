import numpy as np

# Set elections parameters
N_VOTERS = 2
N_CHOICE = 5
port_compteur_1_c=11636
port_compteur_1_v=11637
port_compteur_2_v=11638
# Set public parameters (we must have p prime and p > N_VOTERS)
P = 17

# Set file names for Pickle
FILEC1 = "fileC1.txt"
FILEC2 = "fileC2.txt"

def bytes_to_nparray(data: bytes):
    B = "".join(data.decode('utf-8')).split()
    if B[0] == '[':
        del(B[0])
    else:
        B[0] = B[0][1:]
    if B[len(B)-1] == '[':
        del(B[len(B)-1])
    else:
        B[len(B)-1] = B[len(B)-1][:-1] 
    A = np.array(B, dtype=int)
    return A

def sum_votes(votes):
    s = np.zeros(N_CHOICE, dtype=int)
    
    for vote in votes:
        s = s + vote
        
    for i in range(N_CHOICE):
        s[i] = s[i] % P
        
    return s
# Set ports for voters and verifiers
#VERIFS = [
#    ("localhost", 8764),
#    ("localhost", 8763)]
#VOTERS = [("localhost", 8762 - i) for i in range(N_VOTERS)]
