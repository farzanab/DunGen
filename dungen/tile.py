"""Class and function related to tile generation."""

import sys

tile_types = {
	'wall':{'blocked': True,'char': '#', 'colour':'white'},
	'floor':{'blocked': False, 'char': '.', 'colour':'white'},
	'obstacle':{'blocked': True, 'char': '8', 'colour':'white'}
}

def gen_tile_dict(spec_dict):
	"""Set tile_types based on spec_dict."""
	if spec_dict.get('wall_char'):
		tile_types['wall']['char'] = spec_dict['wall_char']
	if spec_dict.get('wall_colour'):
		tile_types['wall']['colour'] = spec_dict['wall_colour']
	if spec_dict.get('floor_char'):
		tile_types['floor']['char'] = spec_dict['floor_char']
	if spec_dict.get('floor_colour'):
		tile_types['floor']['colour'] = spec_dict['floor_colour']
	if spec_dict.get('obstacle_char'):
		tile_types['obstacle']['char'] = spec_dict['obstacle_char']
	if spec_dict.get('obstacle_colour'):
		tile_types['obstacle']['colour'] = spec_dict['obstacle_colour']

class Tile:
	def __init__(self, type):
		self.type = type
		type = tile_types[type]
		self.block_sight = self.blocked = type['blocked']
		if type['colour'] == 'black':
			self.block_sight = False
		self.char = type['char']
		self.colour = type['colour']
		self.has_entity = 0
		self.explored = False
		
	def set_type(self, type):
		self.type = type
		type = tile_types[type]
		self.block_sight = self.blocked = type['blocked']
		self.char = type['char']
		self.colour = type['colour']
		
	def set_blank(self):
		self.char = ' '