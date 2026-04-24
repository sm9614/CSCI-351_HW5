from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI


def create_network():
    net = Mininet()

    print("Creating routers and hosts")
    routerA = net.addHost("routerA", ip="20.10.172.129/26")
    routerB = net.addHost("routerB", ip="20.10.172.1/25")
    routerC = net.addHost("routerC", ip="20.10.172.193/27")

    hostA1 = net.addHost("hostA1", ip="20.10.172.130/26")
    hostA2 = net.addHost("hostA2", ip="20.10.172.131/26")

    hostB1 = net.addHost("hostB1", ip="20.10.172.2/25")
    hostB2 = net.addHost("hostB2", ip="20.10.172.3/25")

    hostC1 = net.addHost("hostC1", ip="20.10.172.194/27")
    hostC2 = net.addHost("hostC2", ip="20.10.172.195/27")

    print("adding links")
    net.addLink(hostA1, routerA)
    net.addLink(hostA2, routerA)

    net.addLink(hostB1, routerB)
    net.addLink(hostB2, routerB)

    net.addLink(hostC1, routerC)
    net.addLink(hostC2, routerC)

    net.addLink(routerA, routerB)
    net.addLink(routerB, routerC)
    net.addLink(routerC, routerA)

    net.start()
    net.pingAll()
    CLI(net)
    net.stop()


def main():
    create_network()


if __name__ == "__main__":
    main()
