import ssl
import socket
import struct
import pickle
HEADERSIZE=10

def send_array(sock, array):
	length = len(array)*8
	array_string=pickle.dumps(array)
	length=len(array_string)
	data=bytes(f"{len(array_string):<{HEADERSIZE}}", 'utf-8')+array_string
	sock.send(data)

def recvall(sock):
    full_msg=b''
    new_msg=True
    while new_msg:
        newbuf = sock.recv(16)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    print(buf)
    array=pickle.loads(buf)
    return array

def recv_array(sock):
    while True:
        full_msg = b''
        new_msg = True
        still_receive=True
        while still_receive:
            msg = sock.recv(16)
            if new_msg:
                print("new msg len:",msg[:HEADERSIZE])
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            print(f"full message length: {msglen}")

            full_msg += msg

            print(len(full_msg))

            if len(full_msg)-HEADERSIZE == msglen:
                still_receive=False
                print("full msg recvd")
                print(full_msg[HEADERSIZE:])
                print(pickle.loads(full_msg[HEADERSIZE:]))
                return (pickle.loads(full_msg[HEADERSIZE:]))
         
