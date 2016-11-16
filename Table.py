class RouterEntry:

    def __init__(self, ip, next_hop, port):
        self.ip = ip
        self.next_hop = next_hop
        self.port = port

    def __str__(self):
        ip = self.ip + "( " + self.ip_net + " ) "
        return str(ip + self.next_hop + " " + self.port + "\n")


class ArpEntry:

    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac


class RouterTable:

    def __init__(self):
        self.entries = []
        self.default = None

    def append_entry(self, ip, next_hop, port):
        '''
            Adiciona uma entrada a lista na tabela de roteamento.

            @param ip: endereco ip de rede a ser armazenado.
            @param next_hop: next hop a ser armazenado
            @param port: numero da porta a qual o pacote deve
            ser encaminhado.
        '''
        e = RouterEntry(ip, next_hop, port)
        if ip == "0.0.0.0/0":
            self.default = e
        else:
            self.entries.append(e)

    def get_destiny(self, dst):
        '''
            Para um dado destino o metodo retorna a porta pela
            qual o roteador deve enviar o pacote.

            @param dst: ip de rede destino.
            @return: um objeto do tipo RouterPort
        '''
        # Compara o ip destino com todas as entradas da tabela
        for e in self.entries:
            # print e.ip, dst.ip_net
            if e.ip == dst.ip_net:
                # Econtrou, envia ip destino
                return e
        # Nao encontrou, retorna rota default
        return self.default

    def __str__(self):
        s = ""
        for e in self.entries:
            s += "      " + str(e)
        return s


class ArpTable:

    def __init__(self):
        self.entries = []

    def append_entry(self, ip, mac):
        e = ArpEntry(ip, mac)
        self.entries.append(e)

    def get_mac(self, ip):
        '''
            Verifica se existe uma entrada na tabela com o ip dado
            e retorna o MAC caso ela entrada exista.

            @param ip: endereco IP a ser procurado.
            @return: retorna o MAC se ip existir, ou None caso contrario.
        '''
        for e in self.entries:
            if e.ip == ip:
                return e.mac
        return None

    def contains_ip(self, ip):
        for e in self.entries:
            if e.ip == ip:
                return e.ip
        return None
