from room import Room, dimension_gen, gen_room_dict, gen_num_rooms
from tile import Tile, gen_tile_dict
from entity import Entity, Monster, Player, Door
from obstacles import place_obstacle, place_edge
from random import randint, choice, random
from math import ceil
import sys, time

class GameMap:
	"""GameMap class with methods for map generation."""
	def __init__(self, spec_dict):
		self.width = 80
		self.height = 40
		gen_tile_dict(spec_dict)
		self.tiles = [[Tile('wall') for y in range(self.height)] for x in range(self.width)]
		self.rooms = []
		
	def makemap(self, spec_dict, monster_dict):
		map_type = spec_dict.get('map_type', 1)
		if map_type == 1:
			self.makemap1(spec_dict, monster_dict)
		elif map_type == 2:
			self.makemap2(spec_dict, monster_dict)		
	
	def makemap1(self, spec_dict, monster_dict):
		"""
		Use a (mostly) randomised algorithm to generate a map.
		
		Generate number of rooms of each type, and try to fit them.
		"""
		tries = []
		test = 0
		limit = 1
		tim1 = time.process_time()
		while test < limit:
			num_small, num_medium, num_large, is_random = gen_num_rooms(spec_dict, tries)
			
			if num_small is None:
				break
			test += 1
			if is_random:
				limit = 100
				limit2 = 250
			else:
				limit2 = 2000
			num_rooms = num_small + num_medium + num_large
			
			room_sizes = gen_room_dict(spec_dict, monster_dict, num_small, num_medium, num_large)
			for test2 in range(limit2):
				self.rooms =[]
				self.tiles = [[Tile('wall') for y in range(self.height)] for x in range(self.width)]
				for i in range(num_rooms):
					if i < num_large:
						size = 'large'
					elif i < num_large + num_medium:
						size = 'medium'
					else:
						size = 'small'
					trial = 0
					flag = True
					while flag:
						trial += 1
						if trial > 200:
							break
						width, height, max_monsters = dimension_gen(size, room_sizes)
						x = randint(0, self.width - width - 1)
						y = randint(0, self.height - height - 1)
					
						new_room = Room(x, y, width, height, max_monsters)
						
						for room in self.rooms:
							if new_room.intersect(room):
								break
						else:
							flag = False
							self.create_room(new_room)
							self.place_obstacles(new_room, size)
							if i > 0:
								x1, y1 = new_room.get_point()
								x2, y2 = self.rooms[-2].get_point()
								
								if randint(0, 1):
									self.hor_tun(x1, x2, y1)
									self.ver_tun(y1, y2, x2)
								else:
									self.ver_tun(y1, y2, x1)
									self.hor_tun(x1, x2, y2)
					if flag:
						break
				else:
					test = limit + 1
					break
		
		if test == limit or num_small is None:
			print(time.process_time() - tim1)
			sys.exit("Inadequate map size")	
		for y in range(self.height):
			for x in range(self.width):
				neighbours = []
				if x > 0 and y > 0:
					neighbours.extend([self.tiles[x-1][y-1], self.tiles[x][y-1], self.tiles[x-1][y]])
				if x < self.width - 1 and y > 0:
					neighbours.extend([self.tiles[x+1][y-1], self.tiles[x][y-1], self.tiles[x+1][y]])
				if x > 0 and y < self.height - 1:
					neighbours.extend([self.tiles[x-1][y+1], self.tiles[x][y+1], self.tiles[x-1][y]])
				if x < self.width - 1 and y < self.height - 1:
					neighbours.extend([self.tiles[x+1][y+1], self.tiles[x][y+1], self.tiles[x+1][y]])
				if all([tile.type == 'wall' for tile in neighbours]):
					self.tiles[x][y].set_blank()
	
	def makemap2(self, spec_dict, monster_dict):
		"""
		Create a grid based on the number of rooms and randomly select squares to put rooms in.
		"""
		num_small, num_medium, num_large, is_random = gen_num_rooms(spec_dict)
		num_rooms = num_small + num_medium + num_large
		room_sizes = gen_room_dict(spec_dict, monster_dict, num_small, num_medium, num_large)
		edge = room_sizes['large']['max']
		grid_width = ceil((2.1*num_rooms)**0.5)
		grid_height = ceil((0.525*num_rooms)**0.5)
		self.width = grid_width * edge
		self.height = grid_height * edge
		self.tiles = [[Tile('wall') for y in range(self.height)] for x in range(self.width)]
		grid = [[None for y in range(grid_height)] for x in range(grid_width)]
		for i in range(num_rooms):
			if i < num_large:
				size = 'large'
			elif i < num_large + num_medium:
				size = 'medium'
			else:
				size = 'small'
			while True:
				x, y = randint(0, grid_width - 1), randint(0, grid_height - 1)
				if grid[x][y] == None:
					break
			width, height, max_monsters = dimension_gen(size, room_sizes)
			start_x, start_y = x*edge + randint(0, edge - width), y*edge + randint(0, edge - height)
			room = Room(start_x, start_y, width, height, max_monsters)
			grid[x][y] = room
			self.create_room(room)
			self.place_obstacles(room, size)
		self.join_all_rooms2(grid)
		for y in range(self.height):
			for x in range(self.width):
				neighbours = []
				if x > 0 and y > 0:
					neighbours.extend([self.tiles[x-1][y-1], self.tiles[x][y-1], self.tiles[x-1][y]])
				if x < self.width - 1 and y > 0:
					neighbours.extend([self.tiles[x+1][y-1], self.tiles[x][y-1], self.tiles[x+1][y]])
				if x > 0 and y < self.height - 1:
					neighbours.extend([self.tiles[x-1][y+1], self.tiles[x][y+1], self.tiles[x-1][y]])
				if x < self.width - 1 and y < self.height - 1:
					neighbours.extend([self.tiles[x+1][y+1], self.tiles[x][y+1], self.tiles[x+1][y]])
				if all([tile.type == 'wall' for tile in neighbours]):
					self.tiles[x][y].set_blank()	
			
	def join_all_rooms(self, grid):
		"""Connect each room to all its nearest neighbours in four directions."""
		width = len(grid)
		height = len(grid[0])
		for x in range(width):
			for y in range(height):
				if grid[x][y]:
					room = grid[x][y]
					for i in range(x+1, width):
						if grid[i][y]:
							self.join_rooms(room, grid[i][y])
							break
					for j in range(y+1, height):
						if grid[x][j]:
							self.join_rooms(room, grid[x][j])
							break
							
	def join_all_rooms2(self, grid = None):
		"""Keep connecting rooms randomly until all are connected.""" 
		partitions = [[room] for room in self.rooms]
		while len(partitions) > 1:
			pos1 = randint(0, len(partitions)-1)
			pos2 = randint(0, len(partitions)-1)
			if pos1 == pos2:
				continue
			list1, list2 = partitions[pos1], partitions[pos2]
			room1, room2 = choice(list1), choice(list2)
			self.join_rooms(room1, room2)
			list1.extend(list2)
			del partitions[pos2]
	
	def join_rooms(self, room1, room2):
		"""Connect room1 and room2.""" 
		x1, y1 = room1.get_point()
		x2, y2 = room2.get_point()
		
		if randint(0, 1):
			self.hor_tun(x1, x2, y1)
			self.ver_tun(y1, y2, x2)
		else:
			self.ver_tun(y1, y2, x1)
			self.hor_tun(x1, x2, y2)

	def create_room(self, room):
		"""Set floor tiles in room."""
		self.rooms.append(room)
		for x in range(room.x1+1, room.x2):
			for y in range(room.y1 + 1, room.y2):
				self.tiles[x][y].set_type('floor')
				
	def hor_tun(self, x1, x2, y):
		"""Join (x1, y) and (x2, y)."""
		for x in range(min(x1, x2), max(x1, x2)+1):
			self.tiles[x][y].set_type('floor')
			
	def ver_tun(self, y1, y2, x):
		"""Join (x, y1) and (x, y2)."""
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.tiles[x][y].set_type('floor')
			
	def place_obstacles(self, room, size):
		"""Place obstacles in room based on size."""
		max_obstacles = {'small' : 5, 'medium': 7, 'large': 10}
		if random() < 0.15:
			place_edge(self, room)
		else:
			num = randint(max_obstacles[size] - 2, max_obstacles[size])
			for i in range(num):
				obstacle = choice(['square', 'L1', 'L2', 'L3', 'L4'])
				x, y = randint(room.x1 + 2, room.x2 - 3), randint(room.y1 + 2, room.y2 - 3)
				place_obstacle(self, x, y, obstacle)
			
	def place_entities(self, spec_dict, monster_dict, player_dict, entities):
		"""Place monsters and player on the map."""
		for monster_type in monster_dict.keys():
			for n in range(spec_dict.get(monster_type, 0)):
				while True:
					unfilled_rooms = [room for room in self.rooms if room.num_monsters != room.max_monsters]
					room = choice(unfilled_rooms)
					x, y = room.get_point()
					if self.tiles[x][y].has_entity or self.tiles[x][y].blocked:
						continue
					else:
						monster = Monster(monster_type, monster_dict[monster_type], x, y)
						entities.append(monster)
						room.num_monsters += 1
						self.tiles[x][y].has_entity = 1
						break
		flag = True				
		while flag:
			room = self.rooms[randint(0, len(self.rooms)-1)]
			x, y = room.get_point()
			if self.tiles[x][y].has_entity or self.tiles[x][y].blocked:
				continue
			else:
				flag = False
				player = Player(spec_dict.get('player', 'Player'), player_dict, x, y)
				entities.append(player)
				self.player = player
			
	def is_blocked(self, x, y):
		return self.tiles[x][y].blocked
		
	def get_entity(self, x, y, entities):
		"""Return living entity at (x, y)."""
		if self.tiles[x][y].has_entity:
			for entity in entities:
				if entity.x == x and entity.y == y and entity.char != '%':
					return entity
		return None
		
	def place_door(self, entities):
		"""Place door (stairs) on the map."""
		player = entities[-1]
		maxd = 0
		bigroom = None
		for room in self.rooms:
			d = abs(player.x - 0.5*(room.x1 + room.x2)) + abs(player.y - 0.5*(room.y1 + room.y2))
			if d > maxd:
				maxd = d
				bigroom = room
		x, y = bigroom.get_point()
		while self.tiles[x][y].blocked:
			x, y = bigroom.get_point()
		door = Door(x, y)
		entities.insert(0, door)