ifconfig enp0s8 up
ip addr add 10.0.0.3/24 dev enp0s8

# Configure Routing
# ip route add 10.0.1.0/24 via 10.0.0.1
# ip route del default
# ip route add default via 10.0.0.1
ip route add 10.0.114.0/24 via 10.0.0.1
# Accept SRv6 traffic
# sysctl -w net.ipv6.conf.all.seg6_enabled=1
# sysctl -w net.ipv6.conf.lo.seg6_enabled=1
# sysctl -w net.ipv6.conf.eth1.seg6_enabled=1
# sysctl -w net.ipv6.conf.eth2.seg6_enabled=1

# Enable forwarding
sysctl -w net.ipv6.conf.all.forwarding=1
