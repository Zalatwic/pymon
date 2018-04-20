#kps59

import socket
import struct
import select

with open("targets.txt") as i:
    ipTargets = [line.split() for line in i]

UDP_PORT = 5005
COUNT = 0

for target in ipTargets:
    print(target[0])
    UDP_IP = socket.gethostbyname(target[0])
    PACKETDATA = '#' + format(COUNT, '04d') +  '; hello, this is a test from the case institute of technology, if you see this please report it to kps59@case.edu. this is not harmful and can be ignored. the purpose of this test is to verify that packets being returned truncate the payload from unexpected udp traffic. this is not the case with many different router configurations. if you would like to know more please contact the above with any inquiries. ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################'
    PACKETDATA = PACKETDATA.encode("utf8")

    try:
        outSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        outSock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 64)
        outSock.sendto(PACKETDATA, (UDP_IP, UDP_PORT))
        outSock.close()
        print("packet sent")
    except socket.error as x:
        print("socket error, on your side")

    #create a raw socket to read back the data
    try:
        print("attempt reception")
        inSock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        inSock.settimeout(3)
        inPacket = inSock.recv(1500)
         
        #print recieved data
        print(inPacket)
        print("revieved data:", chr(ord(inPacket[0])))

        inSock.close()
    except socket.error as x:
        print("socket error, probably timeout")

    COUNT += 1
