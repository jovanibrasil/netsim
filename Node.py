from Table import ArpTable
import Util


class Node():

    def __init__(self, name, ip, ip_net, gateway, mac):
        self.name = name
        self.mac = mac
        self.ip = ip
        self.ip_net = ip_net
        self.gateway = gateway
        self.arp_table = ArpTable()

    def icmp_send(self, pack, nodes, routers):
        """
            Uma vez que um host tenha recebido um arp_request, ele
            deve responder a origem utilizando um arp_reply. Ja se
            o pacote recebido pelo host for um imcp_request, o host
            deve responder a origem utilizando um icmp_reply.

            Argumentos:
                pack -- pacote recebido.
                port -- a porta pela qual estou recebendo o pacote.
                nodes -- lista de hosts da aplicacao.
                routers - lista de roteadores da aplicacao.
        """
        # Se estamos na mesma rede.
        dst = pack.dst[pack.i]
        if self.ip_net == dst.ip_net:
            mac = self.arp_table.get_mac(dst.ip)
            if mac is None:
                # Descobre MAC com ARP_REQUEST e ARP_REPLY.
                args = (self.name, self.ip, dst.ip)
                pack.print_arp_request(args)
                args = (dst.name, dst.ip, dst.mac, self.name)
                pack.print_arp_reply(args)
                # Atualiza ARPTABLE.
                self.arp_table.append_entry(dst.ip, dst.mac)
                dst.arp_table.append_entry(self.ip, self.mac)
            # Envia icmp request.
            args = (self.name, self.ip, dst.name, dst.ip, 8)
            pack.message(args)
            dst.icmp_receive(pack, None, nodes, routers)
        # Caso contrario, envio para para porta padrao.
        else:
            # Busco objeto destino e sua porta.
            ip_gateway = self.gateway
            if "/" not in self.gateway:
                ip_gateway += "/" + self.ip.split("/")[1]

            r = Util.get_object(ip_gateway, nodes, routers)
            gateway = r[0]
            dst_port = r[1]

            mac = self.arp_table.get_mac(ip_gateway)
            if mac is None:
                # Faz arp_request, guarda valores e faz envio.
                args = (self.name, self.ip, dst_port.ip)
                pack.print_arp_request(args)
                args = (gateway.name, dst_port.ip, dst_port.mac, self.name)
                pack.print_arp_reply(args)
                # Atualiza ARPTABLE
                self.arp_table.append_entry(dst_port.ip, dst_port.mac)
                gateway.arp_table.append_entry(self.ip, self.mac)
            args = (self.name, self.ip, gateway.name, dst_port.ip, 8)
            pack.message(args)
            gateway.icmp_receive(pack, dst_port, nodes, routers)

    def icmp_receive(self, pack, port, nodes, routers):
        """
            O comportamento de um host quando recebe um icmp_request
            pode ser de duas maneiras:

            1. Se nao ha host na lista para repassar o pacote, retorna
            um icmp_reply para a origem.
            2. Se existem mais hosts na lista, repassa um icmp_request
            para o proximo host da lista.

            Argumentos:
                pack -- pacote recebido.
                port -- a porta pela qual estou recebendo o pacote.
                nodes -- lista de nodos da aplicacao.
                routers -- lista de roteadores da aplicacao.
        """
        if pack.p_type == "IRQ":
            pack.ttl = 8
            # Se so tenho um elemento na lista de hosts.
            if pack.multi_host is False:
                # Altera tipo do pacote.
                pack.p_type = "IRP"
                # Altera referencias dos objetos.
                dst = pack.dst
                pack.dst = [pack.src]
                pack.src = dst[0]
                # Altera valores do pacote.
                pack.src_ip = pack.src.ip
                pack.dst_ip = pack.dst[pack.i].ip
            # Se eu tenho uma lista de hosts destino.
            else:
                pack.src = self
                pack.src_ip = self.ip
                if pack.i < len(pack.dst)-1:
                    pack.i = pack.i + 1
                else:
                    # Acabaram os nodos, faz reply para o primeiro.
                    pack.p_type = "IRP"
                    pack.dst = [pack.src_aux]
                    pack.i = 0
                    pack.dst_ip = pack.dst[pack.i].ip
            self.icmp_send(pack, nodes, routers)

    def __str__(self):
        n = "Host name = " + self.name
        m = "\n     Mac = " + self.mac
        i = "\n     Ip host = " + self.ip
        h = "\n     Ip Network = " + self.ip_net
        g = "\n     Gateway = " + self.gateway
        return (n + m + i + h + g)
