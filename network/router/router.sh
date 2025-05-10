#!/bin/bash

# Enable IP forwarding
echo 1 >/proc/sys/net/ipv4/ip_forward

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth1 -j ACCEPT
iptables -A FORWARD -i eth0 -j ACCEPT
# ip route add 172.29.0.0/16 via 172.30.0.4

# FIREWALL
# Set default policies
iptables -P INPUT DROP    # drop all incoming unless explicitly allowed
iptables -P FORWARD DROP  # drop all forwarded unless explicitly allowed
iptables -P OUTPUT ACCEPT # allow all outgoing

# Allow loopback (local) traffic
iptables -A INPUT -i lo -j ACCEPT

# Allow established/related packets (reply traffic)
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Block maliciuous IP
iptables -I INPUT 1 -s 198.51.100.23 -j DROP


# Keep container running
sleep infinity
