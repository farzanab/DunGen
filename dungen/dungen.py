from interpret import interpret
from generator import generate
from error_check import check_errors
import libtcodpy as libtcod 
import engine
import sys

file = sys.argv[1]
with open(file, 'r') as f:
	# processing the file and generating dicts
	string = f.read() 
	specs_dict, player_dict, monsters_dict, behav_dict, spell_dict = interpret(string)
check_errors(specs_dict, player_dict, monsters_dict, behav_dict, spell_dict)

# generating game components
map, entities, player = generate(specs_dict, player_dict, monsters_dict)
name = specs_dict.get('name', 'DunGen')

# setting up game window parameters and initialising
panel_height = 10
screen_width = max(map.width, 80)
screen_height = map.height + panel_height
	
libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(screen_width, screen_height, name)

# the level generation loop
while True:
	libtcod.console_clear(0)
	# engine.main(..) returns True only if an exit command is encountered
	if engine.main(map, entities, player, specs_dict.get('fov', 10), True, specs_dict.get('health_boost',1),spell_dict = spell_dict):
		break
		
	# modifying attributes for new level
	prev_health = player.hp
	max_health = player.max_hp + 5
	mana = player.mana + 2
	for m in monsters_dict:
		monsters_dict[m]['hp'] += 2
	map, entities, player = generate(specs_dict, player_dict, monsters_dict)
	player.hp, player.max_hp, player.mana = prev_health, max_health, mana