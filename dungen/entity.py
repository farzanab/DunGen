"""Contains classes Entity, and its subclasses Player and Monster."""

from messages import Message
import exec_funcs
import exec_spells
import math, random

# {1: Right, 2: Down, 3: Left, 4: Up}
dirn_dict = {
			 1: (1, 0),
			 2: (0, 1),
			 3: (-1, 0),
			 4: (0, -1)
			}

class Entity(object):
	"""Basic Entity class with its attributes."""
	def __init__(self, name, dict, x, y):
		self.x = x
		self.y = y
		self.name = name
		self.char = dict['char']
		self.colour = dict['colour']
		self.hp = self.max_hp = dict['hp']
		self.attacks = dict.get('attack', 10)
		self.defence = dict.get('defence', 5)
		self.render_order = 1
		
	def __str__(self):
		return self.name
		
	def move(self, dx, dy, map):
		"""Move self by (dx, dy)."""
		if self.x + dx < map.width and self.y + dy < map.height and self.x + dx >= 0 and self.y + dy >= 0:
			x = self.x
			y = self.y
			map.tiles[x][y].has_entity = 0
			x = x + dx
			y = y + dy
			map.tiles[x][y].has_entity = 1
			self.x = x
			self.y = y
		
	def take_damage(self, damage, results):
		"""Reduce own health by damage and check if dead."""
		self.hp -= damage
		
		if self.hp <= 0:
			self.hp = 0
			results.append({'dead': self})
		
	def attack(self, target, results, damage = None):
		"""Attack target possibly causing some damage."""
		if not damage:
			damage = self.attacks - target.defence
		damage = damage	+ random.randint(-1, 1)
		if damage > 0:
			results.append({'message': Message('{} attacks {} for {} hitpoints.'.format(self.name, target.name, damage), 'light_red')})
			target.take_damage(damage, results)			
		else:
			results.append({'message': Message('{} attacks {} but fails miserably.'.format(self.name, target.name), 'yellow')})
			
			
