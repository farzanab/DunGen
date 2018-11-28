"""Functions to generate spec_dict."""

import sys

def lex_specs(string):
	"""Generate list of tuples of specifications."""
	tokens = []
	i = 0
	while string.find('\n', i) != -1:
		end = string.find('\n', i)
		space = string.find(':', i, end)
		if space == -1:
				i = end +1
				continue
		tokens.append((string[i:space].strip().lower(), (string[space+1:end].strip())))
		i = end +1
	space = string.find(':', i)
	if space > -1:
		tokens.append((string[i:space].strip().lower(), string[space+1:].strip()))
	return tokens
	
def spec_process(tokens, monsters):
	"""Process tokens to generate spec_dict."""
	spec_list = ['name', 'rooms', 'small', 'small_min', 'small_max', 'medium', 'medium_min', 'medium_max', 'large_min', 'large_max', 'large',
	'player', 'wall_char', 'wall_colour', 'floor_char', 'floor_colour', 'obstacle_char', 'obstacle_colour', 'map_type', 'health_boost', 'fov'] + monsters
	spec_dict = {}
	for token in tokens:
		if token[0] in spec_list:
			if spec_dict.get(token[0]) is None:
				val = token[1]
				try:
					val = int(val)
				except ValueError:
					val = val
				spec_dict[token[0]] = val
			else:
				sys.exit("Repeated specifications! " + token[0])				
		else:
			sys.exit("Bad specification: " + token[0])
	return spec_dict

def spec_exec(string, monsters):
	"""Wrapper function to generate spec_dict from string."""
	tokens = lex_specs(string)
	return spec_process(tokens, monsters)