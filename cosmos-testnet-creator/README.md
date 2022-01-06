# Cosmos Testnet Creator

This is a set of tools that help with setting up Cosmos test networks.

The genesis-tinker library helps create custom genesis files by tinkering with existing ones and replacing wallets and values with ones that work for your testnet.

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
