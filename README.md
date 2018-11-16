It has been a long time that we always having issues when deploying an application and firewalls are not ready yet. 


There is plenty of ways of testing network connectivities, such as using telnet or nc.

However all these has its own problem


Telnet requires installing packages which may not be by default installed

Telnet requires the target service to be up and running

nc requires installation of netcat package which may consider as not secure

nc works well for tcp, but for udp, it will fail if the firewall rule is drop packet instead of reject

There are several other approaches, and most of the approaches are either requires installation of additional packages nor needs the service to be already installed.

Checking network connectivity before actually spend effort to install large applications such as EAP, Openshift, Openstack or other applications that require large number of ports for communication becomes a difficult task in real world.

Design principles 

Minimum requirements for managing node and managed node

Test of TCP and UDP

Allow checking from groups of client to groups of servers

Target services does not have to start 


Requirements


Python in both managing node and managed node

The testing port is not binding (that is the actual service is not up and running yet)

How it works

This playbook will basically starts the server application which is a simple python scripts at server side and then starts the python clients trying to send a simple message to server. The client will ensure that a reply is received.

After all clients has sent it message, we will check the server and see how many clients have connected to it since it starts.

By this way we can make the connectivity green. And all the others not being able to connect will be marked as fail – red.

Technical skill worth note taking

Customizing ansible set_stats callback

In order to generate a report for all the ports we scanned, we will use the set_stats callback and allow ansible to print out a report after the playbook runs

Customizing ansible loopup module

To check the ip of the hostname maps to, we used customised loop up plugin instead of using ansible gathered fact for the reason that we only need to know which ip is the host actually mapped to when there is multiple network devices

Improvements

Performance

In current design, the whole process is flat looping all the node recursively, so the performance order is n to the power 3. Which is not a perfect way. Will think for more ways to improve the performance

Check multi-cast

Multi-cast testing is needed for some of the clustering application but they are not being tested in the playbook. I believe multi-cast ports to be used are not as many as tcp and udp one. But will still consider to improve this by adding this function




































