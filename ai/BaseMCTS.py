import math
import random
from rts import mMap
from misc.mLogger import log
from misc import utils
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
		if random.random() < 0.9 and len(self.childNodes) > 10:
			s = sorted(self.childNodes, key=lambda c: c.wins / c.visits)[-1]
			return s, True
		else:
			move = self.state.GetRandomMove()
			s, old = self.add_child(move, self.state)
			return s, old

	def update(self, move, result):
		self.visits += 1
		self.wins += result
		self.result.append(result)

	def desc(self):
		return str(self.camp) + ': ' + str(self.state.GetMovesNum()) + '|' + str(self.state.get_unit_num()[self.camp]) + ' ' + str(round(self.wins / (self.visits + 0.0001), 2)) + '/' + str(self.visits)
		
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


def entropy(rootnode):
	p = map(lambda x: 1.0 * x.visits / rootnode.visits, rootnode.childNodes)
	et = 0
	for i in p:
		if abs(i) > 0.0001:
			et += -i * math.log(i) / math.log(2)
	return et


def draw_dot(rootnode, dirname, filenum, show=True):
	from PIL import Image
	dot = Digraph(format='png')
	rootnode.draw(dot)

	filenum += 1
	dot.render('result/%s/%d' % (dirname, filenum), view=False)
	if show:
		filename = './result/%s/%d.png' % (dirname, filenum)
		im = Image.open(filename, 'r')
		im.show()
	return filenum


def mkdir(dirnum, filenum):
	dirname = 'dir%d' % dirnum
	if config.draw_dot_every_iter or config.draw_dot_every_mcts or config.show_dot_every_iter or config.show_dot_every_mcts:
		filenum = 0
		dirnum += 1
		dirname = 'dir%d' % dirnum
		try:
			shutil.rmtree('./result/' + dirname)
		except OSError:
			pass
		os.mkdir('./result/' + dirname)
	return dirname, dirnum, filenum
