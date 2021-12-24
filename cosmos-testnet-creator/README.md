# Cosmos Testnet Creator

## API

Tinkering with genesis files

```python
import cosmos_genesis_tinker

genesis = cosmos_genesis_tinker.GenesisTinker()

genesis.load_file(file)
genesis.save_file(file)
old  = {
"pub_key": "",
"address": "",
"consensus_address": ""
}
genesis.swap_validator(old, new)
genesis.swap_delegator(old_adddress, new_address)
genesis.increase_balance(address, increase=300000000, denom="uatom")
genesis.increase_validator_power(validator_address, power_increase=DEFAULT_POWER)
genesis.increase_validator_stake(operator_address, increase=DEFAULT_POWER*POWER_TO_TOKENS)
genesis.increase_delegator_stake(delegator_address, increase=DEFAULT_POWER*POWER_TO_TOKENS)
```

Setting up a Cosmos Network

```python
import cosmos_network_creator

network = cosmos_network_creator.Network()

network.set_genesis_file(path_or_url)
network.set_version("v4.2.0")

machine1 = network.add_machine("127.0.0.1")
machine2 = network.add_machine("127.0.0.1", home="/home/public-facing/gaia/")

machine1.enable_monitoring()
machine2.enable_monitoring()

machine1.set_validator_keypair(something_something)
machine1.enable_validating() # ??
machine1.enable_pruning()

machine2.add_block_explorer(port=420)
machine2.expose_rpc(port=666)

machine1.disable_p2p()
machine1.add_persistent_peer(machine2)

machine2.add_address_book(path_or_object)

relayer = network.add_relayer("127.0.0.1", some_configuration_i_dunno)

relayer.connect_to(machine2)

# Build the network
network.build()
```

## Functionality (TODOs)

- [ ] Publishing on PIP?
- [ ] Pull latest state into a `genesis.json` file
	- [ ] Temporary: hardcode genesis.json file to use
	- Get exported state as genesis file form current mainnet (from github? from somewhere)
		- `gaid export --height int`
		- Is there a way with RPC? Can we talk to a service?
		- Nice to have: automate this with SSH?
- [x] High level python APIs (kinda like DSL for performing operations)
	- Based around this GH issue comment: https://github.com/hyphacoop/cosmos-organizing/issues/28#issuecomment-959780454
- [ ] Ansible for setting up nodes
  - Gaiad binary
  	- Specify a custom path?
  	- Release tag to download from github
  	- Non-gaiad binaries too?
	- How many validators
		- Configure pruning
		- Persitent peers
	- How they are peered with each other
		- Generate addressbook or config.toml?
	- Full nodes: (non-validators)
		- Block explorer
		- Statesync nodes
		- Sentries for validators (connects to validator, runs p2p)
		- Archive nodes (no pruning)
		- Public RPC endpoints?
	- Adding monitoring to nodes
		- graphana
		- panic (simply vc)
	- Relayers (IBC)
	- Connecting to an existing testnet?
- Procuring machines? Terraform?


## Structure

- Use [pylint](https://pylint.org/) and [autopep8](https://github.com/hhatto/autopep8)
- Phases
	- Configure
		- Number of nodes
		- (existing node IDs?)
		- Gaiad binary?
