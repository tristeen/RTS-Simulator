import math
import random
from rts import mMap
from misc.mLogger import log
from misc import utils
#import uuid
from graphviz import Digraph
import random
import subprocess
import platform
import os
import shutil
from ps import PoolSearch
from rts import mState
import hashlib
from rts import mUnit
import mThinker
import config
import copy

filenum = 0
dirnum = 0

#p0 = 0.6
p0 = 0.6
pg = 1
pl = 0.8

class Node(object):

	def __init__(self, move=None, parent=None, state=None):
		self.id = utils.gen_id()
		self.move = move
		self.parentNode = parent
		self.childNodes = []
		self.state = state.Clone()
		self.camp = state.camp
		self.wins = 0
		self.visits = 0
		self.result = []
	
		self.move_reward = {}

	def add_child(self, m, s):
		for i in self.childNodes:
			if self.move_eq(i.move, m):
				return i, True
		state = self.state.Clone()
		state.camp = int(not self.state.camp)
		n = Node(move=m, parent=self, state=state.Clone())
		self.childNodes.append(n)
		return n, False
	
	def move_eq(self, move1, move2):
		move1_list = sorted(move1.items())
		move2_list = sorted(move2.items())
		return filter(lambda x: x[1], move1_list) == filter(lambda x: x[1], move2_list)

	def select_child(self):
		if not len(self.childNodes): 
			move = self.state.GetRandomMove()
			s, old = self.add_child(move, self.state)
			return s, old
		if random.random() < p0:
			if random.random() < pg:
				s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))[-1]
			else:
				s = random.choice(self.childNodes)
			return s, True
		else:
			move = {}
			for unit_id, v in self.move_reward.iteritems():
				mr = sorted(v.items(), key=lambda x: 1.0 * sum(x[1]) / len(x[1]))		
				if random.random() < pl:
					move[unit_id] = mr[0][0]
				else:
					move[unit_id] = random.choice(map(lambda x: x[0], mr))	
			s, old = self.add_child(move, self.state)
			return s, old

	def update(self, move, result):
		self.visits += 1
		self.wins += result
		self.result.append(result)
		if move:
			for k, v in move.iteritems():
				self.move_reward.setdefault(k, {})
				if v in self.move_reward[k]:
					self.move_reward[k][v].append(result)
				else:
					self.move_reward[k][v] = []
					self.move_reward[k][v].append(result)

	def desc(self):
		return str(self.camp) + ': ' + str(self.state.GetMovesNum()) + '|' + str(self.state.get_unit_num()[self.camp]) + ' ' + str(round(self.wins/(self.visits + 0.0001), 2)) + '/' + str(self.visits)
		
	def move_desc(self):
		desc = ''
		if not self.move:
			return desc
		for k, v in self.move.iteritems():
			if v:
				desc += '' + v[0].__name__[0] + ''
			elif self.state.get_unit(k).type not in [0, 4]:
				desc += '_'
		_sum = 0
		for i in hashlib.md5(repr(self.move)).hexdigest():
			_sum += eval('0x%s' % i)
		desc += str(_sum)
		return desc
		
	def draw(self, dot):
		if self.camp:
			dot.node(str(self.id), self.desc(), fontsize='12', color='tomato', peripheries='2', penwidth='2', style='filled')
		else:
			dot.node(str(self.id), self.desc(), fontsize='12', color='skyblue', peripheries='2', style='filled', penwidth='2')
		if self.parentNode:
			dot.edge(str(self.parentNode.id), str(self.id), self.move_desc(), penwidth=str(self.get_edge_width()))
		for i in self.childNodes:
			i.draw(dot)

	def get_edge_width(self):
		if not self.parentNode:
			return 2
		p_visit = self.parentNode.visits
		if (1.0 * self.visits) / (p_visit + 0.0001) > 0.33:
			return 3
		else:
			return 1


def MCTS(rootstate, itermax):
	global filenum
	filenum = 0
	global dirnum
	dirnum += 1
	dirname = 'dir%d' % dirnum
	try:
		shutil.rmtree('./result/' + dirname)
	except OSError:
		pass
	os.mkdir('./result/' + dirname)
	rootnode = Node(state=rootstate)

	thinker = mThinker.ThinkerWeightedChoice()

	for i in range(itermax):
		state = rootstate.Clone()

		#log.info('Select')
		node, old = rootnode, True
		while old:
			node, old = node.select_child()
		
		#log.info('Rollout')
		state = node.state.Clone()
		#for j in xrange(32):
		for j in xrange(8):
			thinker.set_map(state.to_dict())
			action = thinker.get_action(state.camp)
			#state.DoMove(state.GetRandomMove())
			state.DoMove(action)

		#log.info('Backpropagate')
		result = state.GetResult(not node.camp)
		node.update(None, result)
		while node != None:
			#result = state.GetResult(node.camp)
			if node.parentNode:
				result = state.GetResult(not node.parentNode.camp)
				node.parentNode.update(node.move, result)
				node = node.parentNode
			else:
				break

		#raw_input('press any key to continue')
		if config.draw_dot_every_iter or config.show_dot_every_iter:
			draw_dot(rootnode, dirname, config.show_dot_every_iter)

	if config.draw_dot_every_mcts or config.show_dot_every_mcts:
		draw_dot(rootnode, dirname, config.show_dot_every_mcts)
	#print sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move
	#return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move
	#print 'rootnode.childNodes', rootnode.childNodes
	return sorted(rootnode.childNodes, key=lambda c: sum(c.result) / len(c.result))[-1].move


def draw_dot(rootnode, dirname, show=True):
	global filenum

	from PIL import Image
	dot = Digraph(format='png')
	rootnode.draw(dot)

	filenum += 1
	dot.render('result/%s/%d' % (dirname, filenum), view=False)
	if show:
		filename = './result/%s/%d.png' % (dirname, filenum)
		im = Image.open(filename, 'r')
		im.show()
