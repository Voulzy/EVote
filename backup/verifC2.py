import socket
from threading import Thread
import numpy as np

from config import N_VOTERS
from config import bytes_to_nparray, sum_votes

from voter import send_vote

def threaded_client(connection, votes):
    connection.send(str.encode('Welcome to the election server nº2\n'))
    while True:
        data = connection.recv(2048)
        if not data:
            break
        reply = 'Server nº2 received: ' + data.decode('utf-8')
        vote = bytes_to_nparray(data)
        votes.append(vote)
        connection.sendall(str.encode(reply))
    connection.close()

if __name__ == "__main__":

    votes = []
    
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    port = 1232
    ThreadCount = 0
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    
    print('Waiting for a voter connection...')
    ServerSocket.listen(N_VOTERS)
    
    while True:
        Client, address = ServerSocket.accept()
        print('Connected to voter at: ' + address[0] + ':' + str(address[1]))
        voter = Thread(target=threaded_client, args=(Client, votes))
        voter.start()
        ThreadCount += 1
        print('Voter number: ' + str(ThreadCount))
        voter.join()
        
        if(ThreadCount == N_VOTERS):
            print("Sum of votes received in this server: ", sum_votes(votes))
            
            # On envoie à C1 la somme des votes de C2
            send_vote(host, 1233, np.array_str(sum_votes(votes)))
            print("Results sent to checker 1")
    
    ServerSocket.close()        