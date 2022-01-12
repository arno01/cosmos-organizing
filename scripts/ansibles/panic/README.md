# Ansible playbooks for configuring PANIC user_config_nodes.ini

### Configure PANIC on monitoring server

To add a node to PANIC config file run the `configure_panic.yml` playbook:
`ansible-playbook -i root@monitor.prod.earthball.xyz, configure_panic.yml --extra-vars "config_file=/home/panic/panic_cosmos/config/user_config_nodes.ini node_name=node1.vega-testnet hostname=node1.vega-testnet.prod.earthball.xyz rpc_port=26657 is_validator=1 include_in_node_monitor=1 include_in_network_monitor=1"`

Variables:
- `config_file` is where the PANIC config file is
- `node_name` is the name of the node normally the first part of the hostname
- `hostname` is the FQDN of the node
- `rpc_port` is the gaiad RPC port normally 26657
- `is_validator` set to `1` if the node is a validator if not set to `0`
- `include_in_node_monitor` set to `1`  to include in node monitor if not set to `0`
- `include_in_network_monitor` set to `1`  to include in network monitor if not set to `0`


To remove a node from PANIC config file simply run the `unconfigure_panic.yml` playbook with the `node_name` variable set:
`ansible-playbook -i root@monitor.prod.earthball.xyz, unconfigure_panic.yml --extra-vars "config_file=/home/panic/panic_cosmos/config/user_config_nodes.ini node_name=node1.vega-testnet"`
