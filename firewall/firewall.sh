#!/bin/bash

# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Flush existing rules
iptables -F
iptables -t nat -F
iptables -X

# Set default FORWARD policy to ACCEPT
iptables -P FORWARD ACCEPT

# NAT (Masquerading) for both networks
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE

# Keep the container running
tail -f /dev/null