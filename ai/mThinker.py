from misc.mLogger import log
from rts import mMap
import random
from misc import utils
from rts import mState
#from ps import PoolSearch
import mMCTS
import mNewMCTS
import mEG
import mUCT
import mNaiveMCTS
import config

class Thinker(object):
	
	def __init__(self, _map, thinkers):
		self.map_ = _map
		self.thinkers_ = thinkers

	def execute(self):
	#   1
		camp, thinker = 0, self.thinkers_[0]
		thinker.set_map(self.map_.to_dict())
		actions = thinker.get_action(camp)
		for _id, action in actions.iteritems():
			try:
				if action:
					action[0](self.map_.get_unit(_id), action[1])
			except TypeError:
				log.info('unit %s has been killed.' % _id)
		self.map_.cleanup()

		camp, thinker = 1, self.thinkers_[1]
		thinker.set_map(self.map_.to_dict())
		actions = thinker.get_action(camp)
		for _id, action in actions.iteritems():
			try:
				if action:
					action[0](self.map_.get_unit(_id), action[1])
			except TypeError:
				log.info('unit %s has been killed.' % _id)
		self.map_.cleanup()

	#	2
	#	for camp, thinker in self.thinkers_.iteritems():
	#		# print PoolSearch.calc_rts(self.map_.to_dict(), camp, 10)
	#		thinker.set_map(self.map_.to_dict())
	#		actions = thinker.get_action(camp)
	#		for _id, action in actions.iteritems():
	#			try:
	#				if action:
	#					action[0](self.map_.get_unit(_id), action[1])
	#			except TypeError:
	#				log.info('unit %s has been killed.' % _id)
	#	self.map_.cleanup()

	#	actions = {}
	#	for camp, thinker in self.thinkers_.iteritems():
	#		thinker.set_map(self.map_.to_dict())
	#		actions.update(thinker.get_action(camp))
	#	actions = actions.items()
	#	random.shuffle(actions)
	#	for _id, action in actions:
	#		try:
	#			if action:
	#				action[0](self.map_.get_unit(_id), action[1])
	#		except TypeError:
	#			log.info('unit %s has been killed.' % _id)
	#	self.map_.cleanup()

class ThinkerRandom(object):
												
	def __init__(self):
		pass

	def set_map(self, map_data):
		self.map_ = mMap.mMap(map_data)
								
	def get_action(self, camp):
		actions = {}
		for u, i, j in self.map_:
			if u.camp_ != camp:
				continue
			available = u.available_actions()
			if not available:
				continue
			action = random.choice(available)
			actions[u.id] = (action[0], random.choice(action[1]))
			actions[u.id][0](u, actions[u.id][1])
		log.debug('ThinkerRandom %s' % repr(actions))
		return actions


class ThinkerUCT(ThinkerRandom):

	def __init__(self):
		super(ThinkerUCT, self).__init__()

	def set_map(self, map_data):
		self.map_ = mMap.mMap(map_data)

	def get_action(self, camp):
		state = mState.RTSState(self.map_.to_dict(), camp)
		#m = mMAB.MTS(rootstate=state, itermax=32, stragey='UCT')
		m = mUCT.MCTS(rootstate=state, itermax=config.iter_times)
		return m


class ThinkerEG(ThinkerRandom):

	def __init__(self):
		super(ThinkerEG, self).__init__()

	def set_map(self, map_data):
		self.map_ = mMap.mMap(map_data)

	def get_action(self, camp):
		state = mState.RTSState(self.map_.to_dict(), camp)
		m = mEG.MCTS(rootstate=state, itermax=config.iter_times)
		return m


class ThinkerNaiveMCTS(ThinkerRandom):

	def __init__(self):
		super(ThinkerNaiveMCTS, self).__init__()

	def set_map(self, map_data):
		self.map_ = mMap.mMap(map_data)

	def get_action(self, camp):
		state = mState.RTSState(self.map_.to_dict(), camp)
		m = mNaiveMCTS.MCTS(rootstate=state, itermax=config.iter_times)
		return m

#order_choice
class ThinkerMCTS(ThinkerRandom):

	def __init__(self):
		super(ThinkerMCTS, self).__init__()

	def set_map(self, map_data):
		self.map_ = mMap.mMap(map_data)

	def get_action(self, camp):
		state = mState.RTSState(self.map_.to_dict(), camp)
		m = mMCTS.MCTS(rootstate=state, itermax=config.iter_times, choice='orderchoice')
		return m

#order_choice
class ThinkerNewMCTS(ThinkerRandom):

	def __init__(self):
		super(ThinkerNewMCTS, self).__init__()

	def set_map(self, map_data):
		self.map_ = mMap.mMap(map_data)

	def get_action(self, camp):
		state = mState.RTSState(self.map_.to_dict(), camp)
		m = mNewMCTS.MCTS(rootstate=state, itermax=config.iter_times, choice='orderchoice')
		return m

class ThinkerMCTS_RC(ThinkerRandom):

	def __init__(self):
		super(ThinkerMCTS_RC, self).__init__()

	def set_map(self, map_data):
		self.map_ = mMap.mMap(map_data)

	def get_action(self, camp):
		state = mState.RTSState(self.map_.to_dict(), camp)
		m = mMCTS.MCTS(rootstate=state, itermax=config.iter_times, choice='randomchoice')
		return m

class ThinkerRandomBiased(ThinkerRandom):

	def __init__(self):
		super(ThinkerRandomBiased, self).__init__()
		self.biased_ = {'attack': 1, 'returnback': 2, 'harvest': 3, 'produce': 4, 'move': 5}

	def get_action(self, camp):
		actions = {}
		for u, i, j in self.map_:
			if u.camp_ != camp:
				continue
			available = u.available_actions()
			if not available:
				continue
			log.debug('available %d' % len(available))
			available.sort(key=lambda x: self.biased_.get(x[0].im_func.func_name, 0))
			log.debug(repr(available))
			action = available[0]
			actions[u.id] = (action[0], random.choice(action[1]))
			actions[u.id][0](u, actions[u.id][1])
		log.debug('ThinkerRandomBiased %s' % repr(actions))
		return actions


class ThinkerWeightedChoice(ThinkerRandom):

	def __init__(self):
		super(ThinkerWeightedChoice, self).__init__()
		self.weights_ = {'attack': 10, 'harvest': 8, 'returnback': 6, 'produce': 1, 'move': 1}

	def get_action(self, camp):
		actions = {}
		for u, i, j in self.map_:
			if u.camp_ != camp:
				continue
			available = u.available_actions()
			if not available:
				continue
			action_names = map(lambda x: x[0].im_func.func_name, available)
			weights = filter(lambda x: x[0] in action_names, self.weights_.items())
			name = utils.weighted_choice(weights)
			action = filter(lambda x: x[0].im_func.func_name == name, available)[0]
			actions[u.id] = (action[0], random.choice(action[1]))
			actions[u.id][0](u, actions[u.id][1])
		log.debug('ThinkerWeightedChoice %s' % repr(actions))
		return actions

import re
import sys
Pattern = re.compile('Thinker(\w+)$')

thinkers = {}
for k, v in globals().items():
	if Pattern.match(k):
		thinkers[k] = v
