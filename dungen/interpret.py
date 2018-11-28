from define_funcs import define, lex_define
from specs_funcs import spec_exec
import sys, re

def split_blocks(string):
	"""Break string into blocks starting with define."""
	key = re.compile(r'[ \n\t]+define[ \n\t]+')
	blocks = key.split(string)
	blocks = [blocks[0]] + ['define ' + blocks[i] for i in range(1, len(blocks))]
	return blocks
	
def interpret(string):
	blocks = split_blocks(string)
	try:
		blocks = [blocks[0]] + sorted([lex_define(block) for block in blocks[1:]], key = lambda block: ['player', 'monster', 'behav', 'spell'].index(block[1]))
	except:
		sys.exit("Invalid definition")
	default_player_dict = {'char':'@', 'colour': 'white', 'hp': 20, 'attack': 20, 'defence': 10, 'mana': 5}
	behav_dict = {'scaredycat':'flee();', 'brave':'if {player_distance < 2} {attack();} {move_towards();}', 'basic': 'if {health > maxhealth /2}{if {player_distance < 2} {attack();} {move_towards();}} {flee();}'}
	monsters_dict = {'monster':{'char': 'm', 'colour':'green', 'hp': 5, 'behav': behav_dict['basic'], 'attack': 10, 'defence': 5}}
	player_dict = {}
	spell_dict = {}
	while len(blocks) > 1:
		block = blocks.pop()
		define(block, player_dict, monsters_dict, behav_dict, spell_dict)
	spec_dict = spec_exec(blocks[0], list(monsters_dict.keys()))
	# if player not defined
	if len(player_dict) == 0:
		player_dict = default_player_dict
	return spec_dict, player_dict, monsters_dict, behav_dict, spell_dict