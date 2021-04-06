# EVote

rm Voteur_* piur supprimer les certificats puis rm myCA*  
For asyncio ==> Run test.py -k 2048 -n 5 (3 votants) ==> crée tous les nouveaux certificats  
Lancer dans 3 terminaux : compteur_async.py 5 (en premier) compteur_async_2.py 5, puis client_async.py  
Les threads ont était intégrer dans client_async.py     
Il reste à gérer les exceptions (brokenpipe par exemple), mais le programme marche (l'exception arrive après la lecture de la donnée)
