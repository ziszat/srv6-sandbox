#!/bin/bash

# Configure Interfaces
ifconfig enp0s8 up
ip -6 addr add 2001:10::2/64 dev enp0s8

ifconfig enp0s9 up
ip -6 addr add 2001:12::1/64 dev enp0s9

ifconfig enp0s10 up
ip -6 addr add 2001:13::1/64 dev enp0s10

ifconfig lo up
ip -6 addr add fc00:1::1/64 dev lo

# Enable forwarding
sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv6.conf.all.forwarding=1

# Accept SRv6 traffic
sysctl -w net.ipv6.conf.all.seg6_enabled=1
sysctl -w net.ipv6.conf.lo.seg6_enabled=1
sysctl -w net.ipv6.conf.enp0s8.seg6_enabled=1
sysctl -w net.ipv6.conf.enp0s9.seg6_enabled=1
sysctl -w net.ipv6.conf.enp0s10.seg6_enabled=1

# Configure Routing
ip -6 route del default
ip -6 route add default via 2001:12::2
ip -6 route add fc00:f::/64 via 2001:10::1
ip -6 route add fc00:2::/64 via 2001:12::2
ip -6 route add fc00:3::/64 via 2001:13::2
ip -6 route add fc00:33::/64 via 2001:13::2
ip -6 route add 2001:56::/64 via 2001:13::2
ip -6 route add 2001:b::/64 via 2001:10::1

# Enable forwarding
sysctl -w net.ipv6.conf.all.forwarding=1

# # Configure SR policies
# ip -6 route add fc00:1::a/128 encap seg6local action End.DX4 nh4 10.0.0.1 dev enp0s8
# ip route add 10.0.1.0/24 encap seg6 mode encap segs fc00:22::a,fc00:3::a dev enp0s9
# ip -6 route add fc00:e::/64 encap seg6 mode encap segs fc00:5::f3:0,fc00:6::D6 dev enp0s9 table br2
ip -6 route add fc00:1::a/128 encap seg6local action End dev enp0s10
ip -6 route add fc00:11::a/128 encap seg6local action End dev enp0s8


# # Configure Branches (BR1 and BR2)
# cd ~/
# rm -rf sr-sfc-demo
# git clone https://github.com/SRouting/sr-sfc-demo
# cd sr-sfc-demo/config/
# sh deploy-term.sh add br1 venp0s8 inet6 fc00:b1::1/64 fc00:b1::2/64
# sh deploy-term.sh add br2 venp0s9 inet6 fc00:b2::1/64 fc00:b2::2/64

# # Configure Policy Based Routing (PBR)
# echo "201 br1" >> /etc/iproute2/rt_tables
# ip -6 rule add from fc00:b1::/64 lookup br1

# echo "202 br2" >> /etc/iproute2/rt_tables
# ip -6 rule add from fc00:b2::/64 lookup br2

# # Configure SR SFC policies
# ip -6 route add fc00:e::/64 encap seg6 mode encap segs fc00:2::f1:0,fc00:3::f2:AD60,fc00:6::D6 dev enp0s8 table br1
# ip -6 route add fc00:e::/64 encap seg6 mode encap segs fc00:5::f3:0,fc00:6::D6 dev enp0s9 table br2

# # Configure SRv6 End.D6 behaviour for traffic going to BR1 and BR2
# ip -6 route add local fc00:1::d6/128 dev lo
