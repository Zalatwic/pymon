#kps59

import socket
import struct
import select
import time
import sys

with open("targets.txt") as i:
    ipTargets = [line.split() for line in i]

UDP_PORT = 20
COUNT = 0

rttList = list()    # list to hold the amount of time it takes between sending and recieving the packet
hopList = list()    # list to hold the amount of hops
amtList = list()    # list to hold the amount of bytes 

# adds an element to each fooList on each pass, will be kept in the order of ipTargets
for target in ipTargets:
    print(target[0])
    UDP_IP = socket.gethostbyname(target[0])
    PACKETDATA = '#' + format(COUNT, '02d') +  '; hello, this is a test from the case institute of technology, if you see this please report it to kps59@case.edu. this is not harmful and can be ignored. the purpose of this test is to verify that packets being returned truncate the payload from unexpected udp traffic. this is not the case with many different router configurations. if you would like to know more please contact the above with any inquiries. ##################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################'
    PACKETDATA = PACKETDATA.encode("utf8")

    try:
        # create the sockets for the ping
        outSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        inSock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

        # set the ttl to something we know
        ttl = 36
        outSock.setsockopt(socket.SOL_IP, socket.IP_TTL, 36)
        
        # bind the incoming port and set timeout
        inSock.bind(("", UDP_PORT))
        inSock.settimeout(4)

        # initiate sending of udp packet
        outSock.sendto(PACKETDATA, (UDP_IP, UDP_PORT))
        rtt = time.time()

        # revieve packet (icm message expected)
        inPacket, ipResp = inSock.recvfrom(1550)
        rtu = time.time()
        
        outSock.close()
        print("packet sent")

        timeMil = 1000 * (rtu - rtt)
        
        # get packet number from two bytes from the packet which contain COUNT of sent
        packetNumber = (int)(inPacket[57]) * 10 + (int)(inPacket[58]) - 528

        # check that the packet is coming from the correct destination, if not set values to -1
        if COUNT != packetNumber: 
            rttList.append(-1)
            hopList.append(-1)
            amtList.append(-1)

        else:
            rttList.append(timeMil)
            print(timeMil)
       
            # unpack struct elements as needed based on below chart
            ttlIn = inPacket[36] 

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
       
            print(ipResp)
            # append hopList with amount of hops
            hopList.append(ttl - ttlIn)

            # append amtList with the amount of extranious octothorpes missing
            amtList.append(0 - (sys.getsizeof(inPacket) - (1556)))

            # print recieved data
            inSock.close()
    
    except socket.error as x:
        print("socket error")
        rttList.append(-1)
        hopList.append(-1)
        amtList.append(-1)
        exit
    except IndexError as x:
        print("packet shorter than expected")
        continue

    COUNT += 1

print(hopList)
print(rttList)
print(amtList)
