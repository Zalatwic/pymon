#kps59

import numpy as np
import matplotlib.colors as mcol
import matplotlib.patches as mpatch
import matplotlib.pyplot as pyp
import socket
import struct
import select
import time
import sys

with open("target.txt") as i:
    ipTargets = [line.split() for line in i]

UDP_PORT = 33444
COUNT = 0

rttList = list()    # list to hold the amount of time it takes between sending and recieving the packet
hopList = list()    # list to hold the amount of hops
amtList = list()    # list to hold the amount of bytes
respUrl = list()    # list to hold origin of responce urls

# adds an element to each fooList on each pass, will be kept in the order of ipTargets
for target in ipTargets:
    print(target[0])
    UDP_IP = socket.gethostbyname(target[0])
    PACKETDATA = '#' + '; hello, this is a test from the case institute of technology, if you see this please report it to kps59@case.edu. this is not harmful and can be ignored. the purpose of this test is to verify that packets being returned truncate the payload from unexpected udp traffic. this is not the case with many different router configurations. if you would like to know more please contact the above with any inquiries. ####################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################'
    PACKETDATA = PACKETDATA.encode("utf8")

    try:
        # create the sockets for the ping
        outSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        inSock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

        # set the ttl to something we know
        ttl = 64
        outSock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        
        # bind the incoming port and set timeout
        inSock.bind(("", UDP_PORT))
        inSock.settimeout(2)

        # initiate sending of udp packet
        outSock.sendto(PACKETDATA, (UDP_IP, UDP_PORT))
        rtt = time.time()

        # revieve packet (icm message expected)
        inPacket, ipResp = inSock.recvfrom(1500)
        rtu = time.time()
        
        outSock.close()
        print("packet sent")

        timeMil = 1000 * (rtu - rtt)
       
        ttlIn = inPacket[36]

        # idk why but the server and pyrope disagree on what type inPacket[36] is
        if isinstance(inPacket[36], str):
            ttlIn = ord(inPacket[36])
        
        # check that the packet is coming from the correct destination, if not set values to -1
        if UDP_IP != ipResp[0]:
            rttList.append(-1)
            hopList.append(-1)
            amtList.append(-1)
            respUrl.append(-1)

        else:
            rttList.append(timeMil)

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
       
            # ammend url list with responce url
            respUrl.append(ipResp[0])

            # append hopList with amount of hops
            hopList.append(ttl - ttlIn)

            # append amtList with the amount of extranious octothorpes missing
            amtList.append(sys.getsizeof(inPacket))

            # print recieved data
            inSock.close()
    
    except socket.error as x:
        print("socket error")
        rttList.append(-1)
        hopList.append(-1)
        amtList.append(-1)
        respUrl.append(-1)
        exit
    except IndexError as x:
        print("packet shorter than expected")
        continue

    COUNT += 1

print(hopList)
print(rttList)
print(amtList)

# generate a grap
amtNp = np.array(amtList)
colorList = list()

for t in range(len(amtList)):
    if(amtList[t] > 750):
        colorList.append([amtList[t] / 1560, amtList[t] / 1920, amtList[t] / 1600])
    elif(amtList[t] > 500):
        colorList.append([amtList[t] / 840, amtList[t] / 920, amtList[t] / 770])
    elif(amtList[t] > 330):
        colorList.append([amtList[t] / 920, amtList[t] / 1920, amtList[t] / 600])
    elif(amtList[t] > 200):
        colorList.append([amtList[t] / 360, amtList[t] / 780, amtList[t] / 1600])
    elif(amtList[t] > 100):
        colorList.append([amtList[t] / 1560, amtList[t] / 330, amtList[t] / 420])
    else:
        colorList.append([amtList[t] / 156, amtList[t] / 1920, amtList[t] / 600])

pyp.scatter(hopList, rttList, c = colorList, label = amtList)

h = list()
for g in np.unique(amtNp):
    h.append(mpatch.Patch(color = colorList[amtList.index(g)], label = g))

pyp.legend(loc = 'upper left', handles = h)

pyp.xlabel("Hops to destination server")
pyp.ylabel("RTT (s/1000)")
pyp.title("RTT vs. Hop time")

pyp.savefig('outputgraph.png')
pyp.savefig('outputgraph.pdf')
pyp.show()
