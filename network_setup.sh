# AP intitial setup
apt install hostapd
systemctl unmask hostapd
systemctl enable hostapd

apt install dnsmasq

DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent

cp ./src/dhcpcd.conf /etc/dhcpcd.conf

if [ ! -e /etc/systemctl.d ]; then
    mkdir /etc/systemctl.d
fi

cp ./src/routed-ap.conf /etc/systemctl.d/routed-ap.conf
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
netfilter-persistent save

# configure dhcp and dns for the hosted network
if [ -e /etc/dnsmasq.conf ]; then
    mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bak
fi

cp ./src/dnsmasq.conf /etc/dnsmasq.conf

# ensure wireless operation

rfkill unblock wlan

# configure AP
if [ ! -e /etc/hostapd ]; then
    mkdir /etc/hostapd
fi
if [ -e /etc/hostapd/hostapd.conf ]; then
    mv /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.bak
fi

cp ./src/hostapd.conf /etc/hostapd/hostapd.conf