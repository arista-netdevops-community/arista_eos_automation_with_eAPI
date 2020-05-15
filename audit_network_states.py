import yaml
import os
from jsonrpclib import Server
import time 

username = "arista"
password = "arista"

# Devices inventory 
inventory_f=open('inventory.yml', 'r')
inventory_s=inventory_f.read()
inventory_f.close()
inventory=yaml.load(inventory_s, Loader=yaml.FullLoader)

# Printing some details regarding the devices
for device in inventory:
    print ('-'*60)
    print ('Printing some details regarding the device ' + device)
    ip = inventory[device]['ip']
    url = "http://" + username + ":" + password + "@" + ip + "/command-api"
    switch = Server(url)
    result=switch.runCmds(version=1,cmds=["sh ver"], format='json', autoComplete=True)
    print('model is ' + result[0]['modelName'])
    print('version is ' + result[0]['version'])

# auditing the devices
print ('-'*60)
print ('audit will start in 15 seconds ...')
time.sleep(5)
print ('audit will start in 10 seconds ...')
time.sleep(5)
print ('audit will start in 5 seconds ...')
time.sleep(5)

# auditing all BGP neighbors configured on all the devices (i.e we use the devices configuration as a SoT) 
for device in inventory:
    print ('-'*60)
    print ('Auditing all BGP neighbors configured on the device ' + device)
    print ('i.e we are currently using the device configuration as a SoT') 
    ip = inventory[device]['ip']
    url = "http://" + username + ":" + password + "@" + ip + "/command-api"
    switch = Server(url)
    result=switch.runCmds(version=1,cmds=["show ip bgp neighbors"])
    for item in result[0]['vrfs']['default']['peerList']:  
        print ("the BGP session with " + item['peerAddress'] + " is " + item['state'])
        print ("the number of IPv4 prefixes sent to the BGP neighbor " + item['peerAddress'] + " is " + str(item['prefixesSent']))
        print ("the number of IPv4 prefixes received from the BGP neighbor " + item['peerAddress'] + " is " + str(item['prefixesReceived']))

