Disable and Stop systemd-resolved.service in commnetsemu for free update of /etc/resolv.conf

sudo systemctl stop systemd-resolved.service
sudo rm /etc/resolve.conf (it's a symlink)
