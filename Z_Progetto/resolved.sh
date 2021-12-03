#!/usr/bin/env bash

systemctl stop systemd-resolved.service;
RFILE='/etc/resolve.conf';

if [[ -L "$RFILE" ]]
then
  $(rm $RFILE);
fi
