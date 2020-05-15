import yaml
from jinja2 import Template
import os
from jsonrpclib import Server
import time 

username = "arista"
password = "arista"

# Template to generate devices configuration 
f=open('config.j2')
s=f.read()
f.close()
eos_template=Template(s)

# Directory to save devices configuration 
cwd = os.getcwd()
config_directory = os.path.dirname(cwd + "/config/")
if not os.path.exists(config_directory):
    os.makedirs(config_directory)

# Devices variables 
inventory_f=open('inventory.yml', 'r')
inventory_s=inventory_f.read()
inventory_f.close()
inventory=yaml.load(inventory_s, Loader=yaml.FullLoader)

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

# auditing the devices
print ('-'*60)
print ('audit will start in 15 seconds')
time.sleep(15)

for device in inventory:
    print ('-'*60)
    print ('Auditing the device ' + device)
    ip = inventory[device]['ip']
    url = "http://" + username + ":" + password + "@" + ip + "/command-api"
    switch = Server(url)
    result=switch.runCmds(version=1,cmds=["sh ver"], format='json', autoComplete=True)
    print(result[0]['modelName'])



