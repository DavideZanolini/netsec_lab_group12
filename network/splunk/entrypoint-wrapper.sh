#!/bin/bash
set -e

ip route del default
ip route add default via 172.28.0.2

exec /sbin/entrypoint.sh start-service
