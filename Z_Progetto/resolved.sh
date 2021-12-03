#!/usr/bin/env bash

systemctl stop systemd-resolved.service;
RFILE='/etc/resolv.conf';

if [[ -L "$RFILE" ]]
then
  echo "Removing symlink to /run/systemd/resolve/resolv.conf"
  $(rm $RFILE);
fi
