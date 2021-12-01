#!/usr/bin/env python3

import json, sys, math

if len(sys.argv) != 3:
  print('Usage: ./modify_genesis.py [exported_genesis.json] [new_genesis.json]')
  sys.exit(1)

exported_genesis_filename = sys.argv[1]
new_genesis_filename = sys.argv[2]

raw_exported_genesis = open(exported_genesis_filename)
old = json.load(raw_exported_genesis)

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

def swap_validator():
  # Replace consensus public key for the validator in two places
  # 1. REPLACE old['app_state']['staking']['validators'][INDEX]['consensus_pubkey']['key']
  # 2. REPLACE old['validators'][INDEX]['pub_key']['value']

  # Node 1 (Certus One)
  index = 0
  for validator in old['app_state']['staking']['validators']:
    if old['app_state']['staking']['validators'][index]['consensus_pubkey']['key'] == node1_old_pubkey:
      old['app_state']['staking']['validators'][index]['consensus_pubkey']['key'] = node1_new_pubkey
      break;
    index = index + 1

  index = 0
  for validator in old['validators']:
    if old['validators'][index]['pub_key']['value'] == node1_old_pubkey:
      old['validators'][index]['pub_key']['value'] = node1_new_pubkey
      break;
    index = index + 1

  # Node 2 (Binance Staking)
  index = 0
  for validator in old['app_state']['staking']['validators']:
    if old['app_state']['staking']['validators'][index]['consensus_pubkey']['key'] == node2_old_pubkey:
      old['app_state']['staking']['validators'][index]['consensus_pubkey']['key'] = node2_new_pubkey
      break;
    index = index + 1

  index = 0
  for validator in old['validators']:
    if old['validators'][index]['pub_key']['value'] == node2_old_pubkey:
      old['validators'][index]['pub_key']['value'] = node2_new_pubkey
      break;
    index = index + 1


  # Replace private validator address in one place
  # 1. REPLACE old['validators'][INDEX]['address']
  # Node 1 (Certus One)
  index = 0
  for validator in old['validators']:
    if old['validators'][index]['address'] == node1_old_address:
      old['validators'][index]['address'] = node1_new_address
      break;
    index = index + 1

  # Node 2 (Binance Staking)
  index = 0
  for validator in old['validators']:
    if old['validators'][index]['address'] == node2_old_address:
      old['validators'][index]['address'] = node2_new_address
      break;
    index = index + 1

  # Replace validator consensus address in two places
  # 1. REPLACE old['app_state']['slashing']['missed_blocks'][INDEX]['address']

  # Node 1 (Certus One)
  index = 0
  for missed_blocks in old['app_state']['slashing']['missed_blocks']:
    if old['app_state']['slashing']['missed_blocks'][index]['address'] == node1_old_cosmosvalcons1:
      old['app_state']['slashing']['missed_blocks'][index]['address'] = node1_new_cosmosvalcons1
      break;
    index = index + 1

  # Node 2 (Binance Staking)
  index = 0
  for missed_blocks in old['app_state']['slashing']['missed_blocks']:
    if old['app_state']['slashing']['missed_blocks'][index]['address'] == node2_old_cosmosvalcons1:
      old['app_state']['slashing']['missed_blocks'][index]['address'] = node2_new_cosmosvalcons1
      break;
    index = index + 1

  # 2. REPLACE old['app_state']['slashing']['signing_infos'][INDEX]['address']
  # May need to replace old['app_state']['slashing']['signing_infos'][INDEX]['validator_signing_info']['address'] for certain cases, but does not seem like a requirement
  # Node 1 (Certus One)
  index = 0
  for signing_infos in old['app_state']['slashing']['signing_infos']:
    if old['app_state']['slashing']['signing_infos'][index]['address'] == node1_old_cosmosvalcons1:
      old['app_state']['slashing']['signing_infos'][index]['address'] = node1_new_cosmosvalcons1
      break;
    index = index + 1

  # Node 2 (Binance Staking)
  index = 0
  for signing_infos in old['app_state']['slashing']['signing_infos']:
    if old['app_state']['slashing']['signing_infos'][index]['address'] == node2_old_cosmosvalcons1:
      old['app_state']['slashing']['signing_infos'][index]['address'] = node2_new_cosmosvalcons1
      break;
    index = index + 1

  return 
  
def swap_delegator():
  # Replace address in 6 places

  # Node 2 (Binance Staking)
  # 1. Replace old['app_state']['auth']['accounts'][INDEX]['address']
  index = 0
  for accounts in old['app_state']['auth']['accounts']:
    try:
      if old['app_state']['auth']['accounts'][index]['address'] == old_delegator_address:
        old['app_state']['auth']['accounts'][index]['address'] = new_delegator_address
        break;
      index = index + 1
    except KeyError:
      pass

  # 2. Replace old['app_state']['bank']['balances'][INDEX]['address']
  index = 0
  for balances in old['app_state']['bank']['balances']:
    if old['app_state']['bank']['balances'][index]['address'] == old_delegator_address:
      old['app_state']['bank']['balances'][index]['address'] = new_delegator_address
      break;
    index = index + 1

  # 3. Replace old['app_state']['staking']['delegations'][INDEX]['delegator_address']
  index = 0
  for delegations in old['app_state']['staking']['delegations']:
    if old['app_state']['staking']['delegations'][index]['delegator_address'] == old_delegator_address:
      old['app_state']['staking']['delegations'][index]['delegator_address'] = new_delegator_address
      break;
    index = index + 1

  # 4. Replace old['app_state']['distribution']['delegator_starting_infos'][INDEX]['delegator_address']
  index = 0
  for delegator_starting_infos in old['app_state']['distribution']['delegator_starting_infos']:
    if old['app_state']['distribution']['delegator_starting_infos'][index]['delegator_address'] == old_delegator_address:
      old['app_state']['distribution']['delegator_starting_infos'][index]['delegator_address'] = new_delegator_address
      break;
    index = index + 1
  
  return

