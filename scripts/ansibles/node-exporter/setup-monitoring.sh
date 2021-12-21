#!/bin/bash

read -p 'What is the hostname (FQDN) you want to monitor?
This will be displayed in Grafana too: ' hostname

read -p 'Username to log into the system? ' username

read -p 'node_exporter version to install current version is 1.2.2: ' node_exporter_version

read -p 'Job name? We are currently using the testing chain name such as Vega_Testnet: ' jobname

read -p 'gaiad_port? Default is 26657: ' gaiad_port

read -p 'gaiad prometheus port? Default is 26660: ' gaiad_prometheus_listen_addr

read -p 'Direct path to .gaia directory? (/home/user/.gaia): ' gaia_dir

echo "Installing node_exporter on $hostname"
ansible-playbook -i $username@$hostname, install_node_exporter.yml --extra-vars "node_exporter_version=$node_exporter_version gaia_dir=$gaia_dir"

echo "Configuring Prometheus for $hostname"
ansible-playbook -i root@monitor.prod.earthball.xyz, configure_prometheus.yml --extra-vars "hostname=$hostname node_exporter_port=9100 jobname=$jobname gaiad_port=$gaiad_port gaiad_prometheus_listen_addr=$gaiad_prometheus_listen_addr"

