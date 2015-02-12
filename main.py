from rts import mUnit
from rts import mMap
from rts import mData
from misc import mTimer
import time
from misc.mLogger import log
from ai import mThinker
import threading
import config
from rts import mMap
import pprint

maps = {}

def main(times, thinkers):
	_map = mMap.mMap(mData.maps[config.map_name].to_dict())
	global maps
	maps[times] = [] 

	if config.view:
		from rts import mView
		mv = mView.mView(_map)
		def f():
			while True:
				time.sleep(0.5)
				mv.loop()
		t = threading.Thread(target=f)
		t.start()
	
	#while True:
	for j in xrange(20):
		now = time.time()
		maps[times].append(_map.to_dict())
		thinker1, thinker2 = map(lambda x: getattr(mThinker, x)(), thinkers)  
		thinker = mThinker.Thinker(_map, {0: thinker1, 1: thinker2})
		thinker.execute()
		num = _map.get_unit_num()
		if num[0] in [0, 1] or num[1] in [0, 1]:
			break	
		if abs(num[0] - num[1]) / min(num[0], num[1]) >= 10:
			break
		log.info('num: %d, time: %d'%(j, int(time.time() - now)))
		mTimer.loop()
		if config.debug_pause:
			raw_input('Press any key to continue:')	
	num = _map.get_unit_num()
	if num[0] > num[1]:
		log.info('Win.')
		return 1
	elif num[0] < num[1]:
		log.info('Lose.')
		return -1
	else:
		log.info('Tie.')
		return 0

rst = {}
def run(thinkers):
	global rst
	print thinkers
	filepath = 'datafile_%s_%s.py'%(config.mode, '_'.join(thinkers))
	for i in xrange(config.times):
		now = time.time()
		rst.setdefault(tuple(thinkers), [])
		rst[tuple(thinkers)].append(main(i, thinkers))
		print time.time() - now 
		print rst
		maps_data = pprint.pformat(maps)
		with open(filepath, 'w') as f:
			f.write('data = \\\n%s'%maps_data)

if config.mode in ('compare', 'compareAll'):
	if not hasattr(config, 'thinkers'):
		config.thinkers = mThinker.thinkers.keys()
	for i in config.thinkers:
		for j in config.thinkers:
			#if i == j or (j, i) in rst:
			if i == j:
				continue
			run([i, j])
else:
	run(config.thinkers)	

