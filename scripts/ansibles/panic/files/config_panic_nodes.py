#!/usr/bin/env python3

import configparser, sys, math

# print useage
def print_usage():
	print('Usage:   ./config_panic_nodes.py [config_file] add [node name] [node_rpc_url] [node_rpc_port] [node_is_validator] [include_in_node_monitor] [include_in_network_monitor]')
	print('Example: ./config_panic_nodes.py user_config_nodes.ini add full-node-01.vega-testnet full-node-01.vega-testnet.prod.earthball.xyz 26657 0 1 1')
	print('Example: ./config_panic_nodes.py user_config_nodes.ini del full-node-01.vega-testnet')
	print('add: adds and update existing nodes to PANIC config')
	print('del: deletes existing nodes in PANIC config')

# check number of args matches
if len(sys.argv) != 4 and len(sys.argv) != 9:
	print('Invald number of arguments')
	print_usage()
	sys.exit(1)

filename = sys.argv[1]
operation = sys.argv[2]

# check operations args
if operation == 'add' and len(sys.argv) != 9:
	print('Invald number of arguments for add operation')
	print_usage()
	sys.exit(1)
elif operation == 'del' and len(sys.argv) != 4:
	print('Invald number of arguments for del operation')
	print_usage()
	sys.exit(1)
elif operation != 'del' and operation != 'add':
	print('Invalid operation. Must be add or del')
	print_usage()
	sys.exit(1)

node_found = 0
node_count = 0
config = configparser.ConfigParser()
config.read(filename)

new_config = configparser.ConfigParser()
def reorder_nodes():
	reorder_count = 0
	for node in config:
		try:
			if (node != 'DEFAULT'):
				new_node_id = ("node_" + str(reorder_count))
				new_config[new_node_id] = {}
				new_config[new_node_id]['node_name'] = config[node]['node_name']
				new_config[new_node_id]['node_rpc_url'] = config[node]['node_rpc_url']
				new_config[new_node_id]['node_is_validator'] = config[node]['node_is_validator']
				new_config[new_node_id]['include_in_node_monitor'] = config[node]['include_in_node_monitor']
				new_config[new_node_id]['include_in_network_monitor'] = config[node]['include_in_network_monitor']
				reorder_count = reorder_count + 1
		except:
			KeyError
	reorder_nodes.reorder_count = reorder_count
	return

# add and update section
if operation == 'add':
	new_node_name = sys.argv[3]
	new_node_rpc_url = sys.argv[4]
	new_node_rpc_port = sys.argv[5]
	new_node_is_validator = sys.argv[6]
	new_include_in_node_monitor = sys.argv[7]
	new_include_in_network_monitor = sys.argv[8]

	# check if node already exists and update its values and if not add a new entry
	for node in config:
		try:
			if config[node]['node_name'] == new_node_name:
				print("Node:", config[node]['node_name'], " already exists in key:", node)
				print('Updating the values')
				config[node]['node_rpc_url'] = ("http://" + new_node_rpc_url + ":" + new_node_rpc_port)
				if new_node_is_validator == '1':
					config[node]['node_is_validator'] = 'true'
				else:
					config[node]['node_is_validator'] = 'false'

				if new_include_in_node_monitor == '1':
					config[node]['include_in_node_monitor'] = 'true'
				else:
					config[node]['include_in_node_monitor'] = 'false'
				
				if new_include_in_network_monitor == '1':
					config[node]['include_in_network_monitor'] = 'true'
				else:
					config[node]['include_in_network_monitor'] = 'false'
				node_found = 1
			node_count = node_count + 1
		except:
			KeyError

	# if node_found is set write file and quit else add a new node
	if node_found == 1:
		with open(filename, 'w') as configfile:
			config.write(configfile)
			sys.exit(0)
	else:
		print("Node not found adding to the config")
		reorder_nodes()
		reorder_count = reorder_nodes.reorder_count
		new_node_id = ("node_" + str(reorder_count))
		new_config[new_node_id] = {}
		new_config[new_node_id]['node_name'] = new_node_name
		new_config[new_node_id]['node_rpc_url'] = ("http://" + new_node_rpc_url + ":" + new_node_rpc_port)
		if new_node_is_validator == '1':
			new_config[new_node_id]['node_is_validator'] = 'true'
		else:
			new_config[new_node_id]['node_is_validator'] = 'false'

		if new_include_in_node_monitor == '1':
			new_config[new_node_id]['include_in_node_monitor'] = 'true'
		else:
			new_config[new_node_id]['include_in_node_monitor'] = 'false'
		
		if new_include_in_network_monitor == '1':
			new_config[new_node_id]['include_in_network_monitor'] = 'true'
		else:
			new_config[new_node_id]['include_in_network_monitor'] = 'false'

		with open(filename, 'w') as configfile:
			new_config.write(configfile)
			sys.exit(0)

# delete section
elif operation == 'del':
	node_count = 0
	del_node_name = sys.argv[3]
	for node in config:
		try:
			if config[node]['node_name'] == del_node_name:
				node_found = 1
				node_num = node_count
			node_count = node_count + 1
		except:
			KeyError

	if node_found != 1:
		print('Cannot find node:', del_node_name, 'to delete')
		sys.exit(1)
	else:
		print('Found node:', del_node_name, 'deleting...')
		node_id = ("node_" + str(node_num))
		config.remove_section(node_id)
		reorder_nodes()
		with open(filename, 'w') as configfile:
				new_config.write(configfile)
				sys.exit(0)
