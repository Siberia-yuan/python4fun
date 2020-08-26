import socket


IP='127.0.0.1'
PORT=4002

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((IP,PORT))
# while True:
#     message=input('send:')
#     sock.send(str(message).encode(encoding="utf-8"))
#     recvMessage=sock.recv(4096)
#     print(recvMessage)
sock.send("GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n".encode(encoding="utf-8"))
recvMessage=sock.recv(4096)
print(recvMessage)
sock.close()

