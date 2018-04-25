#kps59

import urllib.request
import geoip2.database
import socket
import math

def getDist(lat1, lon1):
    lat2, lon2 = [41.5007, -81.6023]

    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2-lat1)
    dlam = math.radians(lon2-lon1)

    a = math.sin(dphi/2.0)**2+\
        math.cos(phi1)*math.cos(phi2)*\
        math.sin(dlam/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return c * R * 0.000621371

with open("targets.txt") as i:
    ipTargets = [line.split() for line in i]

with urllib.request.urlopen('http://checkip.amazonaws.com') as response:
    myIp = response.read()

myIp = myIp.decode("utf-8").split('\n')[0]

reader = geoip2.database.Reader('GeoLite2-City.mmdb')
resp = reader.city(myIp).city.name

if(resp == "Cleveland"):
    print("Home id'd as Cleveland")
    
    for target in ipTargets:
        try:
            myIp = socket.gethostbyname(target[0])

            reader = geoip2.database.Reader('GeoLite2-City.mmdb')
            resp = reader.city(myIp).city.name
        
            print("%s; %s; %f" % (myIp, resp, getDist(reader.city(myIp).location.latitude, reader.city(myIp).location.longitude)))
        except TypeError as e:
            print(e)
            exit
        except socket.gaierror as e:
            print(e)
            exit
