import socket
from threading import Thread

from config import N_VOTERS
from config import bytes_to_nparray, sum_votes

def threaded_client(connection, votes):
    connection.send(str.encode('Welcome to the election server nº1\n'))
    while True:
        data = connection.recv(2048)
        if not data:
            break
        reply = 'Server nº1 received: ' + data.decode('utf-8')
        vote = bytes_to_nparray(data)
        votes.append(vote)
        connection.sendall(str.encode(reply))
    connection.close()

if __name__ == "__main__":
    
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    port = 1233
    ThreadCount = 0
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    
    print('Waiting for a voter connection...')
    ServerSocket.listen(N_VOTERS)

    # Set the list where votes are saved
    votes = []

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
            
            # On reçoit les votes de C2 et on fait la somme pour avoir le résultat
            Results = [sum_votes(votes)]
            Checker, address = ServerSocket.accept()
            print('Connected to checker 2 at: ' + address[0] + ':' + str(address[1]))
            checker = Thread(target=threaded_client, args=(Checker, Results))
            checker.start()
            checker.join()
            print("Elections results: ", sum_votes(Results))
        
    ServerSocket.close()
    
    
        
        