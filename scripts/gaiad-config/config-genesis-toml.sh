#!/bin/bash

which stoml 2> /dev/null > /dev/null
if [ $? -ne 0 ]
then
	echo "stoml not installed. Please install stoml"
	echo "GO111MODULE=on go get github.com/freshautomations/stoml"
	exit 3
fi

if [ ! $1 ]
then
	echo "Config file missing"
	exit 1
fi

if [ ! -f $1 ]
then
	echo "Cannot find config file: $1"
	exit 2
fi

# change chain id
old_chain_id=$(stoml $1 chain.old_chain_id)
new_chain_id=$(stoml $1 chain.new_chain_id)
sed -i "s%\"chain_id\": \"$old_chain_id\",%\"chain_id\": \"$new_chain_id\",%g" genesis.json

# configure validators
n=1
while [ $(stoml $1 validators.$n.old_pubkey) ] || [ $n -eq 1 ]
do
	node_old_pubkey=$(stoml $1 validators.$n.old_pubkey)
	node_new_pubkey=$(stoml $1 validators.$n.new_pubkey)
	sed -i "s%$node_old_pubkey%$node_new_pubkey%g" genesis.json

	node_old_address=$(stoml $1 validators.$n.old_address)
	node_new_address=$(stoml $1 validators.$n.new_address)
	sed -i "s%$node_old_address%$node_new_address%g" genesis.json

	node1_old_cosmosvalcons1=$(stoml $1 validators.$n.old_cosmosvalcons1)
	node1_new_cosmosvalcons1=$(stoml $1 validators.$n.new_cosmosvalcons1)
	sed -i "s%$node1_old_cosmosvalcons1%$node1_new_cosmosvalcons1%g" genesis.json

	let n=$n+1
done

# substitute a user account,this user account is a delegator in the genesis file. This user account will be owned by node2(validator2) in the later setup.
old_delegator_address=$(stoml $1 vars.old_delegator_address)
new_delegator_address=$(stoml $1 vars.new_delegator_address)
sed -i "s%$old_delegator_address%$new_delegator_address%g" genesis.json

old_delegator_key=$(stoml $1 vars.old_delegator_key)
new_delegator_key=$(stoml $1 vars.new_delegator_key)
sed -i "s%$old_delegator_key%$new_delegator_key%g" genesis.json


# fix delegation amount over 67%
old_delegation_amount=$(stoml $1 vars.old_delegation_amount)
new_delegation_amount=$(stoml $1 vars.new_delegation_amount)
sed -i "s%$old_delegation_amount%$new_delegation_amount%g" genesis.json

# increase the "delegator_shares" by 6,000,000,000,000,000 correspondingly.
old_delegator_shares=$(stoml $1 vars.old_delegator_shares)
new_delegator_shares=$(stoml $1 vars.new_delegator_shares)
sed -i "s%$old_delegator_shares%$new_delegator_shares%g" genesis.json

# increase the validator power by 6,000,000,000
old_validator_power=$(stoml $1 vars.old_validator_power)
new_validator_power=$(stoml $1 vars.new_validator_power)
sed -i "s%\"power\": \"$old_validator_power\"%\"power\": \"$new_validator_power\"%g" genesis.json

# increase total amounts of bonded tokens recorded during the previous end block by 6,000,000,000
old_last_total_power=$(stoml $1 vars.old_last_total_power)
new_last_total_power=$(stoml $1 vars.new_last_total_power)
sed -i "s%\"$old_last_total_power\"%\"$new_last_total_power\"%g" genesis.json

# fix total supply of uatom
old_uatom_amount=$(stoml $1 vars.old_uatom_amount)
new_uatom_amount=$(stoml $1 vars.new_uatom_amount)
sed -i "s%$old_uatom_amount%$new_uatom_amount%g" genesis.json

# Increase the delegation account by 6,000,000,000,000,000
old_delegation_account=$(stoml $1 vars.old_delegation_account)
new_delegation_account=$(stoml $1 vars.new_delegation_account)
sed -i "s%$old_delegation_account%$new_delegation_account%g" genesis.json

# min deposition amount
old_deposition_amount=$(stoml $1 vars.old_deposition_amount)
new_deposition_amount=$(stoml $1 vars.new_deposition_amount)
sed -i "s%\"amount\": \"$old_deposition_amount\",%\"amount\": \"$new_deposition_amount\",%g" genesis.json

# min voting power that a proposal requires in order to be a valid proposal
old_voting_power=$(stoml $1 vars.old_voting_power)
new_voting_power=$(stoml $1 vars.new_voting_power)
sed -i "s%\"quorum\": \"$old_voting_power\",%\"quorum\": \"$new_voting_power\",%g" genesis.json

# the minimum proportion of “yes” votes requires for the proposal to pass
old_yes_threshold=$(stoml $1 vars.old_yes_threshold)
new_yes_threshold=$(stoml $1 vars.new_yes_threshold)
sed -i "s%\"threshold\": \"$old_yes_threshold\",%\"threshold\": \"$new_yes_threshold\",%g" genesis.json

# voting period
old_voting_period=$(stoml $1 vars.old_voting_period)
new_voting_period=$(stoml $1 vars.new_voting_period)
sed -i "s%\"voting_period\": \"$old_voting_period\"%\"voting_period\": \"$new_voting_period\"%g" genesis.json