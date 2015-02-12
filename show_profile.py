import pstats
p=pstats.Stats('test.out')
p.sort_stats('time').print_stats()
