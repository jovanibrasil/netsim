# TRABALHO FINAL DE REDES DE COMPUTADORES I

O trabalho consiste em desenvolver um simulador de rede. O simulador deve receber como parâmetros de execução o nome de um arquivo de descrição de topologia (conforme formato especificado) e uma lista de nós. O simulador deve apresentar na saída as mensagens enviadas pelos nós e roteadores da topologia conforme o formato estabelecido, considerando o envio de um pacote ICMP Echo Request do primeiro até o último nó da lista e retornando um pacote ICMP Echo Reply para o primeiro nó da lista. A transferência dos pacotes deve respeitar a topologia da rede definida pela arquivo de descrição de topologia. Se existir um loop na topologia, o roteador que chegar ao TTL igual a zero, enviará uma mensagem ICMP Time Exceeded para o último nó que realizou o envio, e o simulador é encerrado.

## Formato do arquivo de descrição de topologia

\# NODE 
\<node\_name\>,\<MAC\>,\<IP/prefix\>,\<gateway\>
\# ROUTER
\<router\_name\>,\<num\_ports\>,\<MAC0\>,\<IP0/prefix\>,\<MAC1\>,\<IP1/prefix\>,\<MAC2\>,\<IP2/prefix\> …
\# ROUTERTABLE
\<router\_name\>,\<net\_dest/prefix\>,\<nexthop\>,\<port\>

## Formato de saída

- Pacotes ARP Request: \<src\_name\> box \<src\_name\> : ARP - Who has \<dst\_IP\>? Tell \<src\_IP\>;
- Pacotes ARP Reply: \<src\_name\> => \<dst\_name\> : ARP - \<src\_IP\> is at \<src\_MAC\>;
- Pacotes ICMP Echo Request: \<src\_name\> => \<dst\_name\> : ICMP - Echo request (src=\<src\_IP\> dst=\<dst\_IP\> ttl=\<TTL\>);
- Pacotes ICMP Echo Reply: \<src\_name\> => \<dst\_name\> : ICMP - Echo reply (src=\<src\_IP\> dst=\<dst\_IP\> ttl=\<TTL\>);
- Pacotes ICMP Time Exceeded: \<src\_name\> => \<dst\_name\> : ICMP - Time Exceeded (src=\<src\_IP\> dst=\<dst\_IP\> ttl=\<TTL\>);

## Modo de execução do simulador

$ simulador \<topologia\> \<nodo1\> \<nodo2\> \<nodo3\> …

## Detalhes para construção do simulador:

- TTL inicial dos pacotes IP deve ser igual a 8.
- A topologia poderá apresentar loops de roteamento.
- A lista de nós de entrada pode ter itens repetidos.
- O simulador deve ser executado a partir de um terminal por linha de comando de acordo com o exemplo apresentado - não deve ser necessário utilizar uma IDE para executar o simulador!!!
- O simulador pode ser implementado em qualquer linguagem.
- A entrada e saída devem respeitar EXATAMENTE os formatos apresentados.
- O formato de saída é baseado na linguagem MsGenny. Sugere-se verificar se a saída está correta através do site https://sverweij.github.io/mscgen\_js. Usar o cabeçalho “wordwraparcs=true,hscale=2.0;” para facilitar a visualização.
