![GitHub](https://img.shields.io/github/license/ksator/arista_eos_automation_with_eAPI)   

## Table of content
[About this repository](#about-this-repository)  
[About eAPI](#about-eapi)  
[Requirements](#requirements)  
[Repository structure](#repository-structure)  
[Basic eAPI tutorial](#basic-eapi-tutorial)  
[eAPI advanced demo](#eapi-advanced-demo)  

## About this repository 

This repo has basic examples of Arista EOS automation using eAPI.  
This includes devices configuration and devices states audit.  

## About eAPI

Using eAPI, an application can send a list of EOS commands (both show commands and configuration commands) to EOS devices.  
eAPI uses JSON-RPC over HTTP.  
So the devices reply using a JSON representation of the show commands which make devices states auditing easy.  

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

## Repository structure 

- The inventory file is [inventory.yml](inventory.yml)
- The variables are defined in the [host_vars](host_vars) directory 
- The directory [templates](templates) has the templates
  - [config.j2](templates/config.j2) is a template to generate configuration files
  - [audit.j2](templates/bgp_audit.j2) is a template to generate EOS show commands to validate the desirated states on remote devices. 
- The directory [config](config) has the devices configuration generated from the template [config.j2](templates/config.j2) and the variables in [host_vars](host_vars) directory. we use eAPI to configure the devices.   
- The directory [audit](audit) has the EOS show commands generated from the template [audit.j2](templates/bgp_audit.j2) and the variables in the [host_vars](host_vars) directory. We reuse the same variables we used to generate the configuration files. To get the devices states, we use eAPI to run these show commands and parse the output. 
- The file [configure_network.py](configure_network.py) generates EOS configuration files from the template [config.j2](templates/config.j2), and uses eAPI to configure the devices
- The file [audit_network_states.py](audit_network_states.py) audits **all** the configured BGP neigbhors. It uses the devices configuration as a SoT. 
- The file [audit_desired_states.py](audit_desired_states.py) audits **only** the BGP neighbors you configured (the ones described in the variables in the [host_vars](host_vars) directory)the devices states. It uses the devices variables as a SoT. To audit only these BGP neighbors, it generates EOS show commands from the template [audit.j2](templates/bgp_audit.j2) and the variables in the [host_vars](host_vars) directory and save these show commands in the directory [audit](audit). So to audit only these BGP neighbors, we reuse the same variables we used to generate the configuration files.
- The file [commands.txt](commands.txt) is used for the basic [basic eAPI tutorial](#basic-eapi-tutorial) 

## Basic eAPI tutorial 

We will use a Python interactive session for this tutorial  

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
>>> conf = ["enable", "configure", "vlan 10", "name ten"]
>>> conf_vlan_10 = switch.runCmds(version=1,cmds=conf)
>>> result=switch.runCmds(version=1,cmds=["show vlan"])
>>> result[0]['vlans']['10']['name']
'ten'
>>> 
```
```
>>> conf = ["enable", "configure", "vlan 20", "name twenty", "vlan 30", "name thirty"] 
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
>>> conf = ["enable", "conf", "vla 40", "nam forty"] 
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
['enable', 'conf', 'vlan 50', 'name fifty', 'vlan 60 ', 'name sixty']
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

## eAPI advanced demo

### Lab topology

3 EOS devices connected in a triangle topology.  
We will use eAPI to configure the devices (EBGP and interfaces) and to audit them.  

![topology.png](topology.png)

### Configure the devices

To generate EOS configuration files and configure the devices, run this command: 

```
python configure_network.py
```

Script output example: 
```
------------------------------------------------------------
Printing some details regarding the device switch1
model is DCS-7050SX-64-F
version is 4.22.1F-INT
------------------------------------------------------------
Printing some details regarding the device switch2
model is DCS-7150S-52-CL-F
version is 4.22.4M-2GB
------------------------------------------------------------
Printing some details regarding the device switch3
model is DCS-7150S-52-CL-F
version is 4.22.4M-2GB
------------------------------------------------------------
Generating the template for device switch1
The generated device configuration is now saved in the config directory
------------------------------------------------------------
Generating the template for device switch2
The generated device configuration is now saved in the config directory
------------------------------------------------------------
Generating the template for device switch3
The generated device configuration is now saved in the config directory
------------------------------------------------------------
configuring the device switch1
Done
------------------------------------------------------------
configuring the device switch2
Done
------------------------------------------------------------
configuring the device switch3
Done
```

Run this command to see the files generated
```
ls config
```

### Audit the devices 

#### To audit all BGP sessions currently configured on the devices

Run this command: 

```
python audit_network_states.py
```

Script output example: 
```
------------------------------------------------------------
Printing some details regarding the device switch1
model is DCS-7050SX-64-F
version is 4.22.1F-INT
------------------------------------------------------------
Printing some details regarding the device switch2
model is DCS-7150S-52-CL-F
version is 4.22.4M-2GB
------------------------------------------------------------
Printing some details regarding the device switch3
model is DCS-7150S-52-CL-F
version is 4.22.4M-2GB
------------------------------------------------------------
audit will start in 15 seconds ...
audit will start in 10 seconds ...
audit will start in 5 seconds ...
------------------------------------------------------------
Auditing all BGP neighbors configured on the device switch1
i.e we are currently using the device configuration as a SoT
the BGP session with 10.10.10.1 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.1 is 7
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.1 is 5
the BGP session with 10.10.10.3 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.3 is 6
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.3 is 5
------------------------------------------------------------
Auditing all BGP neighbors configured on the device switch2
i.e we are currently using the device configuration as a SoT
the BGP session with 10.10.10.0 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.0 is 5
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.0 is 5
the BGP session with 10.10.10.5 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.5 is 6
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.5 is 6
------------------------------------------------------------
Auditing all BGP neighbors configured on the device switch3
i.e we are currently using the device configuration as a SoT
the BGP session with 10.10.10.2 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.2 is 5
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.2 is 6
the BGP session with 10.10.10.4 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.4 is 6
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.4 is 6
```
#### To audit only the BGP sessions you configured 

Run this command: 
```
python audit_desired_states.py
```

Script output example: 
```
------------------------------------------------------------
Printing some details regarding the device switch1
model is DCS-7050SX-64-F
version is 4.22.1F-INT
------------------------------------------------------------
Printing some details regarding the device switch2
model is DCS-7150S-52-CL-F
version is 4.22.4M-2GB
------------------------------------------------------------
Printing some details regarding the device switch3
model is DCS-7150S-52-CL-F
version is 4.22.4M-2GB
------------------------------------------------------------
audit will start in 15 seconds ...
audit will start in 10 seconds ...
audit will start in 5 seconds ...
------------------------------------------------------------
Auditing only the desired BGP neighbors on the device switch1
i.e we are currently using the device variables as a SoT
the BGP session with 10.10.10.1 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.1 is 7
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.1 is 5
the BGP session with 10.10.10.3 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.3 is 6
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.3 is 5
------------------------------------------------------------
Auditing only the desired BGP neighbors on the device switch2
i.e we are currently using the device variables as a SoT
the BGP session with 10.10.10.0 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.0 is 5
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.0 is 5
the BGP session with 10.10.10.5 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.5 is 6
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.5 is 6
------------------------------------------------------------
Auditing only the desired BGP neighbors on the device switch3
i.e we are currently using the device variables as a SoT
the BGP session with 10.10.10.2 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.2 is 5
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.2 is 6
the BGP session with 10.10.10.4 is Established
the number of IPv4 prefixes sent to the BGP neighbor 10.10.10.4 is 6
the number of IPv4 prefixes received from the BGP neighbor 10.10.10.4 is 6
```
To see the commands generated, run this command: 
```
ls audit   
```
