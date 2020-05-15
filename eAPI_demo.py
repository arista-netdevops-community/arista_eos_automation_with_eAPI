import yaml
from jinja2 import Template
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

# Template to generate devices configuration 
f=open('templates/config.j2')
s=f.read()
f.close()
eos_template=Template(s)

# Directory to save the generated devices configuration 
cwd = os.getcwd()
config_directory = os.path.dirname(cwd + "/config/")
if not os.path.exists(config_directory):
    os.makedirs(config_directory)

# Genrating the devices configuration
for device in inventory:
    print ('-'*60)
    print ('Generating the template for device ' + device)
    f=open(inventory[device]['vars'])
    s=f.read()
    f.close()
    vars = yaml.load(s, Loader=yaml.FullLoader)
    conf = open(config_directory + '/' + device + '.txt','w')
    conf.write(eos_template.render(vars))
    conf.close()
    print ('The generated device configuration is now saved in the config directory')

# configuring the devices
for device in inventory:
    print ('-'*60)
    print ('configuring the device ' + device)
    ip = inventory[device]['ip']
    url = "http://" + username + ":" + password + "@" + ip + "/command-api"
    switch = Server(url)
    f = open(config_directory + '/' + device + '.txt','r')
    conf_list = f.read().splitlines()
    f.close() 
    conf = switch.runCmds(version=1,cmds=conf_list, autoComplete=True)
    print ('Done') 

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

# auditing only the desired BGP neigbhors on all the devices (i.e we use the devices variables as a SoT) 
for device in inventory:
    print ('-'*60)
    print ('Auditing only the desired BGP neighbors on the device ' + device)
    print ('i.e we are currently using the device variables as a SoT') 
    # Generating required show commands' 
    f=open(inventory[device]['vars'])
    s=f.read()
    f.close()
    vars = yaml.load(s, Loader=yaml.FullLoader)
    f=open('templates/bgp_audit.j2')
    s=f.read()
    f.close()
    bgp_audit_template=Template(s)
    audit = open("audit/" + device +  "_bgp_audit.txt",'w')
    audit.write(bgp_audit_template.render(vars))
    audit.close()
    # Running required show commands 
    audit = open("audit/" + device +  "_bgp_audit.txt",'r')
    show_commands_list = audit.read().splitlines()
    ip = inventory[device]['ip']
    url = "http://" + username + ":" + password + "@" + ip + "/command-api"
    switch = Server(url)
    for item in show_commands_list: 
        if(item == " "):
            show_commands_list.remove(" ")
    result = switch.runCmds(version=1,cmds=show_commands_list)
    for item in result: 
        print ("the BGP session with " + item['vrfs']['default']['peerList'][0]['peerAddress'] + " is " + item['vrfs']['default']['peerList'][0]['state'])
        print ("the number of IPv4 prefixes sent to the BGP neighbor " + item['vrfs']['default']['peerList'][0]['peerAddress'] + " is " + str(item['vrfs']['default']['peerList'][0]['prefixesSent']))
        print ("the number of IPv4 prefixes received from the BGP neighbor " + item['vrfs']['default']['peerList'][0]['peerAddress'] + " is " + str(item['vrfs']['default']['peerList'][0]['prefixesReceived']))





