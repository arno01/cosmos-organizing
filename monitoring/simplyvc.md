# PANIC Documentation
PANIC is running on `monitor.prod.earthball.xyz` under the `panic` user this server is also running the Prometheus stack.

## Add a user called `panic`
`useradd -s /bin/bash -m panic`

## Panic monitor (Debian 11)
## install Python 3 and required packages
`apt-get install python3-pip git libffi-dev redis`

## Install pipenv
su to `panic` user
`pip install pipenv`

Re-login as `panic` user

Run:
`git clone https://github.com/SimplyVC/panic_cosmos.git`
`cd panic_cosmos`
`pipenv sync`

## Config process
run `pipenv run python run_setup.py`
```
pipenv run python run_setup.py
Welcome to the PANIC alerter!
==== General
The first step is to set a unique identifier for the alerter. This can be any word that uniquely describes the setup being monitored. Uniqueness is very important if you are running multiple instances of the PANIC alerter, to avoid any possible Redis clashes. The name will only be used internally and will not show up in alerts.
Please insert the unique identifier:
hypha_vegatestnet_panic

==== Alerts
By default, alerts are output to a log file and to the console. Let's set up the rest of the alerts.
---- Telegram Alerts
Alerts sent via Telegram are a fast and reliable means of alerting that we highly recommend setting up. This requires you to have a Telegram bot set up, which is a free and quick procedure.
Do you wish to set up Telegram alerts? (Y/n)
y
Please insert your Telegram bot's API token:
2143589856:AAHSawrQ-xm3vf1tEUkV6_sTS3CjrOqDFxs
Successfully connected to Telegram bot.
Please insert the chat ID for Telegram alerts:
-781050859
Do you wish to test Telegram alerts now? (Y/n)
y
Test alert sent successfully.
Was the testing successful? (Y/n)
y
---- Email Alerts
Email alerts are more useful as a backup alerting channel rather than the main one, given that one is much more likely to notice a a message on Telegram or a phone call. Email alerts also require an SMTP server to be set up for the alerter to be able to send.
Do you wish to set up email alerts? (Y/n)
n
---- Twilio Alerts
Twilio phone-call alerts are the most important alerts since they are the best at grabbing your attention, especially when you're asleep! To set these up, you have to have a Twilio account set up, with a registered Twilio phone number and a verified phone number.The timed trial version of Twilio is free.
Do you wish to set up Twilio alerts? (Y/n)
n

==== Periodic alerts
---- Periodic alive reminder
The periodic alive reminder is a way for the alerter to inform its users that it is still running.
Do you wish to set up the periodic alive reminder? (Y/n)
y
Please enter the amount of seconds you want to pass for the periodic alive reminder. Make sure that you insert a positive integer.
300 
You will be reminded that the alerter is still running every 0h 5m 0s. Is this correct (Y/n) 
y
Would you like the periodic alive reminder to send alerts via Telegram? (Y/n)
y

==== Commands
---- Telegram Commands
Telegram is also used as a two-way interface with the alerter and as an assistant, allowing you to do things such as snooze phone call alerts and to get the alerter's current status from Telegram. Once again, this requires you to set up a Telegram bot, which is free and easy. You can reuse the Telegram bot set up for alerts.
NOTE: If you are running more than one instance of the PANIC alerter, do not use the same telegram bot as the other instance/s.
Do you wish to set up Telegram commands? (Y/n)
y
Please insert your Telegram bot's API token:
<token>
Successfully connected to Telegram bot.
Please insert the authorised chat ID:
<chat id>
Do you wish to test Telegram commands now? (Y/n)
y
Go ahead and send /ping to the Telegram bot.
Press ENTER once you are done sending commands...
Stopping the Telegram bot...
Was the testing successful? (Y/n)
y

==== Redis
Redis is used by the alerter to persist data every now and then, so that it can continue where it left off if it is restarted. It is also used to be able to get the status of the alerter and to have some control over it, such as to snooze Twilio phone calls.
Do you wish to set up Redis? (Y/n)
y
Please insert the Redis host IP: (default: localhost)

Please insert the Redis host port: (default: 6379)

Please insert the Redis password:

Do you wish to test Redis now? (Y/n)
y
Test completed successfully.

Setup finished.
Saved config/user_config_main.ini

==== Nodes
To produce alerts, the alerter needs something to monitor! The list of nodes to be included in the monitoring will now be set up. This includes validators, sentries, and any full nodes that can be used as a data source to monitor from the network's perspective. You may include nodes from multiple networks in any order; PANIC will figure out which network they belong to when you run it. Node names must be unique!
Do you wish to set up the list of nodes? (Y/n)
y
Unique node name:
vega-testnet_certus-one
Node's RPC url (typically http://NODE_IP:26657):
http://198.50.215.1:36657
Trying to connect to endpoint http://198.50.215.1:36657/health
Success.
Is this node a validator? (Y/n)
y
Successfully added validator node.
Do you want to add another node? (Y/n)
y
Unique node name:
vega-testnet_binance-sentry
Node's RPC url (typically http://NODE_IP:26657):
http://143.244.151.9:26657
Trying to connect to endpoint http://143.244.151.9:26657/health
Success.
Is this node a validator? (Y/n)
n
Successfully added full node.
Do you want to add another node? (Y/n)
y
Unique node name:
vega-testnet_coinbase
Node's RPC url (typically http://NODE_IP:26657):
http://198.50.215.1:46657
Trying to connect to endpoint http://198.50.215.1:46657/health
Success.
Is this node a validator? (Y/n)
y
Successfully added validator node.
Do you want to add another node? (Y/n)
n
Saved config/user_config_nodes.ini

==== GitHub Repositories
The GitHub monitor alerts on new releases in repositories. The list of GitHub repositories to monitor will now be set up.
Do you wish to set up the list of repos? (Y/n)
n
Saved config/user_config_repos.ini

Setup completed!
```

