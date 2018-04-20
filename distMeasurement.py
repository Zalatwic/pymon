#kps59

import socket

with open("targets.txt") as i:
    ipTargets = [line.split() for line in i]

#ipTargets = [ipTargets.strip() for x in ipTargets]

UDP_PORT = 5005
COUNT = 0

for target in ipTargets:
    print(target[0])
    UDP_IP = socket.gethostbyname(target[0])
    PACKETDATA = '#' + format(COUNT, '04d') +  '; hello, this is a test from the case institute of technology, if you see this please report it to kps59@case.edu. this is not harmful and can be ignored. the purpose of this test is to verify that packets being returned truncate the payload from unexpected udp traffic. this is not the case with many different router configurations. if you would like to know more please contact the above with any inquiries. ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################'.decode('utf8')

    try:
        outSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        outSock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 64)
        outSock.sendto(PACKETDATA, (UDP_IP, UDP_PORT))
        outSock.close()
    except socket.error as x:
        print("outSock error; " + x)
        sys.exit()

    #create a raw socket to read back the data
    try:
        inSock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        inSock.bind((socket.gethostname(), 0))
        inPacket = recv_sock.recv(1500)
        print("revieved data:", data)
        inSock.close()
    except socket.error as x:
        print("outSock error; " + x)
        sys.exit()

    COUNT += 1
