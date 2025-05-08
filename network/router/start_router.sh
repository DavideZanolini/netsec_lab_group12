#!/bin/bash

# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Setup NAT: masquerade traffic going out to the internal_net
# Replace eth1 with correct interface if needed
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE

# Keep container running
sleep infinity
