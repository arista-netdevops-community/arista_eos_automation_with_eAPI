# About this repo 

This repo has basic examples of Arista EOS automation using JSON-RPC

# Requirements 

## Requirements on the EOS devices

```
s7152#show running-config section management api
management api http-commands
   protocol http
   no shutdown
s7152#
```

## Requirements on your laptop 
```
python -V
Python 3.7.7
```
```
pip install jsonrpclib-pelix 
```
```
pip freeze | grep jsonrpc
jsonrpclib-pelix==0.4.1
```

# EOS automation using the `runCmds` method

```
from jsonrpclib import Server
username = "arista"
password = "arista"
ip = "10.83.28.203"
url = "http://" + username + ":" + password + "@" + ip + "/command-api"
switch = Server(url)
```

## EOS `show commands` 

### without auto completion
```
result=switch.runCmds(version=1,cmds=["show version"])
result[0]['modelName']
result[0]['version']
```
### using auto completion
```
result=switch.runCmds(version=1,cmds=["sh ver"], format='json', autoComplete=True)
result[0]['modelName']
result[0]['version']
```
### using several commands 
```
commands_list = ["sh env temp", "sh ver"]
result=switch.runCmds(version=1,cmds=commands_list, format='json', autoComplete=True)
result[0]['systemStatus'] 
result[1]['version'] 
```

## EOS configuration changes 

### without auto completion
```
conf = ["configure", "vlan 100", "name test"] 
conf_vlan_100 = switch.runCmds(version=1,cmds=conf)
result=switch.runCmds(version=1,cmds=["sh vlan"], format='json', autoComplete=True)
result[0]['vlans']['100']['name']

```
### using auto completion 
```
conf = ["conf", "vla 101", "nam whatever"] 
conf_vlan_101 = switch.runCmds(version=1,cmds=conf, autoComplete=True)
result=switch.runCmds(version=1,cmds=["sh vlan"], format='json', autoComplete=True)
result[0]['vlans']['101']['name']
```
### configuring EOS devices using more commands 
```
conf = ["conf", "vlan 10", "name ten", "vlan 20", "name twenty"] 
conf_vlans = switch.runCmds(version=1,cmds=conf, autoComplete=True)
result=switch.runCmds(version=1,cmds=["sh vlan"], format='json', autoComplete=True)
for key,value in result[0]['vlans'].items(): 
   print("vlan " + key + " name is " + value['name'])
```
### configuring EOS devices using a file 
```
f = open("commands.txt", "r")
conf = f.read().splitlines()
f.close() 
conf

conf_vlans = switch.runCmds(version=1,cmds=conf, autoComplete=True)
result=switch.runCmds(version=1,cmds=["sh vlan"], format='json', autoComplete=True)
for key,value in result[0]['vlans'].items(): 
   print("vlan " + key + " name is " + value['name'])
```

# EOS automation using the `getCommandCompletions` method
```
from jsonrpclib import Server
username = "arista"
password = "arista"
ip = "10.83.28.203"
url = "http://" + username + ":" + password + "@" + ip + "/command-api"
switch = Server(url)

command_to_complete = "sh"
command_completed = switch.getCommandCompletions(command_to_complete) 
command_completed
command_completed['completions']
print(command_completed['completions'].keys())

for item in command_completed['completions']: 
    print(item)

for key,value in command_completed['completions'].items(): 
     print(key)

command_to_complete = "sh ver"
command_completed=switch.getCommandCompletions(command_to_complete) 
command_completed['completions']
```
