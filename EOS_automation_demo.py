import yaml
from jinja2 import Template
import os
from jsonrpclib import Server

username = "arista"
password = "arista"

f=open('config.j2')
s=f.read()
f.close()
eos_template=Template(s)

cwd = os.getcwd()
config_directory = os.path.dirname(cwd + "/config/")
if not os.path.exists(config_directory):
    os.makedirs(config_directory)

inventory_f=open('inventory.yml', 'r')
inventory_s=inventory_f.read()
inventory_f.close()
inventory=yaml.load(inventory_s, Loader=yaml.FullLoader)

for device in inventory:
    print ('-'*60)
    print ('rendering the template for device ' + device)
    f=open(inventory[device]['vars'])
    s=f.read()
    f.close()
    vars = yaml.load(s, Loader=yaml.FullLoader)
    conf = open(config_directory + '/' + device + '.txt','w')
    conf.write(eos_template.render(vars))
    conf.close()

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

