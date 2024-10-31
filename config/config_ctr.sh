ifconfig eth1 up
ip -6 addr add 2001:b::2/64 dev eth1

sysctl -w net.ipv6.conf.all.disable_ipv6=0

ifconfig lo up
ip -6 addr add fc00:b::b/64 dev lo

sysctl -w net.ipv6.conf.all.forwarding=1

ip -6 route add 2001:13::/64 via 2001:b::1
ip -6 route add 2001:56::/64 via 2001:b::1
ip -6 route add 2001:10::/64 via 2001:b::1
ip -6 route add 2001:12::/64 via 2001:b::1
ip -6 route add 2001:24::/64 via 2001:b::1
ip -6 route add 2001:35::/64 via 2001:b::1