#!/bin/bash

expected_out="n1 box n1 : ARP - Who has 192.168.0.3? Tell 192.168.0.2;
n2 => n1 : ARP - 192.168.0.3 is at 00:00:00:00:00:02;
n1 => n2 : ICMP - Echo request (src=192.168.0.2 dst=192.168.0.3 ttl=8);
n2 => n1 : ICMP - Echo reply (src=192.168.0.3 dst=192.168.0.2 ttl=8);"

output=$(python main.py topo1.txt n1 n2)

# echo $expected_out
# echo $output

if [ "$output" = "$expected_out" ]
then
    echo "[v] topo1.txt n1 n2"
else
    echo "[x] topo1.txt n1 n2"
fi

expected_out="n1 box n1 : ARP - Who has 192.168.0.1? Tell 192.168.0.2;
r1 => n1 : ARP - 192.168.0.1 is at 00:00:00:00:00:05;
n1 => r1 : ICMP - Echo request (src=192.168.0.2 dst=192.168.1.2 ttl=8);
r1 box r1 : ARP - Who has 192.168.1.2? Tell 192.168.1.1;
n3 => r1 : ARP - 192.168.1.2 is at 00:00:00:00:00:03;
r1 => n3 : ICMP - Echo request (src=192.168.0.2 dst=192.168.1.2 ttl=7);
n3 => r1 : ICMP - Echo reply (src=192.168.1.2 dst=192.168.0.2 ttl=8);
r1 => n1 : ICMP - Echo reply (src=192.168.1.2 dst=192.168.0.2 ttl=7);" 

output=$(python main.py topo1.txt n1 n3)

# echo $expected_out
# echo $output

if [ "$output" = "$expected_out" ]
then
    echo "[v] topo1.txt n1 n3"
else
    echo "[x] topo1.txt n1 n3"
fi

expected_out="n1 box n1 : ARP - Who has 192.168.0.3? Tell 192.168.0.2;
n2 => n1 : ARP - 192.168.0.3 is at 00:00:00:00:00:02;
n1 => n2 : ICMP - Echo request (src=192.168.0.2 dst=192.168.0.3 ttl=8);
n2 box n2 : ARP - Who has 192.168.0.1? Tell 192.168.0.3;
r1 => n2 : ARP - 192.168.0.1 is at 00:00:00:00:00:05;
n2 => r1 : ICMP - Echo request (src=192.168.0.3 dst=192.168.1.2 ttl=8);
r1 box r1 : ARP - Who has 192.168.1.2? Tell 192.168.1.1;
n3 => r1 : ARP - 192.168.1.2 is at 00:00:00:00:00:03;
r1 => n3 : ICMP - Echo request (src=192.168.0.3 dst=192.168.1.2 ttl=7);
n3 box n3 : ARP - Who has 192.168.1.3? Tell 192.168.1.2;
n4 => n3 : ARP - 192.168.1.3 is at 00:00:00:00:00:04;
n3 => n4 : ICMP - Echo request (src=192.168.1.2 dst=192.168.1.3 ttl=8);
n4 box n4 : ARP - Who has 192.168.1.1? Tell 192.168.1.3;
r1 => n4 : ARP - 192.168.1.1 is at 00:00:00:00:00:06;
n4 => r1 : ICMP - Echo reply (src=192.168.1.3 dst=192.168.0.2 ttl=8);
r1 box r1 : ARP - Who has 192.168.0.2? Tell 192.168.0.1;
n1 => r1 : ARP - 192.168.0.2 is at 00:00:00:00:00:01;
r1 => n1 : ICMP - Echo reply (src=192.168.1.3 dst=192.168.0.2 ttl=7);"

output=$(python main.py topo1.txt n1 n2 n3 n4)

# echo $expected_out
# echo $output

if [ "$output" = "$expected_out" ]
then
    echo "[v] topo1.txt n1 n2 n3 n4"
else
    echo "[x] topo1.txt n1 n2 n3 n4"
fi

expected_out="n1 box n1 : ARP - Who has 192.168.0.1? Tell 192.168.0.2;
r1 => n1 : ARP - 192.168.0.1 is at 00:00:00:00:00:05;
n1 => r1 : ICMP - Echo request (src=192.168.0.2 dst=192.168.1.2 ttl=8);
r1 box r1 : ARP - Who has 192.168.1.2? Tell 192.168.1.1;
n3 => r1 : ARP - 192.168.1.2 is at 00:00:00:00:00:03;
r1 => n3 : ICMP - Echo request (src=192.168.0.2 dst=192.168.1.2 ttl=7);
n3 => r1 : ICMP - Echo request (src=192.168.1.2 dst=192.168.0.3 ttl=8);
r1 box r1 : ARP - Who has 192.168.0.3? Tell 192.168.0.1;
n2 => r1 : ARP - 192.168.0.3 is at 00:00:00:00:00:02;
r1 => n2 : ICMP - Echo request (src=192.168.1.2 dst=192.168.0.3 ttl=7);
n2 => r1 : ICMP - Echo request (src=192.168.0.3 dst=192.168.1.3 ttl=8);
r1 box r1 : ARP - Who has 192.168.1.3? Tell 192.168.1.1;
n4 => r1 : ARP - 192.168.1.3 is at 00:00:00:00:00:04;
r1 => n4 : ICMP - Echo request (src=192.168.0.3 dst=192.168.1.3 ttl=7);
n4 => r1 : ICMP - Echo reply (src=192.168.1.3 dst=192.168.0.2 ttl=8);
r1 => n1 : ICMP - Echo reply (src=192.168.1.3 dst=192.168.0.2 ttl=7);"

output=$(python main.py topo1.txt n1 n3 n2 n4)

# echo $expected_out
# echo $output

if [ "$output" = "$expected_out" ]
then
    echo "[v] topo1.txt n1 n3 n2 n4"
else
    echo "[x] topo1.txt n1 n3 n2 n4"
fi

output=$(python main.py topo3.txt n1 n2)

exit 0