## Running PANIC
`pipenv sync`
`pipenv run python run_alerter.py`
```
Enabled alerting channels (general): ConsoleChannel, LogChannel, TelegramChannel
Enabled alerting channels (periodic alive reminder): ConsoleChannel, LogChannel, TelegramChannel
Trying to connect to http://198.50.215.1:36657/status
Success.
Trying to connect to http://143.244.151.9:26657/status
Success.
Trying to connect to http://198.50.215.1:46657/status
Success.
Node monitor (vega-testnet_certus-one) started.
Node monitor (vega-testnet_binance-sentry) started.
Node monitor (vega-testnet_coinbase) started.
Telegram commands started.
Network monitor (vega-testnet) started with 2 validator(s) and 1 full node(s).
Periodic alive reminder started.
```

## Setup systemd
~/panic_cosmos/start.sh
```
#!/bin/sh
cd /home/sysadmin/panic_cosmos
pipenv sync
pipenv run python run_alerter.py
```

`/etc/systemd/system/panic-cosmos.service`
```
[Unit]
Description=panic cosmos
After=network-online.target

[Service]
User=sysadmin
WorkingDirectory=/home/sysadmin/panic_cosmos
ExecStart=/home/sysadmin/panic_cosmos/start.sh
Restart=always
RestartSec=3
LimitNOFILE=4096
Environment="PATH=/home/sysadmin/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games"

[Install]
WantedBy=multi-user.target

```
```
sudo systemctl daemon-reload
sudo systemctl enable panic-cosmos.service # starts on boot
sudo systemctl start panic-cosmos.service # start process
```

## Adding new nodes
To add new, update and deleting nodes it is recommanded to use the PANIC Ansible playbook in this repo or `/usr/local/bin/config_panic_nodes.py` on the monitoring server

### To manually edit the config file
To add new nodes to be monitored edit `~/panic_cosmos/config/user_config_nodes.ini`

Add node blocks with incremental IDs `[node_3]`

Example of adding new nodes:
```
[node_3]
node_name = full-node-02
node_rpc_url = http://165.22.235.50:26657
node_is_validator = false
include_in_node_monitor = true
include_in_network_monitor = true

[node_4]
node_name = full-node-01
node_rpc_url = http://134.122.35.247:26657
node_is_validator = false
include_in_node_monitor = true
include_in_network_monitor = true

[node_5]
node_name = state-sync-test-01
node_rpc_url = http://143.198.41.219:26657
node_is_validator = false
include_in_node_monitor = true
include_in_network_monitor = true
```

After updating the config either manually or with the script you must restart PANIC to reload the config
`systemctl restart panic-cosmos`
