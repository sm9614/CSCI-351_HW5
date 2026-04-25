from mininet.net import Mininet
from mininet.node import OVSController
from mininet.link import TCLink
from mininet.node import Node
from mininet.cli import CLI


def create_network():
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
    net.addLink(routerB, transition_switch, intfName1="routerB-eth0",
                params1={"ip": "20.10.172.226/27"})
    net.addLink(routerC, transition_switch, intfName1="routerC-eth0",
                params1={"ip": "20.10.172.227/27"})

    # enables forwarding and starts the network
    net.start()
    for router in [routerA, routerB, routerC]:
        router.cmd("sysctl -w net.ipv4.ip_forward=1")

    CLI(net)

    # disble forwarding and stops network
    for router in [routerA, routerB, routerC]:
        router.cmd("sysctl -w net.ipv4.ip_forward=0")
    net.stop()


def main():
    create_network()


if __name__ == "__main__":
    main()
