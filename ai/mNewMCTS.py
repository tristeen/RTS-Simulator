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
import operator
import itertools
from ai import ps

filenum = 0
dirnum = 0
choice_method = 'orderchoice'


class NodeCache(object):

	def __init__(self):
		self.nodes = {}

	def add(self, node):
		self.nodes[node.state] = node  

	def update(self, state, result):
		#print len(self.nodes)
		for k, v in self.nodes.iteritems():	
			if state.equal(k):
				print len(self.nodes)
				print 'state and k is the same'
				v.update_up_to_root(result)

rave = False
node_cache = NodeCache()

class Node(object):

	def __init__(self, move=None, parent=None, state=None):
		self.id = utils.gen_id()
		self.move = move
		self.parentNode = parent
		self.childNodes = []
		self.state = state.Clone()
		self.camp = state.camp
		self.objfunc = mState.ObjectFunc(self.state.to_dict(), self.state.camp)
		self.pool = PoolSearch.Pool(mState.ObjectFunc(self.state.to_dict(), self.state.camp), choice=choice_method)
		self.wins = 0
		self.visits = 0
		self.result = []
		self.values = []
		self.evals = []
		if rave:
			global node_cache
			node_cache.add(self)

	def add_child(self, m, s):
		for i in self.childNodes:
			if self.move_eq(i.move, m):
				return i, True
		n = Node(move=m, parent=self, state=s)
		self.childNodes.append(n)
		return n, False
	
	def move_eq(self, move1, move2):
		move1_list = sorted(move1.items())
		move2_list = sorted(move2.items())
		return filter(lambda x: x[1], move1_list) == filter(lambda x: x[1], move2_list)

	def select_child(self):
		#if random.random() < 0.9:
		if random.random() < 0.9:
			move = self.pool.gen()
			move = self.pool.vibrate(move, 0.05)
		else:
			move = self.pool.random()
		move = dict(zip(map(lambda x: getattr(x, 'id'), self.objfunc.args_), move))
		return move

	def update(self, move, result):
		self.visits += 1
		self.wins += result
		self.result.append(result)

		if move:
			m = []
			for i in self.objfunc.args_:
				m.append(move[i.id])
			
			#print '1. pool', map(lambda x: x.keys(), self.pool.pool_)
			#print m
			self.pool.add(m, result)
			self.pool.t_race()
			self.pool.slim()
			#print '2. pool', map(lambda x: x.keys(), self.pool.pool_)
		else:
			self.values.append(round(result, 1))

	def update_up_to_root(self, result):
		node = self
		node.update(None, result[not node.camp])
		node.add_eval(result)
		while node != None:
			if node.parentNode:
				node.parentNode.update(node.move, result[not node.parentNode.camp])
				node = node.parentNode
			else:
				break

	#def desc(self):
	#	return str(self.camp) + ': ' + str(self.state.GetMovesNum()) + '|' + str(self.state.get_unit_num()[self.camp]) + ' ' + str(round(self.wins/self.visits, 2)) + '/' + str(self.visits)
		
	def desc(self):
		#return str(self.visits) + ': ' + str(self.values) + ': ' + str(map(lambda x: round(x, 1), self.result))
		#return str(self.visits) + ': ' + str(map(lambda x: map(lambda y: round(y, 1), x), self.evals))
		return str(self.visits) + ': ' + str(round(sum(self.result) / len(self.result), 1))

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
		if (1.0 * self.visits) / p_visit > 0.33:
			return 3
		else:
			return 1

	def add_eval(self, result):
		self.evals.append(result)

	def update_eval(self):
		if not self.childNodes: 
			return
		for i in self.childNodes:
			i.update_eval()
		del_nodes = []	
		for (i, j) in itertools.combinations(self.childNodes, 2):
			lsti = map(operator.itemgetter(not i.camp), i.evals)
			lstj = map(operator.itemgetter(not j.camp), j.evals)
			if ps.utils.df(lsti, lstj, 0.015):
				log.info('two different list %s %s' % (str(map(lambda x: round(x, 1), lsti)), str(map(lambda x: round(x, 1), lstj))))

				#if lsti is long, and lstj is short...
				#[-11.0, -5.4, -8.8, -10.0, -10.0, -10.4, -5.8, -12.8, -5.4, -10.4] [-4.8]
				if 1.0 * sum(lsti) / len(lsti) > 1.0 * sum(lstj) / len(lstj):
					del_nodes.append(j)
				else:
					del_nodes.append(i)
		for i in set(del_nodes):
			self.childNodes.remove(i)
		for i in self.childNodes:
			self.evals.extend(i.evals)

		self.result = []
		for i in self.evals:
			self.result.append(i[not self.camp])	
		return


def MCTS(rootstate, itermax, choice):
	global choice_method
	choice_method = choice
	dirname = mkdir()
	rootnode = Node(state=rootstate)
	thinker = mThinker.ThinkerWeightedChoice()
	if rave:
		global node_cache
		node_cache = NodeCache()

	for i in range(itermax):
		node = rootnode
		state = rootstate.Clone()

		#log.info('Select')
		old = True
		while old:
			move = node.select_child()
			# delete delete
			state = node.state.Clone()
			state.DoMove(move)
			node, old = node.add_child(move, state.Clone())
		#log.info('Rollout')
		#state = node.state.Clone()
		#for j in xrange(32):
		for j in xrange(8):
			thinker.set_map(state.to_dict())
			action = thinker.get_action(state.camp)
			#state.DoMove(state.GetRandomMove())
			state.DoMove(action)
			result = (state.GetResult(0), state.GetResult(1))
			if rave:
				node_cache.update(state, result)	

		#log.info('Backpropagate')
		#result = state.GetResult(not node.camp)
		result = (state.GetResult(0), state.GetResult(1))
		node.update_up_to_root(result)		
				
		#raw_input('press any key to continue')
		if config.draw_dot_every_iter or config.show_dot_every_iter:
			draw_dot(rootnode, dirname, config.show_dot_every_iter)

	if config.draw_dot_every_mcts or config.show_dot_every_mcts:
		draw_dot(rootnode, dirname, config.show_dot_every_mcts)
		print 'entropy(rootnode) %.2f'%entropy(rootnode)
	rootnode.update_eval()
	if config.draw_dot_every_mcts or config.show_dot_every_mcts:
		draw_dot(rootnode, dirname, config.show_dot_every_mcts)
		print 'entropy(rootnode) %.2f'%entropy(rootnode)

	#print sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move
	#return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move
	return sorted(rootnode.childNodes, key=lambda c: sum(c.result) / len(c.result))[-1].move

def entropy(rootnode):
	#print 'entropy num %s, sum %s'%(str(map(lambda x: x.visits)), rootnode.visits)
	p = map(lambda x: 1.0 * x.visits / rootnode.visits, rootnode.childNodes)
	et = 0
	for i in p:
		if abs(i) > 0.0001:
			et += -i * math.log(i) / math.log(2)
	return et


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

def mkdir():
	if config.draw_dot_every_iter or config.draw_dot_every_mcts or config.show_dot_every_iter or config.show_dot_every_mcts:
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
		return dirname
