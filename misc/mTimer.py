import heapq
import time

class pq(object):

	def __init__(self, items=[]):
		self.set = dict((item, True) for item in items)
		self.heap = self.set.keys()
		heapq.heapify(self.heap)

	def has_item(self, item):
		return item in self.set

	def pop(self):
		if not self.heap:
			return None
		smallest = heapq.heappop(self.heap)
		del self.set[smallest]
		return smallest

	def push(self, item):
		if not (item in self.set):
			self.set[item] = True
			heapq.heappush(self.heap, item)


class timer(object):

	def __init__(self, _t, _cb, _ud, _loop=False):
		self.t_ = _t
		self.loop_ = _loop
		self.cb_ = _cb
		self.ud_ = _ud

	def __call__(self):
		if self.ud_:
			return self.cb_(self.ud_)
		else:
			return self.cb_()

	def __cmp__(self, other):
		return cmp(self.t_, other.t_)

t = 0
#def time():
#	return t

def tick():
	global t
	t += 1

def create(delay, cb, ud):
	global timers
	_t = time.time() + delay
	#_t = time() + delay
	timers.push(timer(_t, cb, ud))


def loop():
	global timers, cur_timer
	tick()
	while True:
		if not cur_timer:
			cur_timer = timers.pop()
		if not cur_timer:
			break
		if time.time() > cur_timer.t_:
			cur_timer()
			cur_timer = None

timers = pq()
cur_timer = None

if __name__ == '__main__':
	def test(a):
		print a

	import time
	create(1, test, 1)
	while True:
		time.sleep(0.5)
		loop()
