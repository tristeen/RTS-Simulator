mode = 'compare'
iter_times = 256

if mode == 'debug':
	draw_dot_every_iter = False
	show_dot_every_iter = False
	draw_dot_every_mcts = True
	show_dot_every_mcts = False
	view = True
	log = False
	times = 1
	map_name = 'map2'
	debug_pause = False
	thinkers = ['ThinkerNewMCTS', 'ThinkerWeightedChoice']
elif mode == 'compare':
	draw_dot_every_iter = False
	show_dot_every_iter = False
	draw_dot_every_mcts = False
	show_dot_every_mcts = False
	view = False
	log = False
	times = 2
	map_name = 'map3'
	debug_pause = False
	#thinkers = ['ThinkerNewMCTS', 'ThinkerMCTS', 'ThinkerMCTS_RC', 'ThinkerNaiveMCTS', 'ThinkerEG', 'ThinkerUCT', 'ThinkerWeightedChoice',]
	#thinkers = ['ThinkerNewMCTS', 'ThinkerMCTS', 'ThinkerMCTS_RC', 'ThinkerWeightedChoice',]
	thinkers = ['ThinkerNewMCTS', 'ThinkerNaiveMCTS', 'ThinkerEG', 'ThinkerUCT']
	#thinkers = ['ThinkerMCTS', 'ThinkerWeightedChoice']
	#thinkers = ['ThinkerNaiveMCTS', 'ThinkerNewMCTS', 'ThinkerMCTS']
	#thinkers = ['ThinkerEG', 'ThinkerNewMCTS']
	#thinkers = ['ThinkerMCTS', 'ThinkerEG']
elif mode == 'compareAll':
	draw_dot_every_iter = False
	show_dot_every_iter = False
	draw_dot_every_mcts = False
	show_dot_every_mcts = False
	view = False
	log = False
	times = 10
	map_name = 'map3'
	debug_pause = False
