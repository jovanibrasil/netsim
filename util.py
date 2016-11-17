from node import Node
from router import Router


def octenize(string):
    # Complexe octate with zeros.
    return (str(0) * (8 - len(string))) + string


def int_to_bin(ip):
    # Convert an interger number to a binary string.
    return [octenize(bin(int(e))[2:]) for e in ip]


def conf_values(ip):
    # Network address | Hosts address
    l = ip.split('/')
    ip, mask = l[0].split('.'), int(l[1])
    # Binary network address
    net_ip_bin = ''.join(int_to_bin(ip))
    net_ip_bin_without = net_ip_bin[:mask]
    n = net_ip_bin_without + str(0) * (32 - len(net_ip_bin_without))
    net_ip_int = ([str(int(n[i:i+8], 2)) for i in range(0, 32, 8)])
    return ".".join(net_ip_int) + "/" + str(mask)


def load_data(file_name, nodes, routers):
    file_name = "data/" + file_name
    with open(file_name, 'r+') as f:
        line = f.readline()
        # Read nodes(hosts).
        if '#NODE' in line:
            line = f.readline().replace('\n', '')
            while '#ROUTER' not in line:
                l = line.split(',')
                name = l[0]
                ip = l[2]
                ip_net = conf_values(ip)
                mac = l[1]
                gateway = l[3]
                n = Node(name, ip, ip_net, gateway, mac)
                nodes[n.name] = n
                line = f.readline().replace('\n', '')
        else:
            print "missing #NODE tag"

        line = f.readline().replace('\n', '')

        # Read routers.
        while 'ROUTERTABLE' not in line:
            l = line.split(',')
            name = l[0]
            ports_n = l[1]
            # Load MAC and IP to ports_n ports.
            ports = []
            x = l[2:len(l)]
            for i in range(0, len(x), 2):
                mac = x[i]
                ip = x[i+1]
                ip_net = conf_values(ip)
                ports.append((mac, ip, ip_net))
            r = Router(name, ports_n, ports)
            routers[r.name] = r
            line = f.readline().replace('\n', '')

        line = f.readline().replace('\n', '')
        # Read routes tables.
        while ',' in line:
            l = line.split(',')
            routers[l[0]].router_table.append_entry(l[1], l[2], l[3])
            line = f.readline().replace('\n', '')
        f.close()


def get_object(ip, nodes, routers):
        # print "prcurando por objeto com ip", ip
        for index in routers:
            router = routers[index]
            # Verifica se tem porta com o ip
            port = router.ports_contains(ip)
            # Se tem retorna
            if port is not None:
                return (router, port)
        return None
