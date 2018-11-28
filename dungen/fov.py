"""Field of Vision functions."""
# Source: Roguelike Tutorial Revised
# https://github.com/TStand90/roguelike_tutorial_revised/blob/part7/fov_functions.py

import libtcodpy as libtcod

def initialize_fov(map):
	"""Set up fov_map."""
	fov_map = libtcod.map_new(map.width, map.height)
	
	for y in range(map.height):
		for x in range(map.width):
			libtcod.map_set_properties(fov_map, x, y, not map.tiles[x][y].block_sight, not map.tiles[x][y].block_sight)
			
	return fov_map
			
def recompute_fov(fov_map, x, y, radius, light_walls = True, algorithm = 0):
	libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)