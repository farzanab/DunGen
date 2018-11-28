"""Keyboard input function."""
# Reference: Roguelike Tutorial Revised
# https://github.com/TStand90/roguelike_tutorial_revised/blob/part7/input_handlers.py

import libtcodpy as libtcod
from states import GameStates

def handle_keys(key, spell_dict, gamestate):
	"""Return dict with player action."""
	if gamestate == GameStates.PLAYER:
		if spell_dict.get(chr(key.c)):
			return {'spell': spell_dict.get(chr(key.c))}

		if key.vk == libtcod.KEY_UP:
			return {'move': (0, -1)}
		if key.vk == libtcod.KEY_DOWN:
			return {'move': (0, 1)}
		if key.vk == libtcod.KEY_RIGHT:
			return {'move': (1, 0)}
		if key.vk == libtcod.KEY_LEFT:
			return {'move': (-1, 0)}
	
	if gamestate == GameStates.DIRECTION:
		if key.vk == libtcod.KEY_UP:
			return {'dirn': 4}
		elif key.vk == libtcod.KEY_DOWN:
			return {'dirn': 2}
		elif key.vk == libtcod.KEY_RIGHT:
			return {'dirn': 1}
		elif key.vk == libtcod.KEY_LEFT:
			return {'dirn': 3}
		else:
			return {'dirn': 5}
	
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	if key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
		
	if chr(key.c) == 'h':
		return {'display': True}
		
	return {}