import socket

IP='www.baidu.com'
PORT=80

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((IP,PORT))

sock.send("GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n".encode(encoding="utf-8"))
recvMessage=sock.recv(4096)
print(recvMessage)
sock.close()
