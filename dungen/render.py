"""Functions for rendering to consoles."""
# Reference: Roguelike Tutorial Revised
# https://github.com/TStand90/roguelike_tutorial_revised/blob/part7/render_functions.py

import libtcodpy as libtcod
import time

colours = {'red': libtcod.red, 'light_red': libtcod.light_red, 'dark_red': libtcod.dark_red,
          'orange': libtcod.orange, 'light_orange': libtcod.light_orange, 'dark_orange': libtcod.dark_orange,
		  'yellow': libtcod.yellow, 'light_yellow': libtcod.light_yellow, 'dark_yellow': libtcod.dark_yellow,
		  'green': libtcod.green, 'light_green': libtcod.light_green, 'dark_green': libtcod.dark_green,
		  'cyan': libtcod.cyan, 'light_cyan': libtcod.light_cyan, 'dark_cyan': libtcod.dark_cyan,
		  'blue': libtcod.blue, 'light_blue': libtcod.light_blue, 'dark_blue': libtcod.dark_blue,
		  'violet': libtcod.violet, 'light_violet': libtcod.light_violet, 'dark_violet': libtcod.dark_violet,
		  'crimson': libtcod.crimson, 'light_crimson': libtcod.light_crimson, 'dark_crimson': libtcod.dark_crimson,
		  'grey': libtcod.grey, 'light_grey': libtcod.light_grey, 'dark_grey': libtcod.dark_grey,
		  'sepia': libtcod.sepia, 'light_sepia': libtcod.light_sepia, 'dark_sepia': libtcod.dark_sepia,
		  'brass': libtcod.brass, 'copper': libtcod.copper, 'gold': libtcod.gold, 'silver': libtcod.silver,
		  'black': libtcod.black, 'white':libtcod.white}
		  
def render_all(map_con, panel_con, map, fov_map, fov_recompute, entities, player, msg_log, screen_width, screen_height, panel_height):
	"""Wrapper function for calling functions for rendering."""
	render(map_con, panel_con, map, fov_map, fov_recompute, entities, player, msg_log, screen_width, screen_height, panel_height)
	libtcod.console_flush()
	clear_all(map_con, map, entities, fov_map)
	
def render_display(map_con, panel_con, map, fov_map, entities, screen_width, screen_height, panel_height):
	"""Display monster health levels, by changing colours."""
	for entity in entities[:-1]:
		if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) and entity.behav and not (entity.colour == 'black' or entity.colour == map.tiles[entity.x][entity.y].colour and entity.char == map.tiles[entity.x][entity.y].char) :
			frac = entity.hp / entity.max_hp
			if frac > 0.75:
				colour = 'dark_crimson'
			elif frac > 0.50:
				colour = 'light_red'
			elif frac > 0.25:
				colour = 'yellow'
			else:
				colour = 'blue'
			
			libtcod.console_set_default_foreground(map_con, colours[colour])
			libtcod.console_put_char(map_con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)
			
	x = 0 if map.width == screen_width else (screen_width - map.width)//2
	libtcod.console_blit(map_con, 0, 0, screen_width, screen_height, 0, x, 0)
	
	libtcod.console_set_default_foreground(panel_con, colours['dark_crimson'])
	libtcod.console_print(panel_con, 3, 5, 'HIGH')
	libtcod.console_set_default_foreground(panel_con, colours['light_red'])
	libtcod.console_print(panel_con, 3, 6, 'ABOVE HALF')
	libtcod.console_set_default_foreground(panel_con, colours['yellow'])
	libtcod.console_print(panel_con, 3, 7, 'BELOW HALF')
	libtcod.console_set_default_foreground(panel_con, colours['blue'])
	libtcod.console_print(panel_con, 3, 8, 'LOW')
	libtcod.console_blit(panel_con, 0, 0, screen_width, panel_height, 0, 0, map.height)
	libtcod.console_flush()
	time.sleep(4)
	
			

def render(map_con, panel_con, map, fov_map, fov_recompute, entities, player, msg_log, screen_width, screen_height, panel_height):
	"""Make changes to consoles based on the current conditions."""
	# Tiles only need to be rendered again if the player moved in the last turn.
	if fov_recompute:
		for y in range(map.height):
			for x in range(map.width):
				visible = libtcod.map_is_in_fov(fov_map, x, y)
				if visible or map.tiles[x][y].explored:
					char = map.tiles[x][y].char
					colour = colours.get(map.tiles[x][y].colour)
					libtcod.console_set_default_foreground(map_con, colour)
					libtcod.console_put_char(map_con, x, y, char, libtcod.BKGND_NONE)
					map.tiles[x][y].explored = True
				else:
					libtcod.console_put_char(map_con, x, y, ' ', libtcod.BKGND_NONE)
	
	# Display all entities taking care of corpses
	for entity in sorted(entities, key= lambda x: x.render_order, reverse = True):
		draw_entity(map_con, entity, fov_map)
	
	x = 0 if map.width == screen_width else (screen_width - map.width)//2
	libtcod.console_blit(map_con, 0, 0, screen_width, screen_height, 0, x, 0)
	
	# Working on the panel
	libtcod.console_clear(panel_con)
	libtcod.console_set_default_foreground(panel_con, colours['red'])
	libtcod.console_print(panel_con, 2, 3, 'HP: {}/{}'.format(player.hp, player.max_hp))
	libtcod.console_set_default_foreground(panel_con, colours['light_blue'])
	libtcod.console_print(panel_con, 15, 3, 'MANA: {}'.format(player.mana))
	
	y = 0
	for message in msg_log.messages:
		libtcod.console_set_default_foreground(panel_con, colours[message.colour])
		libtcod.console_print_ex(panel_con, msg_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
		y += 1
		
	libtcod.console_blit(panel_con, 0, 0, screen_width, panel_height, 0, 0, map.height)
	
def clear_all(con, map, entities, fov_map):
	"""Remove rendered entities."""
	for entity in entities:
		clear_entity(con, map, entity, fov_map)
		
def draw_entity(con, entity, fov_map):
	"""Draw entity if in field of view."""
	if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
		colour = colours.get(entity.colour)
		libtcod.console_set_default_foreground(con, colour)
		libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)
	
def clear_entity(con, map, entity, fov_map):
	"""Clear entity if in field of view."""
	if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
		libtcod.console_set_default_foreground(con, colours[map.tiles[entity.x][entity.y].colour])
		libtcod.console_put_char(con, entity.x, entity.y, map.tiles[entity.x][entity.y].char, libtcod.BKGND_NONE)