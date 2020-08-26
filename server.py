import socket
import threading

def serve(clntSock):
    while True:
        messageFromclnt=clntSock.recv(10)
        print(messageFromclnt)
        #clntSock.send("ack".encode(encoding="utf-8"))
        clntSock.send(messageFromclnt)

def main():
    IP='127.0.0.1'
    PORT=4001
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((IP,PORT))
    server.listen(5)
    while True:
        clntSock,clntAddr=server.accept()
        print("Accept\nIp:{0} Port:{1}".format(clntAddr[0],clntAddr[1]))
        threadInstance=threading.Thread(target=serve,args=(clntSock,))
        threadInstance.start()


if __name__ == '__main__':
    main()