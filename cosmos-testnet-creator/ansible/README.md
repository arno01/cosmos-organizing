# Ansible Cosmos Network Creator

## Dream Playbook - Testnet 1

This playbook (and inventory file) sets up a Cosmos Testnet which contains three validator nodes, and one Archive node, as well as a prometheus monitoring server
All the gaia nodes connect to the prometheus node to report monitoring.
There is also a block explorer on the Archive node

The prometheus node and block exporer pull their hostnames from the inventory file information.

inventory.ini

```ini
# These variables get injected in all the roles
# This makes it easy to configure stuff like ports and versions
[all:vars]
# Specify the version of gaiad to use on nodes
gaiad_version= v4.2.0
genesis_url= https://example.com/genesis.json.gz

# Connect nodes together via the validator IPs
# TODO: Can we access the [validators] group and pull the IPs from there?
persistent_peers="127.0.0.1:26656,4.20.1.3:26656,6.6.6.9:26656"

# Configure gaiad nodes to connect to prometheus for monitoring
prometheus_host=prometheus.hypha.org:26660

[validators]
127.0.0.1
4.20.1.3
6.6.6.9

[archive]
# The arhive node's block expolrer will pull this hostname for its config
testnet-explorer.hypha.org

[prometheus]
prometheus.hypha.org
```

testnet-playbook.yaml

```yaml
- name: Set up validators
  hosts: validators
  roles:
    - role: validator
- name: Set up archive node
  hosts: archive
  roles:
    - role: archive
    - role: block_explorer
- name: Set up prometheus monitoring
	roles:
	  - role: prometheus
```

## Dream Playbook - Testnet 2

This playbook sets up a network with a validator that doesn't connect to anybody but a single sentry node which will then connect out to the rest of the network.

sentry-inventory.ini

```ini
[validator]
validator.example.com

[sentry]
sentry.example.com

[sentry:vars]
validator_id="something or other??"
```

sentry-playbook.yaml

```yaml
- name: Set up sentry node
  - hosts: sentry
  - roles:
    - role: full_node
      vars:
        prune: false
        private_peer_ids: "{{ validator_id }}"
        addressbook_url: "https://quicksync.io/addrbook.cosmos-testnet.json"
- name: Set up validator
  - hosts: validator
  - roles:
    - role: validator
      vars:
        pex:false
        persistent_peers: "{{groups['sentry'][0].ansible_hostname}}:26656"
```

## Functionality

- Reusable Ansible playbooks for setting up entire networks
- Ansible Roles for configuring machines
	- Gaiad (the base layer for gaia nodes)
		- run as systemd service
		- version, for git tag
		- custom genesis file (from local FS or URL)
		- pre-configure node public and private keys
		- custom app.toml (file path OR)
			- custom ports (grpc, api)
			- pruning
			- snapshot_interval
		- custom config.toml (file path OR)
			- fast_sync
			- custom ports (rpc)
			- p2p (laddr, external_address, seeds, persistent_peers)
				- persistent_peers: Should be easy to use machine IPs. [check this](https://stackoverflow.com/questions/36328907/ansible-get-all-the-ip-addresses-of-a-group)
				- private_peer_ids
				- seed_mode
			- statesync
			- prometheus (listen_addr)
		- addressbook.json
		  - Specify a path or a URL (quicksync?)
  - Full Node (extend Gaiad)
	- Validator (extends Gaiad)
		- Sane defaults for setting up a validator node
			- No extra services
			- Not full?
			- configure validator keys
			- Easy to have it peer with just a single peer
	- Statesync (extends Full Node)
		- enables statesync and advertising itself
	- Archive (extend Full Node)
		- Full node
		- No pruning
		- ???
	- Public RPC (extend Gaiad)
		- Expose RPC publicly
		- Heavy pruning?
	- Block Explorer
		- Run along a Full Node (Archive?)
		- Runs block explorer service
  - Graphana
  	- Collect stats
  	- View stats
  - Panic (simply VC)
    - Configure API endpoints and secrets?
  	- Collect stats
  - IBC Relay
  	- TODO: What is needed here?
