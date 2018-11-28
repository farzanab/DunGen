"""Contains functions for executing actions in monster behaviours."""

import sys


def action(monster, keyword, params, player, map, results):
	"""Call appropriate action function."""
	if keyword == 'move':
		action_move(monster, params, map)
	elif keyword == 'attack':
		action_attack(monster, params, player, results)
	elif keyword == 'move_towards':
		action_move_towards(monster, params, player, map)
	elif keyword == 'flee':
		action_flee(monster, params, player, map)
	elif keyword == 'move_random':
		action_move_random(monster, params, map)
			
def action_move(monster, params, map):
	"""
	Move monster by (dx,dy).
	
	monster: a Monster object
	params: a list of 2 integers [dx, dy]
	map: a GameMap object
	"""
	if len(params) != 2:
		sys.exit("Invalid number of arguments for 'move'")
	dx, dy = params[0], params[1]
	try:
		target = map.tiles[monster.x + dx][monster.y + dy]
		if not (target.has_entity or target.blocked):
			monster.move(dx, dy, map)
	except:
		pass
		
def action_attack(monster, params, player, results):
	"""
	Monster attacks player.
	
	monster: a Monster object
	params: a list of 0 [] or 1 integer [damage]
	player: a Player object
	results: list of results
	"""
	if not (len(params) == 0 or len(params) == 1):
		sys.exit("Invalid number of arguments for 'attack'")
	if len(params):
		monster.attack(player, results, params[0])
	else:
		monster.attack(player, results)
	
def action_move_towards(monster, params, player, map):
	"""
	Move monster one space towards player.
	
	monster: a Monster object
	params: a list of 0 integers []
	player: a Player object
	map: a GameMap object
	"""
	if len(params) != 0:
		sys.exit("Invalid number of arguments for 'move_towards'")
	monster.move_towards(player, map)
	
def action_flee(monster, params, player, map):
	"""
	Move monster one space away from player.
	
	monster: a Monster object
	params: a list of 0 integers []
	player: a Player object
	map: a GameMap object
	"""
	if len(params) != 0:
		sys.exit("Invalid number of arguments for 'flee'")
	monster.flee(player, map)
	
def action_move_random(monster, params, map):
	"""
	Move monster one space in a random direction.
	
	monster: a Monster object
	params: a list of 2 integers [dx, dy]
	map: a GameMap object
	"""
	if len(params) != 0:
		sys.exit("Invalid number of arguments for 'move_random'")
	monster.move_random(map)