# CSCI-351_HW5
```
This program creates the following network:
The IP address space is 20.10.172.0 - 20.10.172.255
LAN A has at least 50 hosts
LAN B has at least 75 hosts
LAN C has at least 20 hosts

Running the code:
  1. install the mininet VM
  2. run the VM on virtualbox
  3. run the code via sudo python <path to layer3_network_code.py>
  4. run following commands to test the newtork:

    <host> ping <host>
    <host> traceroute <host>
    pingall

    sample commands:
    hostA1 ping hostA2
    hostA1 ping hostB2
    hostA1 traceroute hostC2
```