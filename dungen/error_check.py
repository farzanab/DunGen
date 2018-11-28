"""Error-checking functions to check all the generated dicts."""

import sys
from lexer import lex

valid_colours = ['red',    'light_red',    'dark_red',      'orange',  'light_orange',  'dark_orange', 
				 'yellow', 'light_yellow', 'dark_yellow',   'green',   'light_green',   'dark_green', 
				 'cyan',   'light_cyan',   'dark_cyan',     'blue',    'light_blue',    'dark_blue', 
				 'violet', 'light_violet', 'dark_violet',   'crimson', 'light_crimson', 'dark_crimson', 
				 'grey',   'light_grey',   'dark_grey',     'sepia',   'light_sepia',   'dark_sepia', 
				 'brass',  'copper',       'gold',          'silver',  'black',         'white'        ]

def check_errors(specs_dict, player_dict, monsters_dict, behav_dict, spell_dict):
	"""Check all dicts by calling appropriate functions."""
	check_specs(specs_dict, list(monsters_dict))
	check_player(player_dict)
	for monster in monsters_dict:
		check_monster(monster, monsters_dict[monster])
	check_all_brackets(behav_dict, spell_dict)
	
def check_specs(specs_dict, monsters):
	"""Check specs_dict for valid specs."""
	num_type = ['small',  'medium',  'large', 'health_boost'] + monsters # specs with non-negative integers
	num_type_p = ['small_min', 'small_max', 'medium_min', 'medium_max', 'large_min', 'large_max', 'fov'] # specs with positive integers
	char_type = ['wall_char', 'floor_char', 'obstacle_char'] # specs with characters
	colour_type = ['wall_colour', 'floor_colour', 'obstacle_colour'] # specs with colours
	other_valid = ['name', 'player'] # specs with strings
	for key in specs_dict:
		if key in num_type:
			if type(specs_dict[key]) == int:
				if specs_dict[key] < 0:
					sys.exit(key + " must be non-negative")
			else:
				sys.exit(key + " must be a non-negative integer")
		elif key in num_type_p:
			if type(specs_dict[key]) == int:
				if specs_dict[key] <= 0:
					sys.exit(key + " must be positive")
			else:
				sys.exit(key + " must be a positive integer")
		elif key in char_type:
			specs_dict[key] = str(specs_dict[key])
			if len(specs_dict[key]) != 1:
				sys.exit(key + " must be a single character")
		elif key in colour_type:
			if specs_dict[key] not in valid_colours:
				sys.exit(key + " must be one of the following colours:\n" + str(valid_colours))
		elif key == 'map_type':
			if specs_dict[key] != 1 and specs_dict[key] != 2:
				sys.exit("map_type must be either 1 or 2")
		elif key == 'rooms':
			if type(specs_dict[key]) == int:
				if specs_dict[key] <= 0:
					sys.exit(key + " must be positive")
			else:
				sys.exit(key + " must be a positive integer")
		elif key in other_valid:
			specs_dict[key] = str(specs_dict[key])
		else:
			sys.exit("Invalid key " + key)
	if specs_dict.get('rooms'):
		if specs_dict.get('small', 0) + specs_dict.get('medium', 0) + specs_dict.get('large', 0) > specs_dict['rooms']:
			sys.exit("Insufficient total number of rooms to fulfil given specifications")

def check_player(player_dict):
	"""Check player_dict for valid specs."""
	for key in player_dict:
		if key == 'char':
			player_dict[key] = str(player_dict[key])
			if len(player_dict[key]) != 1:
				sys.exit("player char must be a single character")
		elif key == 'colour':
			if player_dict['colour'] not in valid_colours:
				sys.exit("player colour must be one of the following colours:\n" + str(valid_colours))
		else:
			if type(player_dict[key]) == int:
				if player_dict[key] < 0:
					sys.exit("player " + key + " must be a non-negative integer")
			else:
				sys.exit("player " + key + " must be a non-negative integer")
			
				
def check_monster(name, monster_dict):
	"""Check monster_dict for valid specs."""
	for key in monster_dict:
		if key == 'char':
			monster_dict[key] = str(monster_dict[key])
			if len(monster_dict[key]) != 1:
				sys.exit(name + " char must be a single character")
		elif key == 'colour':
			if monster_dict['colour'] not in valid_colours:
				sys.exit(name + " colour must be one of the following colours:\n" + str(valid_colours))
		elif key == 'behav':
			pass
		else:
			if type(monster_dict[key]) == int:
				if monster_dict[key] < 0:
					sys.exit(name + " " + key + " must be a non-negative integer")
			else:
				sys.exit(name + " " + key + " must be a non-negative integer")
				
def check_expression(tokens):
	"""Check expression formed by tokens."""
	expression = ' '.join([str(token[0]) for token in tokens])
	count = 0
	for i in range(len(tokens)):
		if tokens[i][0] == '(':
			count += 1
		elif tokens[i][0] == ')':
			count -= 1
			if count < 0:
				sys.exit("Bad bracketting in " + expression)
		elif tokens[i][0] in ['!', '~']:
			if not (tokens[i+1][0] == '(' or tokens[i+1][1] in ['NUM', 'VAR', 'FUNC', 'STATS']):
				sys.exit("Bad expression " + expression)
		elif tokens[i][0] in ['|','&','+','-','*','/','==', '!=', '>=', '>', '<=', '<']:
			if i == 0 or i == len(tokens) - 1 or not ((tokens[i-1][0] == ')' or tokens[i-1][1] in ['NUM', 'VAR', 'STATS']) and 
					(tokens[i+1][0] == '(' or tokens[i+1][1] in ['NUM', 'VAR', 'FUNC', 'STATS'])):
				sys.exit("Bad expression " + expression)
		else:
			if (i > 0 and tokens[i-1][0] not in ['|','&','+','-','*','/','==', '!=', '>=', '>', '<=', '<', '!', '~', '(']) or \
			   (i < len(tokens) - 1 and tokens[i+1][0] not in ['|','&','+','-','*','/','==', '!=', '>=', '>', '<=', '<', ')']):
				sys.exit("Bad expression " + expression)
				
	if count != 0:
		sys.exit("Bad bracketting in " + expression)
		
def check_brackets(tokens):
	"""Check proper braces in tokens."""
	tokenlist = [token[0] for token in tokens]
	count = 0
	for token in tokenlist:
		if token == '{':
			count += 1
		elif token == '}':
			count -= 1
			if count < 0:
				return False
	return count == 0

def check_all_brackets(behav_dict, spell_dict):
	"""Check proper braces in all behaviours and spells."""
	for key in behav_dict:
		tokens = lex(behav_dict[key])
		if not check_brackets(tokens):
			sys.exit("Bad bracketting in behav " + key)
	for key in spell_dict:
		tokens = lex(spell_dict[key]['spell'])
		if not check_brackets(tokens):
			sys.exit("Bad bracketting in spell " + key)