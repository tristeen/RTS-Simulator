import random
import copy
import operator
import heapq
import math
import utils
import itertools
from rts import mMap

heapq.cmp_lt = lambda x, y: x[1] > y[1]

class ObjectFunc(object):

	dist = 3

	def __init__(self, map_data, camp):
		self.map_ = mMap.mMap(map_data)
		self.camp_ = camp
		self.args_ = []
		self.init_args()

	def init_args(self):
		for u, i, j in self.map_:
			if u.camp_ == self.camp_ and u.type:
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

class Pool(object):

	max_size = 7
	alpha = 0.1

	def __init__(self, objfunc_, choice):
		self.objfunc_ = objfunc_
		self.pool_ = [{} for i in xrange(self.objfunc_.args_num())]
		self.evaluate_list = []
		#self.target_size = min(int(Pool.alpha * self.objfunc_.arg_size(i)), Pool.max_size)
		if choice == 'randomchoice':
			self.choice_ = random.choice
		elif choice == 'orderchoice':
			self.choice_ = order_weight_choose

	def add(self, values, objvalue):
		self.evaluate_list.append((values[:], objvalue))
		for i, v in enumerate(values):
			v = v or ()
			assert type(v) == tuple

			#print self.pool_[i].keys()	
			self.pool_[i].setdefault(v, [])
			self.pool_[i][v].append(objvalue)
			#print self.pool_[i].keys()	
		#p2 = map(lambda x: x.keys(), self.pool_)
		#if p1 != p2 and p1[0]:
		#	print '*' * 100
		#	print values
		#	print p1
		#	print p2

	def slim(self):
		for i, p in enumerate(self.pool_):
			target_size = max(min(int(Pool.alpha * self.objfunc_.arg_size(i)), Pool.max_size), 2)
			if len(p) <= target_size:
				continue
			#p = copy.deepcopy(p)
			#pp = copy.deepcopy(p)
			#for k, v in p.iteritems():
			#	p[k] = self._filter(v)
			#p = p.items()
			#p.sort(key=operator.itemgetter(1), reverse=True)
			#p = dict(p[:target_size])

			r = [(k, self._filter(v)) for k, v in p.iteritems()]
			r.sort(key=operator.itemgetter(1), reverse=True)
			r = dict(r[:target_size])
			#r = map(operator.itemgetter(1), r[:target_size])
			self.pool_[i] = dict(filter(lambda x: x[0] in p, self.pool_[i].iteritems()))

	def _filter(self, obj_values):
		return float(sum(obj_values)) / len(obj_values)
		#return max(obj_values)

	def t_race(self):
		for i, p in enumerate(self.pool_):
			candidate = p.keys()
			#print 'src candidate size %d'%len(candidate)
			for (k1, v1), (k2, v2) in itertools.combinations(p.items(), 2):
				if k1 == k2:
					continue
				if not (utils.df(v1, v2) or utils.similar(k1, v1, k2, v2)):
					continue
				k = k1
				if sum(v1) / len(v1) > sum(v2) / len(v2):
					k = k2
				if k in candidate:
					candidate.remove(k)
			#print 'dst candidate size %d'%len(candidate)
			self.pool_[i] = dict(
				filter(lambda x: x[0] in candidate, self.pool_[i].iteritems()))

	def gen(self):
		sol = []
		for i, p in enumerate(self.pool_):
			if p:
				sol.append(self.choice_(p.keys()))
			else:
				sol.append(self.random()[i])
			#print p.keys()
		#print self.pool_
		#print sol
		return sol

	def random(self):
		return self.objfunc_.random()

	def vibrate(self, values, p2):
		return self.objfunc_.vibrate(values, p2)

	def to_str(self):
		return 'Pool:\n' + '\n'.join(map(lambda x: repr(x.keys()), self.pool_))


weights = {
	1: {0: 1},
	2: {0: 0.8, 1: 0.2},
	3: {0: 0.8, 1: 0.15, 2: 0.05},
	4: {0: 0.8, 1: 0.12, 2: 0.05, 3: 0.03},
	5: {0: 0.8, 1: 0.11, 2: 0.04, 3: 0.03, 4: 0.02},
	6: {0: 0.8, 1: 0.11, 2: 0.04, 3: 0.03, 4: 0.01, 5: 0.01},
	7: {0: 0.8, 1: 0.11, 2: 0.04, 3: 0.02, 4: 0.01, 5: 0.01, 6: 0.01},
}
max_size = max(weights.keys())

def order_weight_choose(items):
	if len(items) > max_size:
		items = items[:max_size]
	index = utils.weighted_choice(weights[len(items)].items())		
	return items[index]


def calc(objfunc, times=1000):
	p1, p2 = 0.7, 0.3
	pool = Pool(objfunc)
	for i in xrange(times):
		if random.random() < p1:
			p = pool.gen()
			p = pool.vibrate(p, p2)
			objvalue = pool.objfunc_.evaluate(p)
			pool.add(p, objvalue)
		else:
			p = pool.random()
			objvalue = pool.objfunc_.evaluate(p)
			pool.add(p, objvalue)
		pool.t_race()
		pool.slim()
	x, y = heapq.nlargest(1, pool.evaluate_list, key=operator.itemgetter(1))[0]
	return y, x

def calc_rts(map_data, camp, times=1000):
	objfunc = ObjectFunc(map_data, camp)		
	return calc(objfunc, times)

if __name__ == '__main__':
	#global p1, p2
	#p1, p2 = 0.7, 0.3
	import ObjectFunction
	for k, v in ObjectFunction.TestFunctions.iteritems():
		sol = calc(v)
		print 'function name: %40s,\tobject value: %.2f,\tsolution is: %s' % (k, sol[0], sol[1])
