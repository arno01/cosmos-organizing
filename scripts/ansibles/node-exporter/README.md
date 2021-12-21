# Ansible playbooks for setting up Prometheus monitoring

### Install Node Exporter on host:

`ansible-playbook -i user@FQDN, install_node_exporter.yml --extra-vars "node_exporter_version=1.2.2 gaia_dir=/home/user/.gaia"`

### Configure Prometheus on monitoring server

`ansible-playbook -i user@monitor.prod.earthball.xyz, configure_prometheus.yml --extra-vars "hostname=FQDN node_exporter_port=9100 jobname=Vega_Testnet gaiad_port=26657 gaiad_prometheus_listen_addr=26660"`

#### Make sure `prometheus` is set to true in `~/.gaia/config/config.toml`

Ease of use interactive shell script wrapper which will run the `install_node_exporter.yml` and the `configure_prometheus.yml` playbooks:
`./setup-monitoring.sh `
```
What is the hostname (FQDN) you want to monitor?
This will be displayed in Grafana too: full-node-01.vega-testnet.prod.earthball.xyz
Username to log into the system? root
node_exporter version to install current version is 1.2.2: 1.2.2
Job name? We are currently using the testing chain name such as Vega_Testnet: Vega_Testnet
gaiad_port? Default is 26657: 26657
gaiad prometheus port? Default is 26660: 26660
Direct path to .gaia directory? (/home/user/.gaia): /root/.gaia
Installing node_exporter on full-node-01.vega-testnet.prod.earthball.xyz
```

To stop monitoring a node simply run the `unconfigure_prometheus.yml` playbook with the hostname variable set:
`ansible-playbook -i root@monitor.prod.earthball.xyz, unconfigure_prometheus.yml --extra-vars "hostname=state-sync-test-01.vega-testnet.prod.earthball.xyz"`

This playbook will remove the config files on the monitoring server with the defined hostname.