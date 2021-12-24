#!/usr/bin/env python3

import sys
import cosmos_genesis_tinker

if len(sys.argv) != 3:
    print(
        'Usage: ./modify_genesis.py [exported_genesis.json] [new_genesis.json]')
    sys.exit(1)

exported_genesis_filename = sys.argv[1]
new_genesis_filename = sys.argv[2]

# static values (for now, should be in .json config file)
node1_old_pubkey = "cOQZvh/h9ZioSeUMZB/1Vy1Xo5x2sjrVjlE/qHnYifM="
node1_old_address = "B00A6323737F321EB0B8D59C6FD497A14B60938A"
node1_new_pubkey = "qwiUMxz3llsy45fPvM0a8+XQeAJLvrX3QAEJmRMEEoU="
node1_new_address = "D5AB5E458FD9F9964EF50A80451B6F3922E6A4AA"
node1_old_cosmosvalcons1 = "cosmosvalcons1kq9xxgmn0uepav9c6kwxl4yh599kpyu28e7ee6"
node1_new_cosmosvalcons1 = "cosmosvalcons16k44u3v0m8uevnh4p2qy2xm08y3wdf92xsc3ve"

node2_old_pubkey = "W459Kbdx+LJQ7dLVASW6sAfdqWqNRSXnvc53r9aOx/o="
node2_old_address = "83F47D7747B0F633A6BA0DF49B7DCF61F90AA1B0"
node2_new_pubkey = "oi55Dw+JjLQc4u1WlAS3FsGwh5fd5/N5cP3VOLnZ/H0="
node2_new_address = "7CB07B94FD743E2A8520C2B50DA4B03740643BF5"
node2_old_cosmosvalcons1 = "cosmosvalcons1s0686a68krmr8f46ph6fklw0v8us4gdsm7nhz3"
node2_new_cosmosvalcons1 = "cosmosvalcons10jc8h98awslz4pfqc26smf9sxaqxgwl4vxpcrp"

# user account for delegator (node2)
old_delegator_address = "cosmos1qq9ydrjeqalqa3zyqqtdczvuugsjlcc3c7x4d4"
new_delegator_address = "cosmos10aak94tfdl3pgt8qe6ga75qh3zkf3anpq8aqg0"
old_delegator_key = "AjEkAHzQakRnyUppiM5/hnA6h2D7NkdxExxgiCG+NiDh"
new_delegator_key = "A81DhG/5sB6RA8dl/6jtmX0svTc0xJL5NjPPI/q4jJWP"

# binance val
validator_address = "cosmosvaloper156gqf9837u7d4c4678yt3rl4ls9c5vuursrrzf"
token_bonding_pool = "cosmos1fl48vsnmsdzcv85q5d2q4z5ajdha8yu34mf0eh"

tinker = cosmos_genesis_tinker.GenesisTinker()

tinker.load_file(exported_genesis_filename)
tinker.swap_validator({
    "pub_key": node1_old_pubkey,
    "address": node1_old_address,
    "consensus_address": node1_old_cosmosvalcons1
}, {
    "pub_key": node1_new_pubkey,
    "address": node1_new_address,
    "consensus_address": node1_new_cosmosvalcons1
})

tinker.swap_validator({
    "pub_key": node2_old_pubkey,
    "address": node2_old_address,
    "consensus_address": node2_old_cosmosvalcons1
}, {
    "pub_key": node2_new_pubkey,
    "address": node2_new_address,
    "consensus_address": node2_new_cosmosvalcons1
})
tinker.swap_delegator(old_delegator_address, new_delegator_address)

tinker.increase_balance(new_delegator_address, 300000000)

tinker.increase_validator_power(node2_old_address, 6000000000)

stake_increase = 6000000000000000
tinker.increase_balance(token_bonding_pool, stake_increase)
tinker.increase_validator_stake(validator_address, stake_increase)
tinker.increase_delegator_stake(new_delegator_address, stake_increase)

tinker.save_file(new_genesis_filename)
