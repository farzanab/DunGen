"""Functions for placing obstacles on the map at (x, y)."""

def place_obstacle(map, x, y, type):
	"""Call appropriate function. (x, y) is the upper left corner for that obstacle."""
	if type == 'square':
		place_square(map, x, y)
	elif type == 'L1':
		place_L1(map, x, y)
	elif type == 'L2':
		place_L2(map, x, y)
	elif type == 'L3':
		place_L3(map, x, y)
	elif type == 'L4':
		place_L4(map, x, y)

def place_edge(map, room):
	"""Set all tiles inside a room as obstacles except those next to walls."""
	for x in range(room.x1 + 2, room.x2 - 1):
		for y in range(room.y1 + 2, room.y2 - 1):
			map.tiles[x][y].set_type('obstacle')

def place_square(map, x, y):
	if not (map.tiles[x][y].blocked or map.tiles[x][y+1].blocked or 
			map.tiles[x+1][y].blocked or map.tiles[x+1][y+1].blocked):
		map.tiles[x][y].set_type('obstacle')
		map.tiles[x][y+1].set_type('obstacle')
		map.tiles[x+1][y].set_type('obstacle')
		map.tiles[x+1][y+1].set_type('obstacle')
		
def place_L1(map, x, y):
	if not (map.tiles[x][y+1].blocked or 
			map.tiles[x+1][y].blocked or map.tiles[x+1][y+1].blocked):
		map.tiles[x][y+1].set_type('obstacle')
		map.tiles[x+1][y].set_type('obstacle')
		map.tiles[x+1][y+1].set_type('obstacle')
		
def place_L2(map, x, y):
	if not (map.tiles[x][y].blocked or 
			map.tiles[x+1][y].blocked or map.tiles[x+1][y+1].blocked):
		map.tiles[x][y].set_type('obstacle')
		map.tiles[x+1][y].set_type('obstacle')
		map.tiles[x+1][y+1].set_type('obstacle')
		
def place_L3(map, x, y):
	if not (map.tiles[x][y].blocked or map.tiles[x][y+1].blocked or 
			map.tiles[x+1][y+1].blocked):
		map.tiles[x][y].set_type('obstacle')
		map.tiles[x][y+1].set_type('obstacle')
		map.tiles[x+1][y+1].set_type('obstacle')
		
def place_L4(map, x, y):
	if not (map.tiles[x][y].blocked or map.tiles[x][y+1].blocked or 
			map.tiles[x+1][y].blocked):
		map.tiles[x][y].set_type('obstacle')
		map.tiles[x][y+1].set_type('obstacle')
		map.tiles[x+1][y].set_type('obstacle')