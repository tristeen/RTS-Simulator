#import uuid
from misc import mTimer
import random
import copy
import operator
from misc.mLogger import log
from misc import utils

UNIT_NONE = {'name': 'UNIT_NONE', 'type': 0, 'desc': 'o', 'maxhp': 1, 'price': float('INF')}
UNIT_SOLDIER = {'name': 'UNIT_SOLDIER', 'type': 1, 'desc': '$', 'maxhp': 2, 'attackable': True, 'moveable': True, 'speed': 1, 'attack_range': 1, 'attack_power': 2, 'price': 5, 'population': 2}
UNIT_BASE = {'name': 'UNIT_BASE', 'type': 2, 'desc': '^', 'maxhp': 20, 'produceable': True, 'product': (1, 3), 'price': 20, 'population': 5}
UNIT_WORKER = {'name': 'UNIT_WORKER', 'type': 3, 'desc': '@', 'maxhp': 1, 'moveable': True, 'speed': 1, 'produceable': True, 'product': (2,), 'attack_power': 1, 'attackable': True, 'attack_range': 1, 'harvestable': True, 'harvest_count': 2, 'harvest_range': 1, 'price': 2, 'population': 1}
UNIT_RES = {'name': 'UNIT_RES', 'type': 4, 'desc': '*', 'maxhp': 10000,  'res_count': 60, 'price': float('INF')}
UNITS = {0: UNIT_NONE, 1: UNIT_SOLDIER, 2: UNIT_BASE, 3: UNIT_WORKER, 4: UNIT_RES}

class Unit(object):

	def __init__(self, d):
		self.lock_ = False
		self.camp_ = 0
		self.res_ = 0
		self.type_ = 0
		self.dying_ = False
		if type(d) is int:
			self.type_ = d
		else:
			self.from_dict(d)
			#self.type_ = self.type
		if 'maxhp' in self.__dict__:
			raise Exception()
		if 'hp_' not in self.__dict__:
			self.hp_ = UNITS[self.type_]['maxhp']
		if 'id' not in self.__dict__:
			self.id = utils.gen_id()

	def __getattr__(self, name):
		return UNITS[self.type_][name]

	def lock(self):
		self.lock_ = True

	def unlock(self):
		self.lock_ = False

	def to_str(self):
		return UNITS[self.type_]['desc']
	
	def to_dict(self):
		d = {}
		d['camp_'] = self.camp_
		d['res_'] = self.res_
		d['hp_'] = self.hp_
		d['dying_'] = self.dying_
		d['id'] = self.id
		d['type_'] = self.type_
		#d.update(self.__dict__)
		#d.pop('lock_')
		#d.pop('res_')
		return d

	def from_dict(self, d):
		if 'camp_' in d:
			self.camp_ = d['camp_']
		if 'res_' in d:
			self.res_ = d['res_']
		if 'hp_' in d:
			self.hp_ = d['hp_']
		if 'id' in d:
			self.id = d['id']
		if 'type' in d:
			self.type_ = d['type']
		if 'type_' in d:
			self.type_ = d['type_']
		#self.__dict__.update(d)

	def set_map(self, _map):
		self.map_ = _map

	def random_action(self):
		if not self.type:
			return 1
		actions = self.available_actions()
		if actions:
			action = random.choice(actions)
			action[0](self, random.choice(action[1]))
		log.debug(repr(map(lambda x: len(x[1]), actions)))
		num = reduce(operator.mul, map(lambda x: len(x[1]), actions), 1)
		return num

	def available_actions(self):
		actions = []
		if self.lock_:
			return actions
		if not self.type:
			return actions
		pos_list = self.calc_moveable_pos()
		if pos_list:
			#actions.append((Unit.move, copy.deepcopy(pos_list)))
			actions.append((Unit.move, pos_list))
		pos_list = self.calc_attackable_pos()
		if pos_list:
			#actions.append((Unit.attack, copy.deepcopy(pos_list)))
			actions.append((Unit.attack, pos_list))
		unit_list = self.calc_produceable_unit()
		if unit_list:
			#actions.append((Unit.produce, copy.deepcopy(unit_list)))
			actions.append((Unit.produce, unit_list))
		pos_list = self.calc_harvestable_pos()
		if pos_list:
			#actions.append((Unit.harvest, copy.deepcopy(pos_list)))
			actions.append((Unit.harvest, pos_list))
		pos_list = self.calc_returnbackable_pos()
		if pos_list:
			#actions.append((Unit.returnback, copy.deepcopy(pos_list)))
			actions.append((Unit.returnback, pos_list))
		return actions

	def availables(self):
		actions = []
		for act, arg in self.available_actions():
			for i in arg:
				actions.append((act, i))
		return actions

	def size(self):
		num = 1
		for act, arg in self.available_actions():
			num *= len(arg)
		return num
	#important
	#the second one import bias
