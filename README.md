# Ansible Playbook for network port checking from host level - OpenShift as example

It has been a long time that we always having issues when deploying an application and firewalls are not ready yet. 

There is plenty of ways of testing network connectivities, such as using telnet or nc.

However all these has its own problem

* Telnet requires installing packages which may not be by default installed
* Telnet requires the target service to be up and running
* nc requires installation of netcat package which may consider as not secure
* nc works well for tcp, but for udp, it will fail if the firewall rule is drop packet instead of reject

There are several other approaches, and most of the approaches are either requires installation of additional packages nor needs the service to be already installed.

Checking network connectivity before actually spend effort to install large applications such as EAP, Openshift, Openstack or other applications that require large number of ports for communication becomes a difficult task in real world.


## Design principles

* Minimum requirements for managing node and managed node
* Test of TCP and UDP
* Allow checking from groups of client to groups of servers
* Target services does not have to start

## Requirements

* Python in both managing node and managed node
* The testing port is not binding (that is the actual service is not up and running yet)


## How it works

This playbook will basically starts the server application which is a simple python scripts at server side and then starts the python clients trying to send a simple message to server. The client will ensure that a reply is received.


After all clients has sent it message, we will check the server and see how many clients have connected to it since it starts.


By this way we can make the connectivity green. And all the others not being able to connect will be marked as fail – red.

## Play book structure

```
|- callback_plugins
|   | - installer_checkpoint.py
|   | - installer_checkpoint.pyc
| - files
|   | - tcpClient.py
|   | - tcpServer.py
|   | - udpClient.py
|   | - udpServer.py
| - inventory
| - lookup_plugins
|   | - ip.py
|   | - ip.pyc
| - main.yaml
| - port_definition.yaml
| - tasks
    | - init_phases.yaml
    | - loop_phase_from_clients.yaml
    | - loop_phase_to_server.yaml
    | - register_test_result.yaml
    | - server_check.yaml
    | - start_port_check.yaml
    | - start_to_servers.yaml
    | - tcp_from_clients.yaml
    | - tcp_to_server.yaml
    | - udp_from_clients.yaml
    | - udp_to_server.yaml

```

## How to use:
1. Fill in the inventory as usual, grouping the nodes by zone or by nature. For example, Openshift groups the hosts into masters, nodes
2. Fill in the port_definition.yaml for the ports to be scanned
3. Run the playbook as usual



## Example port_definition.yaml

```yaml
port_definitions:
- from_group: nodes
  to_group: nodes
  type: udp
  port: 4789
- from_group: nodes
  to_group: masters
  type: udp
  port: 8053
- from_group: nodes
  to_group: masters
  type: tcp
  port: 8053
- from_group: nodes
  to_group: masters
  type: tcp
  port: 8443
- from_group: masters
  to_group: nodes
  type: tcp
  port: 10250
- from_group: masters
  to_group: nodes
  type: tcp
  port: 10010
- from_group: masters
  to_group: masters
  type: udp
  port: 8053

# Optional for NFS
- from_group: masters
  to_group: masters
  type: udp
  port: 2049


- from_group: masters
  to_group: masters
  type: tcp
  port: 2379
- from_group: masters
  to_group: masters
  type: tcp
  port: 2380

################ addition for 3.11 prometheus monitoring
- from_group: nodes
  to_group: nodes
  type: tcp
  port: 9100

- from_group: nodes
  to_group: nodes
  type: tcp
  port: 10250

- from_group: nodes
  to_group: nodes
  type: udp
  port: 8444
  
```

## Technical skill worth note taking

### Customizing ansible set_stats callback
In order to generate a report for all the ports we scanned, we will use the 
set_stats callback and allow ansible to print out a report after the playbook runs

### Customizing ansible loopup module

To check the ip of the hostname maps to, we used customized loop up plugin instead of using ansible gathered fact for the reason that we only need to know which ip is the host actually mapped to when there is multiple network devices

## To be improved

### Performance

In current design, the whole process is flat looping all the node recursively, so the performance order is n to the power 3. Which is not a perfect way. Will think for more ways to improve the performance

### Check multi-cast

Multi-cast testing is needed for some of the clustering application but they are not being tested in the playbook. I believe multi-cast ports to be used are not as many as tcp and udp one. But will still consider to improve this by adding this function


## Feedback

https://github.com/apoletics/ansible-network-check
