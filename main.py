import util
import sys
from packet import Packet

'''
Autor: Jovani Brasil
Email: jovanibrasil@gmail.com

'''


def main(argv):
    if(len(argv) > 1):

        nodes = dict()
        routers = dict()

        util.load_data(argv[0], nodes, routers)

        # for n in nodes:
        #    print nodes[n]

        # for r in routers:
        #    print routers[r]

        p = Packet("IRQ")
        p.src = nodes[argv[1]]
        p.src_ip = p.src.ip
        p.src_aux = nodes[argv[1]]
        for i in range(2, len(argv)):
            p.dst.append(nodes[argv[i]])
        p.dst_ip = p.dst[0].ip
        if len(argv) > 2:
            p.multi_host = True
        p.src.icmp_send(p, nodes, routers)

    else:
        print "Error."

if __name__ == "__main__":
    main(sys.argv[1:])
