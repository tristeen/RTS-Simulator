from rts import mView
import time
from rts import mMap
import sys

if len(sys.argv) >= 2:
	datafile = __import__(sys.argv[1])
else:
	datafile = __import__('datafile')

for i, maps in datafile.data.iteritems():
	for map_data in maps:
		_map = mMap.mMap(map_data)
		mv = mView.mView(_map)
		time.sleep(0.5)
		mv.loop()
	raw_input('Press any key to continue:')
