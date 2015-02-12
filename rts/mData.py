from mUnit import UNIT_NONE, UNIT_SOLDIER, UNIT_BASE, UNIT_WORKER, UNITS, UNIT_RES
import mMap

map1 = {'length': 20,
		'heigth': 20,
		'default': UNIT_NONE,
		'data': {
			(1, 2): UNIT_SOLDIER,
			(1, 3): UNIT_SOLDIER,
			(3, 2): UNIT_BASE,
			(5, 4): UNIT_RES,
			(6, 5): UNIT_WORKER,
			#(4, 3): UNIT_BASE,
			(15, 16): UNIT_BASE,
			(18, 16): UNIT_RES,
			(18, 17): UNIT_WORKER,
		},
	}

map2 = {'length': 12,
		'heigth': 12,
		'default': UNIT_NONE,
		'data': {
			(2, 1): UNIT_WORKER,
			(3, 1): UNIT_BASE,
			(1, 1): UNIT_RES,
			#(4, 3): UNIT_BASE,
			(8, 10): UNIT_BASE,
			(10, 10): UNIT_RES,
			(9, 10): UNIT_WORKER,
		},
	}
	
map3 = {'length': 6,
		'heigth': 6,
		'default': UNIT_NONE,
		'data': {
			(1, 1): UNIT_BASE,
			(0, 0): UNIT_RES,
			#(4, 3): UNIT_BASE,
			(4, 4): UNIT_BASE,
			(5, 5): UNIT_RES,
			#(5, 1): UNIT_WORKER,
		},
	}

map4 = {'length': 8,
		'heigth': 8,
		'default': UNIT_NONE,
		'data': {
			(1, 1): UNIT_BASE,
			(0, 0): UNIT_RES,
			#(4, 3): UNIT_BASE,
			(6, 6): UNIT_BASE,
			(7, 7): UNIT_RES,
			#(5, 1): UNIT_WORKER,
		},
	}

def init_map(map_data):
	_map = mMap.mMap(map_data)
	if map_data == map1:
		_unit2 = _map[15][16]
		_unit2.camp_ = 1
		_unit4 = _map[18][16]
		_unit4.camp_ = 1
		_unit4 = _map[18][17]
		_unit4.camp_ = 1
	elif map_data == map2:
		_unit2 = _map[8][10]
		_unit2.camp_ = 1
		_unit4 = _map[9][10]
		_unit4.camp_ = 1
		_unit3 = _map[10][10]
		_unit3.camp_ = 1
	elif map_data == map3:
		_unit2 = _map[4][4]
		_unit2.camp_ = 1
		_unit4 = _map[5][5]
		_unit4.camp_ = 1
	elif map_data == map4:
		_unit2 = _map[6][6]
		_unit2.camp_ = 1
		_unit4 = _map[7][7]
		_unit4.camp_ = 1
	return _map

maps = {
	'map1': init_map(map1),
	'map2': init_map(map2),
	'map3': init_map(map3),
	'map4': init_map(map4),
}
