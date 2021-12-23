"""
This module helps you configure Cosmos Chain genesis files for testnets.
TODO: Docs for how to get a genesis file
"""

import json

BINANCE_VALIDATOR_ADDRESS = "cosmosvaloper156gqf9837u7d4c4678yt3rl4ls9c5vuursrrzf"
BINANCE_TOKEN_BONDING_POOL_ADDRESS = "cosmos1fl48vsnmsdzcv85q5d2q4z5ajdha8yu34mf0eh"


class GenesisTinker:
    """
    This class gives you primitives for tinkering with Cosmos chain Genesis Files
    """
    genesis = {}

    def load_genesis(self, path):
        """
        Loads a genesis file from the given path
        """

        with open(path, "r", encoding="utf8") as file:
            content = file.read()
            file.close()
            self.genesis = json.load(content)
        return self

    def save_genesis(self, path):
        """
        Save a modified genesis file back to JSON
        """
        with open(path, "w", encoding="utf8") as file:
            json.dump(self.genesis, file, indent=True)
        return self

    def swap_validator(self, old, new):
        """
        Swaps out an existing validator with a new one

        `old` and `new` should contain the properties `pub_key`, `address`, and `consensus_address`
        e.g.

        old = {
            "pub_key" : "Whatever",
            "address": "Something",
            "consensus_address": "cosmosvalcon..."
        }
        """
        staking_validators = self.genesis["app_state"]["staking"]["validators"]
        validators = self.genesis["validators"]
        missed_blocks = self.genesis["app_state"]["slashing"]["missed_blocks"]
        signing_infos = self.genesis["app_state"]["slashing"]["signing_infos"]

        for validator in validators:
            if validator["pub_key"]["value"] == old["pub_key"]:
                validator["pub_key"]["value"] = new["pub_key"]
            if validator["address"] == old["address"]:
                validator["address"] = new["address"]

        for validator in staking_validators:
            if validator["consensus_pubkey"]["key"] == old["pub_key"]:
                validator["consensus_pubkey"]["key"] = new["pub_key"]
                break

        for validator in missed_blocks:
            if validator["address"] == old["consensus_address"]:
                validator["address"] = new["address"]
                break

        for validator in signing_infos:
            if validator["address"] == old["consensus_address"]:
                validator["address"] = new["address"]
                break
        return self

    def swap_delegator(self, old_address, new_address):
        """
        Swaps out an exsiting delegator with a new one
        """

        accounts = self.genesis["app_state"]["auth"]["accounts"]
        balances = self.genesis["app_state"]["bank"]["balances"]
        delegations = self.genesis["app_state"]["staking"]["delegations"]
        starting_infos = self.genesis["app_state"]["distribution"]["delegator_starting_infos"]

        for account in accounts:
            try:
                if account["address"] == old_address:
                    account["address"] = new_address
                    break
            except KeyError:
                pass

        for balance in balances:
            if balance["address"] == old_address:
                balance["address"] = new_address
                break

        for delegation in delegations:
            if delegation["delegator_address"] == old_address:
                delegation["delegator_address"] = new_address
                break

        for info in starting_infos:
            if info["delegator_address"] == old_address:
                info["delegator_address"] = new_address
                break
        return self

    def increase_balance(self, address, increase=300000000, denom="uatom"):
        """
        Increases the balance of a person and also the overall supply of uatom
        """

        balances = self.genesis["app_state"]["bank"]["balances"]

        for balance in balances:
            if balance["address"] == address:
                for coin in balance["coins"]:
                    if coin["denom"] == denom:
                        old_amount = int(coin["amount"])
                        new_amount = old_amount + increase
                        coin["amount"] = str(new_amount)
                        break
                break

        self.increase_supply(increase, denom)
        return self

    def increase_supply(self, increase, denom="uatom"):
        """
        Increase the totall supply of coins of a given denomination
        """

        supplies = self.genesis["app_state"]["bank"]["supply"]

        for coin in supplies:
            if coin["denom"] == denom:
                old_amount = int(coin["amount"])
                new_amount = old_amount + increase
                coin["amount"] = str(new_amount)
                break
        return self

    def increase_delegation(self, delegator_address, operator_address, validator_address, increase=6000000000000000):
        """
        This function increases the power of a delegator and validator
        It seems to be dependant on binance, so be careful if you're changing stuff.
        """
        operator_address = BINANCE_VALIDATOR_ADDRESS
        token_bonding_pool_address = BINANCE_TOKEN_BONDING_POOL_ADDRESS

        starting_infos = self.genesis["app_state"]["distribution"]["delegator_starting_infos"]
        staking_validators = self.genesis["app_state"]["staking"]["validators"]
        validators = self.genesis["validators"]

        power_increase = (increase / 1000000)

        last_total_power = int(
            self.genesis['app_state']['staking']['last_total_power'])
        new_last_total_power = last_total_power + power_increase
        self.genesis["app_state"]["staking"]["last_total_power"] = str(
            new_last_total_power)

        for info in starting_infos:
            if info["delegator_address"] == delegator_address:
                old_stake = float(info["starting_info"]["stake"])
                new_stake = old_stake + increase
                info["starting_info"]["stake"] = str(
                    format(new_stake), ".18f")
                break

        for validator in staking_validators:
            if validator["operator_address"] == operator_address:
                old_amount = int(validator["tokens"])
                new_amount = old_amount + increase
                validator["tokens"] = str(new_amount)

                old_shares = float(validator["delegator_shares"])
                new_shares = old_shares + increase
                validator["delegator_address"] = str(
                    format(new_shares, ".18f"))
                break

        for validator in validators:
            if validator["address"] == validator_address:
                old_power = int(validator["power"])
                new_power = old_power + power_increase
                validator["power"] = str(new_power)

        # Increases the token boding pool for binance (???) and also the total supply
        self.increase_balance(token_bonding_pool_address, increase)
        return self
