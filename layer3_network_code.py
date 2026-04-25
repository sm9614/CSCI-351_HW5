from mininet.net import Mininet
from mininet.node import OVSController
from mininet.link import TCLink
from mininet.node import Node
from mininet.cli import CLI


def create_network():
    """
    creates the network the following network topology:
    The IP address space is 20.10.172.0 - 20.10.172.255
    LAN A: 20.10.172.128/26 supports atleast 50 hosts
    LAN B: 20.10.172.0/25 supports at least 75 hosts
    LAN C: 20.10.172.192/27 supports at least 20 hosts
    """
    net = Mininet(controller=OVSController, link=TCLink)
    net.addController("c0")

    transition_switch = net.addSwitch("s0")
    switchA = net.addSwitch("s1")
    switchB = net.addSwitch("s2")
    switchC = net.addSwitch("s3")

    print("Creating routers and hosts")
    routerA = net.addHost("routerA", ip=None)
    routerB = net.addHost("routerB", ip=None)
    routerC = net.addHost("routerC", ip=None)

    hostA1 = net.addHost("hostA1", ip="20.10.172.130/26",
                         defaultRoute="via 20.10.172.129")
    hostA2 = net.addHost("hostA2", ip="20.10.172.131/26",
                         defaultRoute="via 20.10.172.129")

    hostB1 = net.addHost("hostB1", ip="20.10.172.2/25",
                         defaultRoute="via 20.10.172.1")
    hostB2 = net.addHost("hostB2", ip="20.10.172.3/25",
                         defaultRoute="via 20.10.172.1")

    hostC1 = net.addHost("hostC1", ip="20.10.172.194/27",
                         defaultRoute="via 20.10.172.193")
    hostC2 = net.addHost("hostC2", ip="20.10.172.195/27",
                         defaultRoute="via 20.10.172.193")

    print("adding links")
    net.addLink(hostA1, switchA)
    net.addLink(hostA2, switchA)

    net.addLink(hostB1, switchB)
    net.addLink(hostB2, switchB)

    net.addLink(hostC1, switchC)
    net.addLink(hostC2, switchC)

    net.addLink(routerA, transition_switch, intfName1="routerA-eth0",
                params1={"ip": "20.10.172.225/27"})
    net.addLink(routerA, switchA, intfName1="routerA-eth1",
                params1={"ip": "20.10.172.129/26"})

    net.addLink(routerB, transition_switch, intfName1="routerB-eth0",
                params1={"ip": "20.10.172.226/27"})
    net.addLink(routerB, switchB, intfName1="routerB-eth1",
                params1={"ip": "20.10.172.1/25"})

    net.addLink(routerC, transition_switch, intfName1="routerC-eth0",
                params1={"ip": "20.10.172.227/27"})
    net.addLink(routerC, switchC, intfName1="routerC-eth1",
                params1={"ip": "20.10.172.193/27"})

    # enables forwarding and starts the network
    net.start()
    for router in [routerA, routerB, routerC]:
        router.cmd("sysctl -w net.ipv4.ip_forward=1")

    # links hosts from different LANs
    # LAN A to LAN B
    routerA.cmd("ip route add 20.10.172.0/25 via 20.10.172.226")
    # LAN A to LAN C
    routerA.cmd("ip route add 20.10.172.192/27 via 20.10.172.227")

    # LAN B to LAN A
    routerB.cmd("ip route add 20.10.172.128/26 via 20.10.172.225")
    # LAN B to LAN C
    routerB.cmd("ip route add 20.10.172.192/27 via 20.10.172.227")

    # LAN C to LAN A
    routerC.cmd("ip route add 20.10.172.128/26 via 20.10.172.225")
    # LAN C to LAN B
    routerC.cmd("ip route add 20.10.172.0/25 via 20.10.172.226")

    hostA1.cmd(
        "sudo route add -net 20.10.172.0 netmask 255.255.255.128 gw 20.10.172.129")
    hostA1.cmd(
        "sudo route add -net 20.10.172.192 netmask 255.255.255.224 gw 20.10.172.129")
    hostA2.cmd(
        "sudo route add -net 20.10.172.0 netmask 255.255.255.128 gw 20.10.172.129")
    hostA2.cmd(
        "sudo route add -net 20.10.172.192 netmask 255.255.255.224 gw 20.10.172.129")

    hostB1.cmd(
        "sudo route add -net 20.10.172.128 netmask 255.255.255.192 gw 20.10.172.1")
    hostB1.cmd(
        "sudo route add -net 20.10.172.192 netmask 255.255.255.224 gw 20.10.172.1")
    hostB2.cmd(
        "sudo route add -net 20.10.172.128 netmask 255.255.255.192 gw 20.10.172.1")
    hostB2.cmd(
        "sudo route add -net 20.10.172.192 netmask 255.255.255.224 gw 20.10.172.1")

    hostC1.cmd(
        "sudo route add -net 20.10.172.128 netmask 255.255.255.192 gw 20.10.172.193")
    hostC1.cmd(
        "sudo route add -net 20.10.172.0 netmask 255.255.255.128 gw 20.10.172.193")
    hostC2.cmd(
        "sudo route add -net 20.10.172.128 netmask 255.255.255.192 gw 20.10.172.193")
    hostC2.cmd(
        "sudo route add -net 20.10.172.0 netmask 255.255.255.128 gw 20.10.172.193")
    
    print("\nNetwork CLI")
    print("hosts in LAN A: hostA1, hostA2")
    print("hosts in LAN B: hostB1, hostB2")
    print("hosts in LAN C: hostC1, hostC2")
    print("commands to test network")
    print("pingall")
    print("<host> ping <host>")
    print("<host> traceroute <host>")
    CLI(net)

    # disble forwarding and stops network
    for router in [routerA, routerB, routerC]:
        router.cmd("sysctl -w net.ipv4.ip_forward=0")
    net.stop()


def main():
    create_network()


if __name__ == "__main__":
    main()
