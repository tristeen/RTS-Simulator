import math
import random
import mMap
from misc.mLogger import log
from misc import utils
import random


class RTSState(mMap.mMap):

	def __init__(self, d, camp):
		super(RTSState, self).__init__(d)
		self.camp = camp

	def Clone(self):
		st = RTSState(self.to_dict(), self.camp)
		return st

	def equal(self, state):
		if cmp(self.to_dict(), state.to_dict()):
			return False
		print 'maps of state, k are the same'
		return self.camp == state.camp

	def DoMove(self, move):
		# print 'DoMove 1'
		# print move
		# for u, i, j in self:
		#	if u.type:
		#		print 'id %s, type %d, camp %d, pos (%d, %d)'%(u.id, u.type, u.camp_, i, j)
		# print 'DoMove 2'
		for _id, action in move.iteritems():
			if not action:
				continue
			try:
				action[0](self.get_unit(_id), action[1])
			except TypeError:
				log.info('UCT unit %s has been killed.' % _id)
		self.camp = int(not self.camp)

	def GetMoves(self):
		actions = []
		_ids = []
		_availables = []
		for u, i, j in self:
			if u.camp_ != self.camp:
				continue
			available = u.available_actions()
			if not available:
				continue
			_ids.append(u.id)
			_availables.append(available)
		for i in utils.product(_availables):
			acts = [j[0] for j in i]
			args = [j[1] for j in i]
			for j in utils.product(args):
				actions.append(dict(zip(_ids, zip(acts, j))))
		return actions

#	def GetRandomMove(self):
#		action = {}
#		for u, i, j in self:
#			if u.camp_ != self.camp_:
#				continue
#			available = u.available_actions()
#			if not available:
#				continue
# not uniform exactly
#			_act = random.choice(available)
#			action[u.id] = (_act[0], random.choice(_act[1]))
#		return action

	def GetRandomMove(self):
		state = self.Clone()
		action = {}
		# for u, i, j in self:
		for u, i, j in state:
			if u.camp_ != state.camp:
				continue
			if not self.get_unit(u.id):
				continue
			available = u.available_actions()
			if not available:
				continue
			# not uniform exactly
			_act = random.choice(available)
			_arg = random.choice(_act[1])
			action[u.id] = (_act[0], _arg)
			action[u.id][0](u, _arg)

		state = self.Clone()
		for _id, act in action.iteritems():
			# print act, _id
			# print self.get_unit(_id)
			# print act
			# print state.get_unit(_id)
			act[0](state.get_unit(_id), act[1])
		return action

	# confilicated states?
	def GetMovesNum(self):
		num = 1
		for u, i, j in self:
			if u.camp_ != self.camp:
				continue
			available = u.available_actions()
			if not available:
				continue
			n = 0
			for a in available:
				n += len(a[1])
			num *= n
		return num

	def GetResult(self, playerjm):
		scores = {playerjm: self.calc_score(playerjm)[0], (not playerjm): self.calc_score(not playerjm)[0]}
		#return max(0, round(1.0 * (scores[playerjm] - scores[not playerjm]) / scores[not playerjm], 2))
		return scores[playerjm] - 1.5 * scores[not playerjm]
		#return scores[playerjm]
	#	if scores[playerjm] > scores[not playerjm]:
	#		return 1
	#	elif scores[playerjm] == scores[not playerjm]:
	#		return 0.5
	#	else:
	#		return 0


class ObjectFunc(RTSState):
	dist = 3

	def __init__(self, d, camp):
		super(ObjectFunc, self).__init__(d, camp)
		self.args_ = []
		self.init_args()

	def init_args(self):
		for u, i, j in self:
			if u.camp_ == self.camp and u.type:
				self.args_.append(u)

	def evaluate(self, values):
		return 1

	def args_num(self):
		return len(self.args_)

	def space_size(self):
		return reduce(operator.mul, map(lambda x: x.size(), self.args_))

	def arg_size(self, i):
		return self.args_[i].size()

	def random(self):
		return [i.random() for i in self.args_]

	def vibrate(self, values, p2):
		return [self.args_[i].vibrate(v, ObjectFunc.dist, p2) for i, v in enumerate(values)]