#	def random(self):
#		actions = self.availables()
#		if not actions:
#			return
#		act, arg = random.choice(self.availables())
#		return (act, arg)

	def random(self):
		actions = self.available_actions()
		if not actions:
			return
		action = random.choice(actions)
		act = action[0]
		arg = random.choice(action[1])
		return (act, arg)

	def vibrate(self, action, dist, p):
		if random.random() > p:
			return action
		actions = self.availables()
		if not actions:
			return
	#	for pos, i in enumerate(actions):
	#		if i[0] != Unit.produce:
	#			continue
	#		#actions[pos] = (i[0], filter(lambda x: x[0] != 'id', i[1]))
	#		actions[pos] = (i[0], i[1])
	#
	#	if action[0] == Unit.produce:
	#		#action = (action[0], filter(lambda x: x[0] != 'id', action[1]))
	#		action = (action[0], action[1])
	#	if action not in actions:
	#		log.error('vibrate. action not in availables.')
	#		return
		r = random.randint(-dist, dist)
		pos = actions.index(action)
		pos = (pos + r) % len(actions)
		return actions[pos]
	
	def can_move(self):
		if not hasattr(self, 'moveable') or not self.moveable:
			return False
		pos = self.map_.get_unit_pos(self)
		if not pos:
			return False
		_, _poses = self.map_.find_empty_pos(pos, self.speed)
		for p in _poses:
			if self.move_check(p):
				return True
		return False	

	def calc_moveable_pos(self):
		pos_list = []
		if not hasattr(self, 'moveable') or not self.moveable:
			return pos_list
		pos = self.map_.get_unit_pos(self)
		if not pos:
			return pos_list
		#for i in xrange(1, self.speed + 1):
		_, _poses = self.map_.find_empty_pos(pos, self.speed)
		#print pos, _poses
		for p in _poses:
			if self.move_check(p):
				pos_list.append(p)
		return list(set(pos_list))

	def can_produce(self):
		if not hasattr(self, 'produceable') or not self.produceable:
			return False
		for i in self.product:
			if self.produce_check(i):
				return True
		return False

	def calc_produceable_unit(self):
		unit_list = []
		if not hasattr(self, 'produceable') or not self.produceable:
			return unit_list
		for i in self.product:
			if self.produce_check(i):
				unit_list.append(i)
		unit_list = list(set(unit_list))
		return tuple([i for i in unit_list])
		# return tuple([tuple(UNITS[i].items()) for i in unit_list])
		# return tuple(unit_list)

	def can_attack(self):
		if not hasattr(self, 'attackable') or not self.attackable:
			return False
		pos = self.map_.get_unit_pos(self)
		if not pos:
			return False
		_, _poses = self.map_.find_nearby_enemy(pos, self.attack_range, self.camp_)
		for p in _poses:
			if self.attack_check(p):
				return True
		return False

	def calc_attackable_pos(self):
		pos_list = []
		if not hasattr(self, 'attackable') or not self.attackable:
			return pos_list
		pos = self.map_.get_unit_pos(self)
		if not pos:
			return pos_list
		_, _poses = self.map_.find_nearby_enemy(pos, self.attack_range, self.camp_)
		for p in _poses:
			if self.attack_check(p):
				pos_list.append(p)
		return list(set(pos_list))

	def can_harvest(self):
		if not hasattr(self, 'harvestable') or not self.harvestable:
			return False
		if self.res_:
			return False
		pos = self.map_.get_unit_pos(self)
		if not pos:
			return False
		_, _poses = self.map_.find_nearby_res(pos, self.harvest_range)
		for p in _poses:
			if self.harvest_check(p):
				return True
		return False

	def calc_harvestable_pos(self):
		pos_list = []
		if not hasattr(self, 'harvestable') or not self.harvestable:
			return pos_list
		if self.res_:
			return pos_list
		pos = self.map_.get_unit_pos(self)
		if not pos:
			return pos_list
		_, _poses = self.map_.find_nearby_res(pos, self.harvest_range)
		for p in _poses:
			if self.harvest_check(p):
				pos_list.append(p)
		return list(set(pos_list))

	def can_return(self):
		if not self.res_:
			return False
		pos = self.map_.get_unit_pos(self)
		if not pos:
			return False
		_, _poses = self.map_.find_nearby_base(pos, self.harvest_range)
		for p in _poses:
			if self.returnback_check(p):
				return True
		return False

	def calc_returnbackable_pos(self):
		pos_list = []
		if not self.res_:
			return pos_list
		pos = self.map_.get_unit_pos(self)
		if not pos:
			return pos_list
		_, _poses = self.map_.find_nearby_base(pos, self.harvest_range)
		for p in _poses:
			if self.returnback_check(p):
				pos_list.append(p)
		return list(set(pos_list))

	def move_check(self, (dst_x, dst_y)):
		if self.lock_:
			return False
		if not self.moveable:
			log.debug('unit must be moveable.')
			return False
		pos = self.map_.get_unit_pos(self)
		if not pos:
			log.debug('unit has no pos info.')
			return False
		if pos == (dst_x, dst_y):
			log.debug('cant move to same pos.')
			return False
		src_x, src_y = pos
		if self.map_.distance(pos, (dst_x, dst_y)) > self.speed:
			log.debug('too far to go.')
			return False
		# find the way
		# now can jump over others :(
		if self.map_[dst_x][dst_y] != NoneUnit:
			log.debug('dst pos is not empty')
			return False
		return True

	def move(self, (dst_x, dst_y)):
		if not self.move_check((dst_x, dst_y)):
			return False
		pos = self.map_.get_unit_pos(self)
		src_x, src_y = pos
		self.map_.swap((src_x, src_y), (dst_x, dst_y))
		log.debug('unit %s (%d, %d) move to (%d, %d).' % (self.id, src_x, src_y, dst_x, dst_y))
		self.lock()
		mTimer.create(0.1, self.unlock, None)
		return True
	
	def produce_check(self, _unit):
		if self.lock_:
			return False
		if not self.produceable:
			log.debug('unit must be produceable.')
			return False
		pos = self.map_.get_unit_pos(self)
		if not pos:
			log.debug('unit has no pos info.')
			return False
		_unit = Unit(_unit)
		price = float('INF')
		if hasattr(_unit, 'price'):
			_price = _unit.price
		if self.map_.camps_[self.camp_].res_ < _price:
			log.debug('there is no enough res to produce this unit.')
			return
		empty_pos, _ = self.map_.find_empty_pos(pos, 1)
		if not empty_pos:
			log.debug('there is no pos to place the new unit.')
			return False
		if not self.map_.population_check(_unit.type, self.camp_):
		   return False
		return True

	def produce(self, _unit):
		if not self.produce_check(_unit):
			return False
		_unit = Unit(_unit)
		_price = float('INF')
		if hasattr(_unit, 'price'):
			_price = _unit.price
		self.map_.camps_[self.camp_].sub_res(_price)
		_unit.set_map(self.map_)
		_unit.camp_ = self.camp_
		pos = self.map_.get_unit_pos(self)
		empty_pos, _ = self.map_.find_empty_pos(pos, 1)
		self.map_.add(empty_pos, _unit)
		log.debug('unit %s (%d, %d) produce unit %s (%d, %d).' % (self.id, pos[0], pos[1], _unit.id, empty_pos[0], empty_pos[1]))
		self.lock()
		mTimer.create(0.1, self.unlock, None)
		return True

	def attack_check(self, (dst_x, dst_y)):
		if self.lock_:
			return False
		if not self.attackable:
			log.debug('unit must be attackable.')
			return False
		pos = self.map_.get_unit_pos(self)
		if not pos:
			log.debug('unit has no pos info.')
			return False
		if self.map_.distance(pos, (dst_x, dst_y)) > self.attack_range:
			log.debug('out of attack range.')
			return False
		if self.map_[dst_x][dst_y] == NoneUnit:
			log.debug('target must not be a none unit.')
			return False
		if self.camp_ == self.map_[dst_x][dst_y].camp_:
			log.debug('target must belong to another camp.')
			return False
		return True

	def attack(self, (dst_x, dst_y)):
		if not self.attack_check((dst_x, dst_y)):
			return False
		self.map_[dst_x][dst_y].hp_ -= self.attack_power
		if self.map_[dst_x][dst_y].hp_ <= 0:
			self.map_[dst_x][dst_y].dying_ = True
			#self.map_.delete((dst_x, dst_y))
		pos = self.map_.get_unit_pos(self)
		log.debug('unit %s (%d, %d) attack (%d, %d).' % (self.id, pos[0], pos[1], dst_x, dst_y))
		self.lock()
		mTimer.create(0.1, self.unlock, None)
		return True

	def harvest_check(self, (dst_x, dst_y)):
		if self.lock_:
			return False
		if not self.harvestable:
			log.debug('unit must be harvestable.')
			return False
		if self.res_:
			log.debug('unit with res must returnback firstly.')
			return False
		pos = self.map_.get_unit_pos(self)
		if not pos:
			log.debug('unit has no pos info.')
			return False
		if self.map_.distance(pos, (dst_x, dst_y)) > self.harvest_range:
			log.debug('out of harvest range.')
			return False
		if self.map_[dst_x][dst_y].name != 'UNIT_RES':
			log.debug('only UNIT_RES can be harvested.')
			return False
		return True

	def harvest(self, (dst_x, dst_y)):
		if not self.harvest_check((dst_x, dst_y)):
			return False
		#UNITS have been modified. .....
		self.map_[dst_x][dst_y].res_count -= self.harvest_count
		if self.map_[dst_x][dst_y].res_count <= 0:
			#self.map_.delete((dst_x, dst_y))
			self.map_[dst_x][dst_y].dying_ = True
		pos = self.map_.get_unit_pos(self)
		self.res_ = self.harvest_count
		log.debug('unit %s (%d, %d) harvest (%d, %d), res %d.' % (self.id, pos[0], pos[1], dst_x, dst_y, self.res_))
		self.lock()
		mTimer.create(0.1, self.unlock, None)
		return True

	def returnback_check(self, (dst_x, dst_y)):
		if self.lock_:
			return False
		if not self.res_:
			log.debug('unit must have res.')
			return False
		pos = self.map_.get_unit_pos(self)
		if not pos:
			log.debug('unit has no pos info.')
			return False
		if self.map_.distance(pos, (dst_x, dst_y)) > self.harvest_range:
			log.debug('out of return range.')
			return False
		if self.map_[dst_x][dst_y].name != 'UNIT_BASE':
			log.debug('only UNIT_BASE can be returned.')
			return False
		if self.map_[dst_x][dst_y].camp_ != self.camp_:
			log.debug('only UNIT_BASE of same camp can be returned.')
			return False
		return True

	def returnback(self, (dst_x, dst_y)):
		if not self.returnback_check((dst_x, dst_y)):
			return False
		self.map_.camps_[self.camp_].add_res(self.res_)
		self.res_ = 0
		pos = self.map_.get_unit_pos(self)
		log.debug('unit %s (%d, %d) return (%d, %d).' % (self.id, pos[0], pos[1], dst_x, dst_y))
		self.lock()
		mTimer.create(0.1, self.unlock, None)
		return True

	def get_max_hp(self):
		return UNITS[self.type_].get('maxhp', 0)

NoneUnit = Unit(0)
