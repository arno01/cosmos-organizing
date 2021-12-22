# Cosmos Testnet Creator

## Functionality (TODOs)

- [ ] Publishing on PIP?
- [ ] Pull latest state into a `genesis.json` file
	- [ ] Temporary: hardcode genesis.json file to use
	- Get exported state as genesis file form current mainnet (from github? from somewhere)
		- `gaid export --height int`
		- Is there a way with RPC? Can we talk to a service?
		- Nice to have: automate this with SSH?
- [ ] High level python APIs (kinda like DSL for performing operations)
	- Based around this GH issue comment: https://github.com/hyphacoop/cosmos-organizing/issues/28#issuecomment-959780454
	- [ ] Swap a custom wallet id into genesis and give it loads of money
		- Replace an existing wallet?
		- Have list of potential IDs to replace if we want multiple?
	- [ ] Swap validator IDs and boost their voting power
	- [ ] Swap delegator IDs
	- [ ] Change delegation
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
