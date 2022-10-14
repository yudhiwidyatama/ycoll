#!/bin/bash
mkdir /root/ycoll
cp lvmusagecoll.py /root/ycoll/
pushd /root/ycoll
pip3 install prometheus-client pyyaml
cp ycoll.service /etc/systemd/system/ycoll.service
systemctl daemon-reload
