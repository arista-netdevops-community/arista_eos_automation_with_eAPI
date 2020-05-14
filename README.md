## About this repo 

This repo has basic examples of Arista EOS automation using JSON-RPC

## Requirements 

### Requirements on the EOS devices

```
s7152#show running-config section management api
management api http-commands
   protocol http
   no shutdown
s7152#
```

### Requirements on your laptop 

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

## EOS automation 

```
>>> from jsonrpclib import Server
>>> from pprint import pprint as pp
>>> username = "arista"
>>> password = "arista"
>>> ip = "10.83.28.203"
>>> url = "http://" + username + ":" + password + "@" + ip + "/command-api"
>>> print(url)
http://arista:arista@10.83.28.203/command-api
>>> switch = Server(url)
```

### EOS automation using the `runCmds` method

#### Running an EOS `show command` 

```
>>> result=switch.runCmds(version=1,cmds=["show version"])
>>> pp(result)
[{'architecture': 'i686',
  'bootupTimestamp': 1589457836.0,
  'hardwareRevision': '00.00',
  'internalBuildId': '523a3357-484c-4110-9019-39750ffa8af5',
  'internalVersion': '4.22.4M-2GB-15583082.4224M',
  'isIntlVersion': False,
  'memFree': 2839848,
  'memTotal': 4009188,
  'mfgName': 'Arista',
  'modelName': 'DCS-7150S-52-CL-F',
  'serialNumber': 'JPE12370337',
  'systemMacAddress': '00:1c:73:1e:e5:ee',
  'uptime': 33731.23,
  'version': '4.22.4M-2GB'}]
>>> 
>>> result[0]['modelName']
'DCS-7150S-52-CL-F'
>>> result[0]['version']
'4.22.4M-2GB'
>>> 
```

#### Running an EOS `show command` using auto completion

```
>>> result=switch.runCmds(version=1,cmds=["sh ver"], format='json', autoComplete=True)
>>> result[0]['modelName']
'DCS-7150S-52-CL-F'
>>> result[0]['version']
'4.22.4M-2GB'
>>> 
```

#### Running several EOS `show commands` 

```
>>> commands_list = ["sh env temp", "sh ver"]
>>> result=switch.runCmds(version=1,cmds=commands_list, format='json', autoComplete=True)
>>> result[0]['systemStatus'] 
'temperatureOk'
>>> result[1]['version'] 
'4.22.4M-2GB'
>>> 
```

#### Configuring EOS 

```
conf = ["configure", "vlan 100", "name test"] 
conf_vlan_100 = switch.runCmds(version=1,cmds=conf)
result=switch.runCmds(version=1,cmds=["sh vlan"], format='json', autoComplete=True)
result[0]['vlans']['100']['name']

```

#### Configuring EOS using commands auto completion 

```
conf = ["conf", "vla 101", "nam whatever"] 
conf_vlan_101 = switch.runCmds(version=1,cmds=conf, autoComplete=True)
result=switch.runCmds(version=1,cmds=["sh vlan"], format='json', autoComplete=True)
result[0]['vlans']['101']['name']
```

#### configuring EOS devices using more commands 

```
conf = ["configure", "vlan 10", "name ten", "vlan 20", "name twenty"] 
conf_vlans = switch.runCmds(version=1,cmds=conf)
result=switch.runCmds(version=1,cmds=["sh vlan"], format='json', autoComplete=True)
for key,value in result[0]['vlans'].items(): 
   print("vlan " + key + " name is " + value['name'])
```

#### configuring EOS devices using a file 

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

### EOS automation using the `getCommandCompletions` method
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
