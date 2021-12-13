#!/usr/bin/env bash

RFILE='/etc/resolv.conf';
if [[ -e "$RFILE" ]]
then
  $(rm $RFILE)
  echo "Restoring symlink to /run/systemd/resolve/stub-resolv.conf"
  $(mv $RFILE.org $RFILE)
fi

echo "Starting systemd-resolved.service"
systemctl start systemd-resolved.service;