def change_account_bank_balance():
  # Get current account balance from old['app_state']['bank']['balances'][INDEX]['coins'][UATOM_INDEX]['amount']
  # Replace old['app_state']['bank']['balances'][INDEX]['coins'][UATOM_INDEX]['amount']
  index = 0
  uindex = 0
  for balances in old['app_state']['bank']['balances']:
    if old['app_state']['bank']['balances'][index]['address'] == new_delegator_address:
      for coins in old['app_state']['bank']['balances'][index]['coins']:
        if old['app_state']['bank']['balances'][index]['coins'][uindex]['denom'] == "uatom":
          old_balance_amount = old['app_state']['bank']['balances'][index]['coins'][uindex]['amount']
          old['app_state']['bank']['balances'][index]['coins'][uindex]['amount'] = int(old['app_state']['bank']['balances'][index]['coins'][uindex]['amount']) + 300000000
          old['app_state']['bank']['balances'][index]['coins'][uindex]['amount'] = str(old['app_state']['bank']['balances'][index]['coins'][uindex]['amount'])
        uindex = uindex +1
      break;
    index = index + 1

  # Correspondingly adjust old['app_state']['bank']['supply'][UATOM_INDEX]['amount']
  uindex = 0
  for supply in old['app_state']['bank']['supply']:
    if old['app_state']['bank']['supply'][uindex]['denom'] == "uatom":
      old['app_state']['bank']['supply'][uindex]['amount'] = int(old['app_state']['bank']['supply'][uindex]['amount']) + 6000000300000000
      old['app_state']['bank']['supply'][uindex]['amount'] = str(old['app_state']['bank']['supply'][uindex]['amount'])
      break;
    uindex = uindex +1

  return

# only works for delegators to binance
def change_delegation():
  # Replace old['app_state']['staking']['delegations'][0]['shares']
  # Replace old['app_state']['distribution']['delegator_starting_infos'][INDEX]['starting_info']['stake']
  index = 0
  for delegator_starting_infos in old['app_state']['distribution']['delegator_starting_infos']:
    if old['app_state']['distribution']['delegator_starting_infos'][index]['delegator_address'] == new_delegator_address:
      old['app_state']['distribution']['delegator_starting_infos'][index]['starting_info']['stake'] = format(float(old['app_state']['distribution']['delegator_starting_infos'][index]['starting_info']['stake']) + 6000000000000000, '.18f')
      old['app_state']['distribution']['delegator_starting_infos'][index]['starting_info']['stake'] = str(old['app_state']['distribution']['delegator_starting_infos'][index]['starting_info']['stake'])
      break;
    index = index + 1

  # Update old['app_state']['staking']['validators'][INDEX]['tokens']
  index = 0
  for validators in old['app_state']['staking']['validators']:
    if old['app_state']['staking']['validators'][index]['operator_address'] == validator_address:
      old['app_state']['staking']['validators'][index]['tokens'] = int(old['app_state']['staking']['validators'][index]['tokens']) + 6000000000000000
      old['app_state']['staking']['validators'][index]['tokens'] = str(old['app_state']['staking']['validators'][index]['tokens'])
      break;
    index = index + 1

  # Update old['app_state']['staking']['validators'][INDEX]['delegator_shares']
  index = 0
  for validators in old['app_state']['staking']['validators']:
    if old['app_state']['staking']['validators'][index]['operator_address'] == validator_address:
      old['app_state']['staking']['validators'][index]['delegator_shares'] = format(float(old['app_state']['staking']['validators'][index]['delegator_shares']) + 6000000000000000, '.18f')
      old['app_state']['staking']['validators'][index]['delegator_shares'] = str(old['app_state']['staking']['validators'][index]['delegator_shares'])
      break;
    index = index + 1

  # Update old['validators'][INDEX]['power']
  index = 0
  for validators in old['validators']:
    if old['validators'][index]['address'] == node2_old_address:
      old['validators'][index]['power'] = int(old['validators'][index]['power']) + 6000000000
      old['validators'][index]['power'] = str(old['validators'][index]['power'])
      break
    index = index + 1

  # Update old['app_state']['staking']['last_total_power']
  old['app_state']['staking']['last_total_power'] = int(old['app_state']['staking']['last_total_power']) + 6000000000
  old['app_state']['staking']['last_total_power'] = str(old['app_state']['staking']['last_total_power'])


  # Increase old['app_state']['bank']['balances'][INDEX]['coins'][UATOM_INDEX]['amount'] for the binance token_bonding_pool account with this address: cosmos1fl48vsnmsdzcv85q5d2q4z5ajdha8yu34mf0eh
  index = 0
  uindex = 0
  for balances in old['app_state']['bank']['balances']:
    if old['app_state']['bank']['balances'][index]['address'] == token_bonding_pool:
      for coins in old['app_state']['bank']['balances'][index]['coins']:
        if old['app_state']['bank']['balances'][index]['coins'][uindex]['denom'] == "uatom":
          old['app_state']['bank']['balances'][index]['coins'][uindex]['amount'] = int(old['app_state']['bank']['balances'][index]['coins'][uindex]['amount']) + 6000000000000000
          old['app_state']['bank']['balances'][index]['coins'][uindex]['amount'] = str(old['app_state']['bank']['balances'][index]['coins'][uindex]['amount'])
        uindex = uindex +1
      break;
    index = index + 1
  return

swap_validator()
swap_delegator()
change_account_bank_balance()
change_delegation()

json.dump(old, open(new_genesis_filename, 'w'), indent = True)