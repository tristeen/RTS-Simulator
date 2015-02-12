import bisect
import random
import collections
import itertools


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


def dict_add(dict1, dict2):
	d = dict(dict1, **dict2)
	for k, v in d.iteritems():
		if isinstance(v, collections.Mapping):
			d[k] = dict_add(dict1.get(k, {}), dict2.get(k, {}))
		else:
			d[k] = dict1.get(k, type(v)()) + dict2.get(k, type(v)())
	return d


def product(args):
	return eval('itertools.product(' + ','.join(map(lambda x: 'args[%d]' % x, range(len(args)))) + ')')

max_id = 0
def gen_id():
	global max_id
	max_id += 1
	return max_id
