import math
from scipy import stats
import numpy as np
import bisect
import random

def df(lst1, lst2, p=0.05):
	#if not lst1 or not lst2:
	#	return True
	#print len(lst1), len(lst2)
	lst1, lst2 = np.array(lst1), np.array(lst2)
	return stats.ttest_ind(lst1, lst2, equal_var=False)[1] < p

def similar(k1, v1, k2, v2):
	return False
	if abs(k1 - k2) < 10 and float(abs(mean(v1) - mean(v2))) / (max(mean(v1), mean(v2)) + 0.000001) < 0.1:
		#print 'similar'	
		return True
	return False	

class LinearTrans(object):

	def __init__(self, a, n):
		self.a = a
		self.n = n
		self.b = self.calc_b()
		self.s = 0.0
		for i in xrange(n):
			f = self.f(i)
			self.s += f > 0 and f or 0

	#y = a * x + b
	def calc_b(self):
		return 1.0 / self.n - (self.n + 1.0) * self.a / 2

	def f(self, i):
		return (i + 1) * self.a + self.b

	def w(self, i):
		#w = self.f(i) / self.s
		w = self.f(i)
		return w > 0 and w or 0


def order_choice(lst):
	dct = {}
	n = len(lst)
	a = -0.02
	lt = LinearTrans(a, n)
	for i, j in enumerate(lst):
		dct[j] = lt.w(i)
	return weighted_choice(dct.items())


def weighted_choice(choices):
	values, weights = zip(*choices)
	total = 0
	cum_weights = []
	for w in weights:
		total += w
		cum_weights.append(total)
	x = random.random() * total
	i = bisect.bisect(cum_weights, x)
	return values[i]

def test():
	from scipy import stats
	import numpy as np
	np.random.seed(12345678)
	rvs1 = stats.norm.rvs(loc=5, scale=10, size=500)	
	rvs2 = stats.norm.rvs(loc=5, scale=10, size=100)
	print stats.ttest_ind(rvs1, rvs2)
	print stats.ttest_ind(rvs1, rvs2, equal_var=False)

if __name__ == '__main__':
	import random
	n = 100
	lst1 = [random.gauss(13, 4) for i in xrange(n)]
	lst2 = [random.gauss(17, 2) for i in xrange(n)]
	from numpy import array
	from scipy import stats

	print df([1], [2])
	#print df([51.5, 51.5, 50.0, 51.5, 50.0, 51.5, 50.0, 52.3, 52.3, 50.0, 50.0, 50.0], [51.5, 51.5, 52.3, 51.5, 52.3, 51.5])
	rvs1, rvs2 = array([51.5, 51.5, 50.0, 51.5, 50.0, 51.5, 50.0, 52.3, 52.3, 50.0, 50.0, 50.0]), array([51.5, 51.5, 52.3, 51.5, 52.3, 51.5])
	#print stats.ttest_ind(rvs1, rvs2, equal_var=False)

