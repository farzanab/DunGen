from gamemap import GameMap

def generate(specs_dict, player_dict, monsters_dict):
	"""Create map, monsters and player based on dicts."""
	map = GameMap(specs_dict)
	map.makemap(specs_dict, monsters_dict)
	entities = []
	map.place_entities(specs_dict, monsters_dict, player_dict, entities)
	map.place_door(entities)
	player = entities[-1]
	return map, entities, player