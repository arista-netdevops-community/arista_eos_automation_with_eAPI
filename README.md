## Table of content
[About this repository](##about-this-repository)  
[About eAPI](##about-eapi)  
[Repository structure](##repository-structure)  
[Requirements](##requirements)  
[Basic eAPI tutorial](##basic-eapi-tutorial)  
[Advanced eAPI demo](##advanced-eapi-demo)  

## About this repo 

This repo has basic examples of Arista EOS automation using eAPI.  

## About eAPI

Using eAPI, an application can send a list of EOS commands (both show commands and configuration commands) to EOS devices.  
eAPI uses JSON-RPC over HTTP. 

## Repository structure 

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

## Basic eAPI tutorial 

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

### The `runCmds` method

Using the `runCmds` method, an application can send a list of EOS commands (both show commands and configuration commands) to EOS devices.  

#### Running a `show command` 

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

#### Running a `show command` using auto completion

```
>>> result=switch.runCmds(version=1,cmds=["sh ver"], format='json', autoComplete=True)
>>> result[0]['modelName']
'DCS-7150S-52-CL-F'
>>> result[0]['version']
'4.22.4M-2GB'
>>> 
```

#### Running a list of several `show commands` 

```
>>> commands_list = ["sh env temp", "sh ver"]
>>> result=switch.runCmds(version=1,cmds=commands_list, format='json', autoComplete=True)
>>> result[0]['systemStatus'] 
'temperatureOk'
>>> result[1]['version'] 
'4.22.4M-2GB'
>>> 
```

#### Configuring EOS with a list of several commands

```
>>> conf = ["configure", "vlan 10", "name ten"]
>>> conf_vlan_10 = switch.runCmds(version=1,cmds=conf)
>>> result=switch.runCmds(version=1,cmds=["show vlan"])
>>> result[0]['vlans']['10']['name']
'ten'
>>> 
```
```
>>> conf = ["configure", "vlan 20", "name twenty", "vlan 30", "name thirty"] 
>>> conf_vlans = switch.runCmds(version=1,cmds=conf)
>>> result=switch.runCmds(version=1,cmds=["show vlan"], format='json')
>>> for key,value in result[0]['vlans'].items(): 
...    print("vlan " + key + " name is " + value['name'])
... 
vlan 1 name is default
vlan 10 name is ten
vlan 20 name is twenty
vlan 30 name is thirty
>>> 
```

#### Configuring EOS using auto completion 

```
>>> conf = ["conf", "vla 40", "nam forty"] 
>>> conf_vlan_101 = switch.runCmds(version=1,cmds=conf, autoComplete=True)
>>> result=switch.runCmds(version=1,cmds=["sh vla"], format='json', autoComplete=True)
>>> result[0]['vlans']['40']['name']
'forty'
>>> 
```

#### Configuring EOS devices using a file 

We will use the file [commands.txt](commands.txt) to create the list of commands to run. 

```
>>> f = open("commands.txt", "r")
>>> conf = f.read().splitlines()
>>> f.close() 
>>> conf
['conf', 'vlan 50', 'name fifty', 'vlan 60 ', 'name sixty']
>>> 
>>> conf_vlans = switch.runCmds(version=1,cmds=conf, autoComplete=True)
>>> result=switch.runCmds(version=1,cmds=["sh vlan"], format='json', autoComplete=True)
>>> for key,value in result[0]['vlans'].items(): 
...    print("vlan " + key + " name is " + value['name'])
... 
vlan 1 name is default
vlan 10 name is ten
vlan 60 name is sixty
vlan 20 name is twenty
vlan 30 name is thirty
vlan 50 name is fifty
vlan 40 name is forty
>>> 
```

### The `getCommandCompletions` method

The `getCommandCompletions` method can be used to complete a command.  
This section is fyi only. Use only `runCmds` method. The `runCmds` method supports auto completion as shown above.  

```
>>> command_to_complete = "sh"
>>> command_completed = switch.getCommandCompletions(command_to_complete) 
>>> 
>>> command_completed
{'complete': False, 'completions': {'show': 'Display details of switch operation'}, 'errors': {}}
>>> 
>>> command_completed['completions']
{'show': 'Display details of switch operation'}
>>> 
>>> print(command_completed['completions'].keys())
dict_keys(['show'])
>>> 
>>> for item in command_completed['completions']: 
...     print(item)
... 
show
>>> 
>>> for key,value in command_completed['completions'].items(): 
...      print(key)
... 
show
>>> 
```
```
>>> command_to_complete = "sh ver"
>>> command_completed=switch.getCommandCompletions(command_to_complete) 
>>> command_completed['completions']
{'version': 'Software and hardware versions'}
>>> 
```

## Advanced eAPI demo

### Lab topology

### Demo building blocks

### Run the demo
