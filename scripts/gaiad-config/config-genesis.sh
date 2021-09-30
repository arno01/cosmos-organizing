#!/bin/bash

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

# load config file
source $1

# change chain id
sed -i "s%\"chain_id\": \"$old_chain_id\",%\"chain_id\": \"$new_chain_id\",%g" genesis.json

# substitue "Certus One", this is our node1
sed -i "s%$node1_old_pubkey%$node1_new_pubkey%g" genesis.json
sed -i "s%$node1_old_address%$node1_new_address%g" genesis.json
sed -i "s%$node1_old_cosmosvalcons1%$node1_new_cosmosvalcons1%g" genesis.json

# substitue "Binance Staking", this is our node2
sed -i "s%$node2_old_pubkey%$node2_new_pubkey%g" genesis.json
sed -i "s%$node2_old_address%$node2_new_address%g" genesis.json
sed -i "s%$node2_old_cosmosvalcons1%$node2_new_cosmosvalcons1%g" genesis.json

# substitute a user account,this user account is a delegator in the genesis file. This user account will be owned by node2(validator2) in the later setup.
sed -i "s%$old_delegator_address%$new_delegator_address%g" genesis.json
sed -i "s%$old_delegator_key%$new_delegator_key%g" genesis.json


# fix delegation amount over 67%
sed -i "s%$old_delegation_amount%$new_delegation_amount%g" genesis.json

# increase the "delegator_shares" by 6,000,000,000,000,000 correspondingly.
sed -i "s%$old_delegator_shares%$new_delegator_shares%g" genesis.json

# increase the validator power by 6,000,000,000
sed -i "s%\"power\": \"$old_validator_power\"%\"power\": \"$new_validator_power\"%g" genesis.json

# increase total amounts of bonded tokens recorded during the previous end block by 6,000,000,000
sed -i "s%\"$old_last_total_power\"%\"$new_last_total_power\"%g" genesis.json

# fix total supply of uatom
sed -i "s%$old_uatom_amount%$new_uatom_amount%g" genesis.json

# Increase the delegation account by 6,000,000,000,000,000
sed -i "s%$old_delegation_account%$new_delegation_account%g" genesis.json

# min deposition amount
sed -i "s%\"amount\": \"$old_deposition_amount\",%\"amount\": \"$new_deposition_amount\",%g" genesis.json

# min voting power that a proposal requires in order to be a valid proposal
sed -i "s%\"quorum\": \"$old_voting_power\",%\"quorum\": \"$new_voting_power\",%g" genesis.json

# the minimum proportion of “yes” votes requires for the proposal to pass
sed -i "s%\"threshold\": \"$old_yes_threshold\",%\"threshold\": \"$new_yes_threshold\",%g" genesis.json

# voting period
sed -i "s%\"voting_period\": \"$old_voting_period\"%\"voting_period\": \"$new_voting_period\"%g" genesis.json
