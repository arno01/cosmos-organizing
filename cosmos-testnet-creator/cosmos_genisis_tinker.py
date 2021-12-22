import json
import sys
import math


def load_file(path):
    file = open(path, "r", encoding="utf8")
    content = file.read()
    file.close()
    genesis = json.load(content)
    return genesis


def save_file(genesis, path):
    file = open(path, "w", encoding="utf8")
    json.dump(genesis, file, indent=True)


def swap_validator(genesis, old, new):
    '''
    `old` and `new` should contain the properties `pub_key`, `address`, and `consensus_address`
    e.g.

    old = {
        "pub_key" : "Whatever",
        "address": "Something",
        "consensus_address": "cosmosvalcon..."
    }
    '''
    staking_validators = genesis['app_state']['staking']['validators']
    validators = genesis['validators']
    missed_blocks = genesis['app_state']['slashing']['missed_blocks']
    signing_infos = genesis['app_state']['slashing']['signing_infos']

    for validator in validators:
        if validator['pub_key']['value'] == old['pub_key']:
            validator['pub_key']['value'] = new['pub_key']
        if validator['address'] == old['address']:
            validator['address'] = new['address']

    for validator in staking_validators:
        if validator['consensus_pubkey']['key'] == old['pub_key']:
            validator['consensus_pubkey']['key'] = new['pub_key']

    for validator in missed_blocks:
        if validator['address'] == old['consensus_address']:
            validator['address'] = new['address']

    for validator in signing_infos:
        if validator['address'] == old['consensus_address']:
            validator['address'] = new['address']
