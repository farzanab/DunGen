"""The main game loop."""
# Reference: Roguelike Tutorial Revised
# https://github.com/TStand90/roguelike_tutorial_revised/blob/part7/engine.py

import libtcodpy as libtcod
from key_handler import handle_keys
from render import render_all, render, render_display
from fov import initialize_fov, recompute_fov
from states import GameStates
from messages import MessageLog, Message
import time

def main(map, entities, player, fov_radius, light_walls, health_boost, spell_dict):
	# defining game display parameters and creating consoles
	panel_height = 10
	screen_width = max(map.width, 80)
	screen_height = map.height + panel_height
	
	map_con = libtcod.console_new(map.width, map.height)
	panel_con = libtcod.console_new(screen_width, panel_height)
	
	fov_recompute = True
	fov_map = initialize_fov(map)
	
	msg_log = MessageLog(25, 50, panel_height - 1)
	
	gamestate = GameStates.PLAYER
	recompute_fov(fov_map, player.x, player.y, fov_radius, light_walls)
	while not libtcod.console_is_window_closed():
		render_all(map_con, panel_con, map, fov_map, fov_recompute, entities, player, msg_log, screen_width, screen_height, panel_height)
		
		# Keyboard input
		key = libtcod.console_wait_for_keypress(True)
		
		action = handle_keys(key, spell_dict, gamestate)
		
		move = action.get('move')
		fullscreen = action.get('fullscreen')
		exit = action.get('exit')
		display = action.get('display')
		spell = action.get('spell')
		dirn = action.get('dirn')
		
		turn_results = []
		
		if move and gamestate == GameStates.PLAYER:
			dx, dy = move
			dest_x, dest_y = player.x + dx, player.y + dy
			if not map.is_blocked(dest_x, dest_y):
				# attack if a monster is present else just move
				target = map.get_entity(dest_x, dest_y, entities[1:-1])
				if target:
					player.attack(target, turn_results)
				else:
					player.move(dx, dy, map)
					fov_recompute = True
					for entity in entities[:-1]:
						# get health_boost if standing on a corpse
						if entity.behav is None and entity.x == player.x and entity.y == player.y:
							player.hp += health_boost
							if player.hp > player.max_hp:
								player.hp = player.max_hp
							entities.remove(entity)
				
				# check if reached stairs
				if entities[0].x == player.x and entities[0].y == player.y:
					msg_log.add_msg(Message('You\'ve reached the stairs. Setting up new map.'.format(player.name), 'red'))
					render_all(map_con, panel_con, map, fov_map, fov_recompute, entities, player, msg_log, screen_width, screen_height, panel_height)
					time.sleep(5)
					return False
				
				gamestate = GameStates.ENEMY
				
		if spell is not None and gamestate == GameStates.PLAYER:
			# Check whether spell is directional
			if spell['dirn']:
				gamestate = GameStates.DIRECTION
				active_spell = spell
				turn_results.append({'message': Message('Targeting active for {}. Choose direction.'.format(active_spell['name']), 'silver')})
			else:
				if player.do_spell(spell, map, fov_map, entities, turn_results):
					gamestate = GameStates.ENEMY
					
		if gamestate == GameStates.DIRECTION and dirn:
			if dirn < 5:
				# execute only if valid direction selected
				if player.do_spell(active_spell, map, fov_map, entities, turn_results, dirn):
					gamestate = GameStates.ENEMY
				else:
					gamestate = GameStates.PLAYER
			else:
				turn_results.append({'message': Message('Targeting cancelled.', 'silver')})
				gamestate = GameStates.PLAYER
		
		if fullscreen:
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
			
		if exit:
			return True
			
		if display:
			render_display(map_con, panel_con, map, fov_map, entities, screen_width, screen_height, panel_height)
		
		for result in turn_results:
			message = result.get('message')
			dead = result.get('dead')
			
			if message:
				msg_log.add_msg(message)
				
			if dead:
				if dead is player:
					msg_log.add_msg(dead.die())
					gamestate = GameStates.DEAD
				else:
					msg_log.add_msg(dead.die())
					map.tiles[dead.x][dead.y].has_entity = 0
				
		if fov_recompute:
			recompute_fov(fov_map, player.x, player.y, fov_radius, light_walls)
			
					
		render_all(map_con, panel_con, map, fov_map, fov_recompute, entities, player, msg_log, screen_width, screen_height, panel_height)
		time.sleep(0.2)
		
		fov_recompute == False
		
		# enemy turn
		if gamestate == GameStates.ENEMY:
			for entity in entities[1:-1]:
				if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) and entity.behav:
					entity_results = []
					entity.take_turn(player, map, entity_results)
					for result in entity_results:
						message = result.get('message')
						dead = result.get('dead')
						
						if message:
							msg_log.add_msg(message)
							
						if dead:
							if dead is player:
								msg_log.add_msg(dead.die())
								gamestate = GameStates.DEAD
							else:
								msg_log.add_msg(dead.die())
							
				if gamestate == GameStates.DEAD:
					break
			else:			
				gamestate = GameStates.PLAYER
	return True