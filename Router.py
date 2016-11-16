from Table import RouterTable
from Table import ArpTable
import Util


class RouterPort:

    def __init__(self, mac, ip_router, ip_net):
        self.mac = mac
        self.ip = ip_router
        self.ip_net = ip_net

    def __str__(self):
        mac = "\n      MAC = " + self.mac
        r_ip = "\n      Port ip = " + self.ip
        n_ip = "\n      Network ip = " + self.ip_net
        return mac + r_ip + n_ip


class RouterPorts:

    def __init__(self, ports):
        self.ports = []
        it = iter(ports)
        for e in it:
            self.ports.append(RouterPort(e[0], e[1], e[2]))

    def contains(self, ip):
        for e in self.ports:
            if e.ip == ip:
                return e
        return None

    def __str__(self):
        ret = str()
        for p in self.ports:
            ret += "        " + str(p)
        return ret


class Router():

    def __init__(self, name, ports_n, ports):
        self.name = name
        self.ports_n = ports_n
        self.router_ports = RouterPorts(ports)
        self.router_table = RouterTable()
        self.arp_table = ArpTable()

    def icmp_send(self, pack, port, nodes, routers):

        dst = pack.dst[pack.i]

        # Verifica destino na tabela de roteamento.
        # Descubro para qual das minhas portas devo enviar o pacote
        # e para qual ip devo enviar.
        rt_entry = self.router_table.get_destiny(dst)
        # Descubro as informacoes desta porta destino.
        local_port = self.router_ports.ports[int(rt_entry.port)]
        dst_port = None

        # Se o destino esta no mesmo enlace
        if rt_entry.next_hop == "0.0.0.0":
            # Se nao tem mac.
            mac = self.arp_table.get_mac(dst.ip)
            if mac is None:
                args = (self.name, local_port.ip, dst.ip)
                pack.print_arp_request(args)
                args = (dst.name, dst.ip, dst.mac, self.name)
                pack.print_arp_reply(args)

                self.arp_table.append_entry(dst.ip, dst.mac)
                dst.arp_table.append_entry(local_port.ip, local_port.mac)
            else:
                dst.arp_table.append_entry(local_port.ip, local_port.mac)
            args = (self.name, local_port.ip, dst.name, dst.ip, pack.ttl)

        # Envia pela porta especificada ou default
        else:
            dst_aux = rt_entry.next_hop + "/" + local_port.ip.split("/")[1]
            res = Util.get_object(dst_aux, nodes, routers)
            dst = res[0]
            dst_port = res[1]
            mac = self.arp_table.get_mac(dst_port.ip)
            # Se ja tem MAC, faz o envio
            if mac is None:
                args = (self.name, local_port.ip, dst_port.ip)
                pack.print_arp_request(args)
                args = (dst.name, dst_port.ip, port.mac, self.name)
                pack.print_arp_reply(args)
                self.arp_table.append_entry(dst_port.ip, dst_port.mac)
                dst.arp_table.append_entry(local_port.ip, local_port.mac)
            args = (self.name, local_port.ip, dst.name, dst_port.ip, pack.ttl)

        pack.message(args)
        dst.icmp_receive(pack, dst_port, nodes, routers)

    def icmp_receive(self, pack, port, nodes, routers):
        """
            Quando um roteador recebe um pacote, ele decrementa o
            TTL do mesmo e so entao avalia o que fazer. Se o pacote
            tem TTL == 0, o reteador manda para origem do pacote um
            icmp_time_exceeded. Caso contrario faz-se a verificacao
            na tabela de roteamento para encontrar o proximo destino
            do pacote.

            Argumentos:
                pack -- o pacote recebido.
                port -- a porta pel qual o pacote foi recebido.
                nodes -- lista de hosts na aplicacao.
                routers -- lista de roteadores da aplicacao.
        """
        # Verifica TTL do pacote.
        pack.ttl = pack.ttl - 1
        if pack.ttl == 0:
            # Pacote passa a ser um icmp_time_exceeded
            pack.p_type = "ITE"
            # Altera referencia dos objetos.
            pack.dst = [pack.src]
            pack.src = self
            pack.ttl = 8
            pack.i = 0
            # Altera ip origem e destino.
            pack.dst_ip = pack.dst[0].ip
            pack.src_ip = port.ip
        # envia pacote
        self.icmp_send(pack, port, nodes, routers)

    def ports_contains(self, ip):
        return self.router_ports.contains(ip)

    def router_table_contains(self, target):
        return self.router_table.contains_ip(target)

    def __str__(self):
        n = "Router name = " + self.name
        n_p = "\n     Number of ports = " + self.ports_n
        r_t = "\n     Router table \n"
        return n + n_p + str(self.router_ports) + r_t + str(self.router_table)
