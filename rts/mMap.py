import mUnit
from mUnit import UNIT_NONE, UNIT_SOLDIER, UNIT_BASE, UNIT_WORKER, UNITS, UNIT_RES
from mUnit import NoneUnit
from misc import mTimer
from misc.mLogger import log
from mCamp import Camp

LENGTH, HEIGTH = 20, 20
POPULATION_LIMIT = 20


class mArray(object):

	def __init__(self, length, heigth):
		self.length_ = length
		self.heigth_ = heigth
		self.data_ = [[NoneUnit for i in xrange(length)] for j in xrange(heigth)]

	def __getitem__(self, pos):
		return self.data_[pos]

	def to_dict(self):
		_data = {}
		for i in xrange(self.heigth_):
			for j in xrange(self.length_):
				if self.data_[i][j] != NoneUnit:
					_data[(i, j)] = self.data_[i][j].to_dict()
		return dict(length=self.length_, heigth=self.heigth_, data=_data)

	def __len__(self):
		return self.length_ * self.heigth_

class mMap(object):

	def __init__(self, d):
		self.camps_ = {0: Camp(0, (255, 0, 0)), 1: Camp(1, (0, 0, 255))}
		self.index_ = {}
		self.from_dict(d)

	def from_dict(self, d):
		for k, v in d.get('camps', {}).iteritems():
			self.camps_[k].from_dict(v)
		self.data_ = mArray(d.get('length', LENGTH), d.get('heigth', HEIGTH))
		for (x, y), u in d.get('data', {}).iteritems():
			_unit = mUnit.Unit(u)
			self.data_[x][y] = _unit
			self.index_[_unit.id] = (_unit, (x, y))
			_unit.set_map(self)	

	def to_dict(self):
		d = self.data_.to_dict()
		d.update({'camps': dict((k, v.to_dict()) for k, v in self.camps_.iteritems())})
		return d

	def add(self, (x, y), u):
		self.data_[x][y] = u
		#if hasattr(u, 'camp_') and u.type not in (0, 4):
		#	self.camps_[u.camp_].add_unit(u)
		self.index_[u.id] = (u, (x, y))

	def swap(self, (src_x, src_y), (dst_x, dst_y)): 
		self.data_[src_x][src_y], self.data_[dst_x][dst_y] = self.data_[dst_x][dst_y], self.data_[src_x][src_y]
		self.index_[self.data_[src_x][src_y].id] = (self.data_[src_x][src_y], (src_x, src_y))
		self.index_[self.data_[dst_x][dst_y].id] = (self.data_[dst_x][dst_y], (dst_x, dst_y))

	def delete(self, (x, y)):
		u = self.data_[x][y]
		#if hasattr(u, 'camp_') and u.type not in (0, 4):
		#	self.camps_[u.camp_].del_unit(u)
		self.index_.pop(u.id)
		self.data_[x][y] = NoneUnit
		#self.data_[x][y].map_ = u.map_

	def get_unit_pos(self, _unit):
		if _unit.id in self.index_:
			return self.index_[_unit.id][1]
		log.warning('get_unit_pos out of index_')
		for u, i, j in self:
			if u.id == _unit.id:
				return i, j
		log.warning('get_unit_pos return None')

	def find_empty_pos(self, (x, y), r):
		empty_pos = []
		for i in xrange(max(0, x - r), min(self.data_.heigth_, x + r + 1)):
			for j in xrange(max(0, y - r), min(self.data_.length_, y + r + 1)):
				if self.data_[i][j] == NoneUnit and (x, y) != (i, j) and self.distance((x, y), (i, j)) <= r:
					empty_pos.append((i, j))
		return empty_pos and empty_pos[0] or None, empty_pos

	def find_nearby_enemy(self, (x, y), r, _camp):
		unit_pos_ = []
		for i in xrange(max(0, x - r), min(self.data_.heigth_, x + r + 1)):
			for j in xrange(max(0, y - r), min(self.data_.length_, y + r + 1)):
				if self.data_[i][j] != NoneUnit and (i, j) != (x, y) and self.data_[i][j].camp_ != _camp and self.distance((x, y), (i, j)) <= r:
					unit_pos_.append((i, j))
		return unit_pos_ and unit_pos_[0] or None, unit_pos_

	def find_nearby_res(self, (x, y), r):
		unit_pos_ = []
		for i in xrange(max(0, x - r), min(self.data_.heigth_, x + r + 1)):
			for j in xrange(max(0, y - r), min(self.data_.length_, y + r + 1)):
				if self.data_[i][j].name == 'UNIT_RES' and self.data_[i][j] != NoneUnit and (i, j) != (x, y) and self.distance((x, y), (i, j)) <= r:
					unit_pos_.append((i, j))
		return unit_pos_ and unit_pos_[0] or None, unit_pos_

	def find_nearby_base(self, (x, y), r):
		unit_pos_ = []
		for i in xrange(max(0, x - r), min(self.data_.heigth_, x + r + 1)):
			for j in xrange(max(0, y - r), min(self.data_.length_, y + r + 1)):
				if self.data_[i][j].name == 'UNIT_BASE' and self.data_[i][j] != None and (i, j) != (x, y) and self.distance((x, y), (i, j)) <= r:
					unit_pos_.append((i, j))
		return unit_pos_ and unit_pos_[0] or None, unit_pos_

	def distance(self, src_pos, dst_pos):
		return abs(src_pos[0] - dst_pos[0]) + abs(src_pos[1] - dst_pos[1])

	def get_unit(self, _id):
		if _id in self.index_:
			return self.index_[_id][0]
		log.warning('get_unit out of index_')
		for u, x, y in self:
			if u.id == _id:
				return u
		log.warning('get_unit return None')

	def get_unit_num(self):
		num = [0, 0]
		for u, _, _ in self:
			if u.type in (0, 4):
				continue
			num[u.camp_] += 1
		return num
	
	def get_population_num(self):
		num = [0, 0]
		for u, _, _ in self:
			if u.type in (0, 4):
				continue
			num[u.camp_] += u.__dict__.get('population', 0)
		return num

	def population_check(self, unit_type, camp):
		unit = mUnit.Unit(unit_type)
		population_num = self.get_population_num()[camp]
		if population_num + unit.__dict__.get('population', 0) >= POPULATION_LIMIT:
			return False
		return True

	def desc(self):
		desc = []
		scores = {}
		for camp_id, camp in self.camps_.iteritems():
			desc.append('CAMP ID: %d' % camp_id)
			score, (res_score, hp_score, attacker_score) = self.calc_score(camp_id)
			scores[camp_id] = score
			desc.append('SCORE: %.1f, (%.2f, %.0f, %.0f)' % (score, res_score, hp_score, attacker_score))
			desc.append('RES NUM: %d' % camp.res_)
			stat = dict((i['name'], 0) for _, i in mUnit.UNITS.iteritems() if i['type'])
			for u, _, _ in self:
				if u.camp_ != camp_id:
					continue
				if u.name not in stat:
					continue
				stat[u.name] += 1
			for name, num in stat.iteritems():
				desc.append('%s: %d' % (name, num))
			desc.append('')

		desc.append('SCORE DIFF: %.1f' % (scores[0] - 1.5 * scores[1]))
		return desc

	def score(self):
		scores = [0.0, 0.0]
		#cfg = {1: 2, 2: 10, 3: 1}
		for u, _, _ in self:
			if u.type in (0, 4):
				continue
			#scores[u.camp_] += cfg[u.type]
			scores[u.camp_] += u.price
		for camp_id, camp in self.camps_.iteritems():
			scores[camp_id] += camp.res_
		return scores

	def calc_score(self, camp):
		#res
		res = self.camps_[camp].res_
		unit_res, unit_price = 0, 0
		#res inc	
		#1. harvestable unit num
		#2. returnbackable unit num
		harvestable_num = 0
		returnbackable_num = 0
		#attack
		attacker_score = 0
		attack_power_sum = 0
		#hp
		hp_score = 0
		#unit score
		unit_score = 0
		for u, _, _ in self:
			if u.camp_ != camp:
				continue
			if u.can_harvest():
				harvestable_num += u.harvest_count
			if u.can_return():
				returnbackable_num += u.harvest_count
			if u.can_attack():
				attacker_score += u.attack_power
				attack_power_sum += u.attack_power
			elif hasattr(u, 'attack_power'):
				attack_power_sum += 0.5 * u.attack_power
			#if u.type not in (0, 4):
			if u.type not in (0, 2, 4):
				hp_score += u.hp_
				unit_price += u.price
			if u.res_:
				unit_res += u.res_
		res_score = 1.2 * res + 0.8 * unit_res + 0.05 * (harvestable_num + returnbackable_num)
		hp_score = 1.5 * hp_score + 1.2 * unit_price
		attacker_score = 0.4 * attacker_score + attack_power_sum
		return res_score + hp_score + attacker_score, (res_score, hp_score, attacker_score)	

	def __iter__(self):
		for i in xrange(self.data_.heigth_):
			for j in xrange(self.data_.length_):
				yield self.data_[i][j], i, j

	def __getitem__(self, pos):
		return self.data_[pos]

	def __repr__(self):
		rows = []
		for i in xrange(self.data_.heigth_):
			rows.append(''.join(map(lambda x: x.to_str(), self.data_[i])))
		return '\n'.join(rows)

	def cleanup(self):
		for u, i, j in self:
			if u.dying_:
				self.delete((i, j))
