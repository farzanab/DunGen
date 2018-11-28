"""Functions used in spells."""

import sys
import libtcodpy as libtcod

def transform(player, x, y, dirn):
	"""Rotate (x, y) with respect to player's coordinates based on direction."""
	x, y = x - player.x, y - player.y
	# {1: Right, 2: Down, 3: Left, 4: Up}
	if dirn == 1:
		x, y = x, y
	elif dirn == 2:
		x, y = -y, x
	elif dirn == 3:
		x, y = -x, -y
	elif dirn == 4:
		x, y = y, -x
	else:
		return None
	x, y = x + player.x, y + player.y
	return x, y

def action(player, keyword, params, name, map, entities, results, dirn):
	"""Call action based on keyword."""
	if dirn:
		params[0], params[1] = transform(player, params[0], params[1], dirn)
	if keyword == 'hit':
		action_hit(player, params, name, map, entities, results)
		
def action_hit(player, params, name, map, entities, results):
	"""Hit entity (if present) according to params."""
	if len(params) != 3:
		sys.exit("Invalid number of arguments for 'hit'")
	x, y, damage = params[0], params[1], params[2]
	try:
		player.hit(x, y, damage, name, map, entities, results)
	except:
		pass
	
def exec_func(keyword, params, map, fov_map, entities, dirn):
	"""Call function based on keyword."""
	if dirn:
		params[0], params[1] = transform(entities[-1], params[0], params[1], dirn)
	if keyword == 'is_monster':
		return is_monster(params, map, entities)
	elif keyword == 'is_wall':
		return is_wall(params, map)
	elif keyword == 'in_fov':
		return in_fov(params, fov_map)
	else:
		sys.exit("BOOM. Something went wrong.")
		
def is_monster(params, map, entities):
	"""Return 1 if monster else 0."""
	if len(params) != 2:
		sys.exit("Invalid number of arguments for 'is_monster'")
	try:
		return 1 if map.get_entity(params[0], params[1], entities[:-1]) else 0
	except:
		return 0
	
def is_wall(params, map):
	"""Return 1 if wall else 0."""
	if len(params) != 2:
		sys.exit("Invalid number of arguments for 'is_monster'")
	try:
		return 1 if map.tiles[params[0]][params[1]].blocked else 0
	except:
		return 0
		
def in_fov(params, fov_map):
	"""Return 1 if tile in field of vision else 0."""
	if len(params) != 2:
		sys.exit("Invalid number of arguments for 'in_fov'")
	try:
		return 1 if libtcod.map_is_in_fov(fov_map, params[0], params[1]) else 0
	except:
		return 0