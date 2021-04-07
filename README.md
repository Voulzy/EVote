# EVote
A POC for multi-parti-computing, for e-vote.  
Scénario : 2 "compteurs", N voteurs. Each voteur send a vector to both compteur.  
One vector is random, the other is random+vote. All operations are done modulo P (with P a prime)

## Pré-Requis  
Python x >=3.8  
asyncio, time, openssl, socket (available with pip install)  

## Configuration   
run test.py (-k foor bits number of keys, -n for number of participant)  --> Output certificate (authority, compteur and participant)
  
## Run a demo  
In order to run a demo (3 voteurs) : run in three different terminal : 
* First, compteur_1.py 4
* Second, compteur_2.py 4
* Third, client.py

You'll see the votes. You can use wireshark to verify it's encrypted throught the channel (localhost for now)
