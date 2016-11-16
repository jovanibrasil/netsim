class Packet:
    def __init__(self, p_type):
        # Tipos disponiveos - IRQ IRP ARQ ARP
        self.p_type = p_type
        self.src = None
        # Para guardar o primeiro elemento no caso
        # do uso de multiplos hosts.
        self.src_aux = None
        self.dst = []
        self.src_ip = ""
        self.dst_ip = ""
        # Index do destino.
        self.i = 0
        self.ttl = 8
        self.multi_host = False

    def message(self, args):
        if self.p_type == "IRQ":
            self.print_icmp_request(args)
        elif self.p_type == "IRP":
            self.print_icmp_reply(args)
        elif self.p_type == "ITE":
            self.print_icmp_time_exceeded(args)
        else:
            print "Error :("

    def print_arp_request(self, args):
        # args = (src_n, src_ip, dst_ip)
        str1 = args[0] + " box " + args[0]
        str2 = " : ARP - Who has " + args[2].split("/")[0]
        str3 = "? Tell " + args[1].split("/")[0] + ";"
        print str1 + str2 + str3

    def print_arp_reply(self, args):
        # args = (src_n, src_ip, src_mac, dst_n)
        str1 = args[0] + " => " + args[3]
        str2 = " : ARP - " + args[1].split("/")[0]
        str3 = " is at " + args[2] + ";"
        print str1 + str2 + str3

    # Os nomes sso passados por parametro, pois eles
    # dizem respeito de onde os pacotes estao na rede.
    # Ja os enderecos ip nao sao passados por parametro
    # pois sao informados no pacote.

    def print_icmp_request(self, args):
        # args = (src_n, src_ip, dst_n, dst_ip)
        src_n = args[0]
        src_ip = self.src.ip.split("/")[0]
        dst_n = args[2]
        dst_ip = self.dst[self.i].ip.split("/")[0]
        str1 = src_n + " => " + dst_n + " : ICMP - Echo request (src="
        str2 = src_ip + " dst=" + dst_ip
        str3 = " ttl=" + str(self.ttl) + ");"
        print str1 + str2 + str3

    def print_icmp_reply(self, args):
        # args = (src_n, src_ip, dst_n, dst_ip, ttl)
        src_n = args[0]
        src_ip = self.src.ip.split("/")[0]
        dst_n = args[2]
        dst_ip = self.dst[self.i].ip.split("/")[0]
        str1 = src_n + " => " + dst_n + " : ICMP - Echo reply (src="
        str2 = src_ip + " dst=" + dst_ip
        str3 = " ttl=" + str(self.ttl) + ");"
        print str1 + str2 + str3

    def print_icmp_time_exceeded(self, args):
        src_n = args[0]
        src_ip = self.src_ip.split("/")[0]
        dst_n = args[2]
        dst_ip = self.dst_ip.split("/")[0]
        str1 = src_n + " => " + dst_n + " : ICMP - Time exceeded (src="
        str2 = src_ip + " dst=" + dst_ip
        str3 = " ttl=" + str(self.ttl) + ");"
        print str1 + str2 + str3
