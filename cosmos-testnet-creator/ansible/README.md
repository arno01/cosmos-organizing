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

After this has run, you'll want to connect to the validator node with ssh and set up delegation to it with a tx

```
gaiad tx staking create-validator \
  --amount=1000000uatom \
  --pubkey=$(gaiad tendermint show-validator) \
  --moniker="choose a moniker" \
  --chain-id=<chain_id> \
  --commission-rate="0.10" \
  --commission-max-rate="0.20" \
  --commission-max-change-rate="0.01" \
  --min-self-delegation="1000000" \
  --gas="auto" \
  --gas-prices="0.0025uatom" \
  --from=<key_name>
```

Who runs this? Should we have an easy way to pull the validator info from remote validator nodes as a function of the ansible scripts?

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

### Dream Playbook 3 - Custom keys, hardcoded config files

This example will set up some gaiad nodes with custom config files and private keys

customkeys-inventory.yaml

```yaml
all:
  vars:
    gaiad_version: "v4.2.0"
    # Specify paths that all the nodes should use for the `.toml` config files
    # Note that this will override any variables that would normally configure those files
    app_toml: "./app.toml"
    client_toml: "./client.toml"
    config_toml: "./config.toml"
	children:
		nodes:
		  hosts:
		    example1.hypha.com:
		      node_key_path: "./example1-node_key.json"
		      priv_validator_key_path: "./example1-priv_vaidator_key.json"
		    example2.hypha.com:
		      node_key_path: "./exammple2-node_key.json"
		    example3.hypha.com:
		      # You can specify the key inline or using variables
		      node_key: "{\"priv_key\": {\"type\": \"Whatever, you get it\"}}"
```

customkeys-playbook.yaml

```yaml
- name: Set up Gaia node with custom keys and configs
  - hosts: nodes
  - role: gaiad
```

## Functionality

- Reusable Ansible playbooks for setting up entire networks
- Ansible Roles for configuring machines
	- Gaiad (the base layer for gaia nodes)
		- run as systemd service
		- Custom monicker (default to hostname?)
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
		- Cosmovisor?
			- Should be able to pull versions from Github and compile them
		- Firewall
			- Block things by default?
			- Open relevant ports as needed?
			- Based on Elon's [scripts](https://github.com/hyphacoop/ansibles/blob/master/distributed-press/srv1.distributed.press/roles/firewall/tasks/rules.yml)
  - Full Node (extend Gaiad)
  	- pruning: "nothing" to keep full history
	- Validator (extends Gaiad)
		- Sane defaults for setting up a validator node
			- No extra services
			- Not full? (pruning?)
			- configure validator keys
			- Easy to have it peer with just a single peer
  - SentriedValidator (extends Validator)
    - Set to be put behind a sentry node
      - P2P disabled and only the sentry node is allowed to connect
    - More aggressive pruning?
    - `sentry_node` variable to configure the sentry in the persistent_peers?
	- Statesync (extends Full Node?)
		- enables statesync and advertising itself
	- Archive (extend Full Node)
		- Full node
		- No pruning
		- ??? What's the difference from a regular full node?
	- Public RPC (extend Gaiad)
		- Expose RPC publicly
		- Heavy pruning?
	- Block Explorer
		- Run along a Full Node (Archive?)
		- Runs [Big Dipper](https://github.com/forbole/big-dipper) block explorer service
  - Prometheus
    - Set up a prometheus host that gaiad can connect to
  - Panic (simply VC)
    - Based on Elon's [scripts](https://github.com/hyphacoop/cosmos-organizing/pull/56?notification_referrer_id=NT_kwDOAA3oh7EyOTQwMDIwNTc4OjkxMTQ5NQ)
    - Configure API endpoints and secrets?
  	- Collect stats
  - IBC Relay
  	- TODO: What is needed here?
