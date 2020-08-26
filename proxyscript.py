import sys
import socket
import threading

def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server.bind((local_host,local_port))
    except:
        print('failed to listen on {0}:{1}'.format(local_host,local_port))
        sys.exit(0)
    print('listen on {0}:{1}'.format(local_host,local_port))

    server.listen(5)
    while True:
        clnt_sock,clnt_addr=server.accept()
        print('connection received from {0}:{1}'.format(clnt_addr[0],clnt_addr[1]))
        proxy_thread=threading.Thread(target=proxy_handler,args=(clnt_sock,remote_host,remote_port,receive_first))
        proxy_thread.start()

def proxy_handler(client_socket,remote_host,remote_port,receive_first):
    remote_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_sock.connect((remote_host,remote_port))

    # Pure test on proxy
    # midMessage=client_socket.recv(4096)
    # remote_sock.send(midMessage)
    # recvRemote=remote_sock.recv(4096)
    # client_socket.send(recvRemote)

    #多次recv会阻塞,掌握proxy思想，明白是怎么回事就好
    #出错失误是因为python3对python2一些地方做了部分修改

    if receive_first:
        remote_buffer=receive_from(remote_sock)
        hexdump(remote_buffer)

        remote_buffer=response_handler(remote_buffer)
        if len(remote_buffer):
            print('sending %d of bytes to client'%len(remote_buffer))
            client_socket.send(remote_buffer)
    while True:
        local_buffer=receive_from(client_socket)
        if len(local_buffer):
            print('receive %d bytes from client'%len(local_buffer))
            hexdump(local_buffer)
            local_buffer=request_handler(local_buffer)
            remote_sock.send(local_buffer)
            print('send to remote')
        remote_buffer=receive_from(remote_sock)
        if len(remote_buffer):
            print('receive %d bytes from remotebuffer'%len(local_buffer))
            hexdump(remote_buffer)
            remote_buffer=response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print('send to client')

        if not len(remote_buffer) and not len(local_buffer):
            client_socket.close()
            remote_sock.close()
            print('connection closed')
            break



def receive_from(connection):
    buffer = ''
    connection.settimeout(2)
    while True:
        data=connection.recv(4096)
        if not len(data):
            break
        buffer+=data
    print('buffer returned')
    return buffer

    #necessary modification on the buffer
    #return connection.recv(4096)


def hexdump(src, length = 16):
    result = []
    digits = 2 if isinstance(src, str) else 4
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = ' '.join(['%0*X' % (digits, ord(x)) for x in s])
        text = ''.join([x if 0x20 <= ord(x) < 0x7F else '.' for x in s])
        result.append('%04X  %-*s   %s' % (i, length*(digits + 1), hexa, text))
    for i in result:
        print(i)

def request_handler(buffer):
    # modification of request if necessary
    return buffer

def response_handler(buffer):
    # modification of response if necessary
    return buffer


def main():
    if len(sys.argv[1:])!=5:
        print('usage: python proxyscript.py [localhost] [localport] [remotehost] [remoteport] [receive_first]')
        print('example:python proxyscript.py 127.0.0.1 9000 10.12.132.1 9000 True')
        sys.exit(0)
    local_host=sys.argv[1]
    local_port=int(sys.argv[2])
    remote_host=sys.argv[3]
    remote_port=int(sys.argv[4])
    receive_first=sys.argv[5]
    if receive_first=="True":
        receive_first=True
    else:
        receive_first=False
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)


if __name__ == '__main__':
    main()

