#kps59

import socket
import struct
import select
import time
import sys

with open("targets.txt") as i:
    ipTargets = [line.split() for line in i]

UDP_PORT = 5005
COUNT = 0

rttList = list()    # list to hold the amount of time it takes between sending and recieving the packet
hopList = list()    # list to hold the amount of hops
amtList = list()    # list to hold the amount of bytes 

# adds an element to each fooList on each pass, will be kept in the order of ipTargets
for target in ipTargets:
    print(target[0])
    UDP_IP = socket.gethostbyname(target[0])
    PACKETDATA = '#' + format(COUNT, '04d') +  '; hello, this is a test from the case institute of technology, if you see this please report it to kps59@case.edu. this is not harmful and can be ignored. the purpose of this test is to verify that packets being returned truncate the payload from unexpected udp traffic. this is not the case with many different router configurations. if you would like to know more please contact the above with any inquiries. ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################'
    PACKETDATA = PACKETDATA.encode("utf8")

    try:
        outSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        outSock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 64)
        rtt = time.time()
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

        # get packet and clock it into rttList
        inPacket = inSock.recv(1500)
        rtu = time.time()
        rttList.append(rtt - rtu)
        print(rtt - rtu)
       
        print()


        #unStruct = struct.unpack("!H", inPacket[36:38])[0]
        unStruct = inPacket[36]

        # this is a diagram of the packet we expect to recieve
        # note that 69 is 0100101 or nibbles 4 and 5 for version and params respectively
        # and we expect a code 3 port unreachable for the icmp message
        #        0       1       2       3
        #     _______________________________    
        # 0  | 69    | dscp  | total length  |  ip
        # 4  | id            | flags | frag  |
        # 8  | ttl   | proto | header check  |
        # 12 | source ip address             |
        # 16 | destination ip address        |
        # 20 | 3     | 3     | checksum      |  icmp
        # 24 | unused        | next-hop mtu  |
        # 28 | 69    | dscp  | total length  |  ip
        # 32 | id            | flags | frag  |
        # 36 | ttl   | proto | header check  |
        # 40 | source ip address             |
        # 44 | destination ip address        |
        # 48 | source port   | dest port     |  udp
        # 52 | length        | checksum      |
        
        # append hopList with amount of hops
        hopList.append(64 - unStruct)

        # append amtList with the amount of extranious octothorpes missing
        amtList.append(0 - (sys.getsizeof(inPacket) - (1556)))

        # print recieved data
        print(inPacket)
        print("revieved data:", unStruct)
        print("test:", inPacket[26])
        inSock.close()

    except socket.error as x:
        print("socket error, probably timeout")

    COUNT += 1