class Monster(Entity):
	def __init__(self, name, dict, x, y):
		Entity.__init__(self, name, dict, x, y)
		self.behav = dict.get('behav', None)
		
	def take_turn(self, player, map, results):
		stats = self.getstats(player)
		exec_funcs.exec1(self, self.behav, stats, player, map, results)
		
	def move_random(self, map):
		"""Move one space in a random direction."""
		x, y = self.x, self.y
		c = 0
		while map.tiles[x][y].blocked or map.tiles[x][y].has_entity:
			if c == 10:
				dx, dy = 0, 0
				break
			dx, dy = dirn_dict[random.randint(1,4)]
			if self.x + dx < map.width and self.y + dy < map.height and self.x + dx >= 0 and self.y + dy >= 0:
				x, y = self.x + dx, self.y + dy
			c += 1
		self.move(dx, dy, map)
		
	def move_towards(self, target, map):
		"""Move one space towards target."""
		dirn_list = self.get_dirn(target.x, target.y)
		dx, dy = 0, 0
		i = 0
		while map.tiles[self.x+dx][self.y+dy].blocked or map.tiles[self.x+dx][self.y+dy].has_entity:
			if i == 4:
				dx, dy = 0, 0
				break
			dx, dy = dirn_dict[dirn_list[i]]
			i += 1
			
		self.move(dx, dy, map)
		
	def flee(self, target, map):
		"""Move one space away from target."""
		dirn_list = self.get_dirn(target.x, target.y)
		dx, dy = 0, 0
		i = 3
		while map.tiles[self.x+dx][self.y+dy].blocked or map.tiles[self.x+dx][self.y+dy].has_entity:
			if i == -1:
				dx, dy = 0, 0
				break
			dx, dy = dirn_dict[dirn_list[i]]
			i -= 1
		self.move(dx, dy, map)
		
	def distance(self, target):
		"""Minimum number of steps required for self to reach target."""
		return abs(self.x - target.x) + abs(self.y - target.y)
	
	def get_dirn(self, x, y):
		"""Return list of directions in decreasing order of preference in order to reach (x, y)."""
		dx = x - self.x
		dy = y - self.y
		dirn = math.atan2(dy,dx)
		if 0 <= dirn < math.pi/4:
			dirn_list = [1, 2, 4, 3]
		elif math.pi/4 <= dirn < math.pi/2:
			dirn_list = [2, 1, 3, 4]
		elif math.pi/2 <= dirn < math.pi*3/4:
			dirn_list = [2, 3, 1, 4]
		elif math.pi*3/4 <= dirn <= math.pi:
			dirn_list = [3, 2, 4, 1]
		elif -math.pi <= dirn < -math.pi*3/4:
			dirn_list = [3, 4, 2, 1]
		elif -math.pi*3/4 <= dirn < -math.pi/2:
			dirn_list = [4, 3, 1, 2]
		elif -math.pi/2 <= dirn < -math.pi/4:
			dirn_list = [4, 1, 3, 2]
		else:
			dirn_list = [1, 4, 2, 3]
			
		return dirn_list	
		
	def die(self):
		self.char = '%'
		self.colour = 'red'
		self.behav = None
		self.render_order = 2
		return Message('{} is dead.'.format(self.name), 'violet')
		
	def getstats(self, player):
		"""Return dict of stats required to take turn."""
		return {'health': self.hp,
				'maxhealth': self.max_hp,
				'phealth': player.hp,
				'maxphealth': player.max_hp,
				'player_distance':self.distance(player)}
				
	def update_stats(self, player, stats, results):
		"""Update actual attributes during a turn."""
		player.hp = stats['phealth']
		self.hp = stats['health']
		if player.hp <= 0:
			player.hp = 0
			results.append({'dead': player})
		elif self.hp <= 0:
			self.hp = 0
			results.append({'dead': self})
			
class Player(Entity):
	def __init__(self, name, dict, x, y):
		Entity.__init__(self, name, dict, x, y)
		self.mana = dict['mana']
		
	def do_spell(self, dict, map, fov_map, entities, results, dirn=None):
		"""Cast spell and check if directional."""
		if self.mana >= dict['cost']:
			exec_spells.exec1(self, dict['spell'], dict['name'], map, fov_map, entities, results, dirn)
			self.mana -= dict['cost']
			return True
		else:
			results.append({'message': Message('You don\'t have enough mana to cast {}.'.format(dict['name']), 'white')})
			return False
		
	def hit(self, x, y, damage, name, map, entities, results):
		"""Long range 'attack' for spells."""
		target = map.get_entity(x, y, entities)
		if target:
			results.append({'message': Message('The {} hits {} for {} hitpoints.'.format(name, target.name, damage), 'crimson')})
			target.take_damage(damage, results)
		else:
			results.append({'message': Message('Oops, {} does nothing.'.format(name), 'white')})
	
	def die(self):
		self.char = '%'
		self.colour = 'dark_crimson'
		return Message('Damn, you died!', 'light_grey')
		
	def getstats(self):
		"""Return dict of required stats for spells."""
		return {'health': self.hp,
				'maxhealth': self.max_hp,
				'mana': self.mana}
				
	def update_stats(self, stats, results):
		"""Update actual attributes during a spell."""
		self.hp = stats['health']
		self.max_hp = stats['maxhealth']
		self.mana = stats['mana']
		if self.mana > 99:
			self.mana = 99
		if self.max_hp > 999:
			self.max_hp = 999
		if self.hp > self.max_hp:
			self.hp = self.max_hp
		if self.hp <= 0:
			self.hp = 0
			results.append({'dead': self})
			
class Door(Entity):
	def __init__(self, x, y):
		self.char = 's'
		self.colour = 'gold'
		self.x = x
		self.y = y
		self.render_order = 1
		self.behav = 1234