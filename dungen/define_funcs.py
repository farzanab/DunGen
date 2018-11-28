"""Contains functions to process definition blocks in the specs file."""

import re
import sys

def lex_define(string):
	"""
	Break string into tokens that can be processed by other functions.
	Generates tuples of specifications where possible.
	"""
	tokens = []
	index = string.find('\n')
	first_line = string[:index]
	string = string[index+1:]
	tokens = re.compile('\S+').findall(first_line)
	tokens = [token.lower() for token in tokens]
	# process first line and check for errors
	if len(tokens) > 3 or tokens[0] != 'define':
		sys.exit("Bad definition: " + first_line)
		
	# check for type of definition
	if tokens[1] == 'behav':
		# behav definitions don't have any specifications, just 'code'
		tokens.append(string)
	elif tokens[1] == 'spell':
		# spell definitions have a few specifications followed by 'code'
		i = 0
		while string.find(':', i) != -1:
			space = string.find(':', i)
			end = string.find('\n', space)
			tokens.append((string[i:space].strip().lower(), string[space+1:end].strip()))
			i = end + 1
		tokens.append(string[i:].strip())
	else:
		# monster and player definitions only have specifications
		i = 0
		while string.find('\n', i) != -1:
			end = string.find('\n', i)
			space = string.find(':', i, end)
			if space == -1:
				i = end +1
				continue
			tokens.append((string[i:space].strip().lower(), string[space+1:end].strip()))
			i = end +1
		space = string.find(':', i)
		if space != -1:
			tokens.append((string[i:space].strip().lower(), string[space+1:].strip()))
	return tokens
	
def def_player(tokens, player_dict):
	"""Store player specifications in player_dict.""" 
	player_dict_default = {'char':'@', 'colour': 'white', 'hp': 20, 'attack': 20, 'defence': 10, 'mana': 5}
	keys = player_dict_default.keys()
	for token in tokens:
		# Check for valid specs
		if token[0] in keys:
			# Check for repeated specs
			if player_dict.get(token[0]) is None:
				val = token[1]
				try:
					val = int(val)
				except ValueError:
					val = val
				player_dict[token[0]] = val
			else:
				sys.exit("Repeated specifications in player: " + token[0])				
		else:
			sys.exit("Bad specification in player: " + token[0])
	# Store default values for undefined specs in player_dict
	for key in keys:
		if player_dict.get(key) is None:
			player_dict[key] = player_dict_default[key]

def def_monster(name, tokens, monsters_dict, behav_dict):
	"""Store monster specifications in monsters_dict."""
	monster_default = {'char': 'm', 'colour':'green', 'hp': 5, 'behav': None, 'attack': 10, 'defence': 5}
	monster = {}
	keys = monster_default.keys()
	for token in tokens:
		# Check for valid specs
		if token[0] in keys:
			# Check for repeated specs
			if monster.get(token[0]) is None:
				if token[0]=='behav':
					try:
						val = behav_dict[token[1]]
					except:
						sys.exit("Undefined behaviour: " + token[1])
				else:
					val = token[1]
					try:
						val = int(val)
					except ValueError:
						val = val
				monster[token[0]] = val
			else:
				sys.exit("Repeated specifications in " + name + ":" + token[0])			
		else:
			sys.exit("Bad specification in " + name + ": " + token[0])
	# Store default values for undefined specs in monster_dict		
	for key in keys:
		if monster.get(key) is None:
			monster[key] = monster_default[key]
	
	monsters_dict[name]=monster
	
def def_behav(name, string, behav_dict):
	"""Store behaviour code in behav_dict."""
	if behav_dict.get(name) is None:
		behav_dict[name] = string
	else:
		sys.exit("Repeated behaviour: " + name)
		
def def_spell(key, tokens, string, spell_dict):
	"""Store spell specifications and code in spell_dict."""
	defaults = {'cost' : 0, 'dirn' : False, 'name':'spell'}
	# Check for invalid key
	if len(key) != 1:
		sys.exit("Invalid key " + key)
	spell_dict[key] = {}
	for token in tokens:
		if token[0] in defaults:
			if (spell_dict[key]).get(token[0]) is None:
				if token[0] == 'dirn':
					if token[1] in ['true', 'yes', 'y'] + ['false', 'no', 'n']:
						if token[1] in ['true', 'yes', 'y']:
							spell_dict[key]['dirn'] = True
						else:
							spell_dict[key]['dirn'] = False
					else:
						sys.exit("Invalid specification for dirn " + token[1] + ". dirn must be one of 'true', 'yes', 'y', 'false', 'no', 'n'")
				elif token[0] == 'cost':
					try:
						spell_dict[key]['cost'] = int(token[1])
					except:
						sys.exit("Invalid cost for spell {}.".format(key))
					if spell_dict[key]['cost'] < 0:
						sys.exit(key + " cost must be a non-negative integer")
				else:
					spell_dict[key]['name'] = token[1]
			else:
				sys.exit("Repeated specification in spell "+ key + ": "+token[0])
		else:
			sys.exit("Bad specification in spell "+ key + ": " + token[0])
	spell_dict[key]['spell'] = string
	for spec in defaults:
		if spec not in spell_dict[key]:
			spell_dict[key][spec] = defaults[spec]
		
def define(tokens, player_dict, monsters_dict, behav_dict, spell_dict):
	"""Call appropriate functions with he right arguments."""
	if tokens[1] == 'behav':
		def_behav(tokens[2], tokens[3], behav_dict)
	elif tokens[1] == 'monster':
		def_monster(tokens[2], tokens[3:], monsters_dict, behav_dict)
	elif tokens[1] == 'player':
		def_player(tokens[2:], player_dict)
	elif tokens[1] == 'spell':
		def_spell(tokens[2], tokens[3:-1], tokens[-1], spell_dict)