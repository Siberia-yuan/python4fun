import socket
def get_ip_status(ip,port):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.connect((ip,port))
        print('host {0} port {1} is open'.format(ip,port))
    except Exception:
        print('host{0} port {1} is not open'.format(ip,port))
    sock.close()


if __name__ == '__main__':
    ip='10.3.9.4'
    port=53
    # for port in range(1,1024):
    #     get_ip_status(ip,port)
    get_ip_status(ip,port)
    print('scanning finished')
    
