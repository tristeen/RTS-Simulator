import BaseMCTS
import mThinker
import random
import config

class Node(BaseMCTS.Node):

	def __init__(self, move=None, parent=None, state=None):
		super(Node, self).__init__(move, parent, state)

	def select_child(self):
		if random.random() < 0.9 and len(self.childNodes) > 10:
			s = sorted(self.childNodes, key=lambda c: c.wins / c.visits)[-1]
			return s, True
		else:
			move = self.state.GetRandomMove()
			s, old = self.add_child(move, self.state)
			return s, old


def MCTS(rootstate, itermax):
	dirnum, filenum = 0, 0
	dirname, dirnum, filenum = BaseMCTS.mkdir(dirnum, filenum)
	rootnode = Node(state=rootstate)

	thinker = mThinker.ThinkerWeightedChoice()

	for i in range(itermax):
		state = rootstate.Clone()

		# log.info('Select')
		node, old = rootnode, True
		while old:
			node, old = node.select_child()
		
		# log.info('Rollout')
		state = node.state.Clone()
		# for j in xrange(32):
		for j in xrange(8):
			thinker.set_map(state.to_dict())
			action = thinker.get_action(state.camp)
			# state.DoMove(state.GetRandomMove())
			state.DoMove(action)

		# log.info('Backpropagate')
		while node != None:
			result = state.GetResult(not node.camp)
			node.update(None, result)
			if node.parentNode:
				#node.parentNode.update(node.move, result)
				node = node.parentNode
			else:
				break

		#raw_input('press any key to continue')
		if config.draw_dot_every_iter or config.show_dot_every_iter:
			draw_dot(rootnode, dirname, filenum, config.show_dot_every_iter)

	if config.draw_dot_every_mcts or config.show_dot_every_mcts:
		draw_dot(rootnode, dirname, filenum, config.show_dot_every_mcts)
	# print sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move
	# return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move
	# print 'rootnode.childNodes', rootnode.childNodes
	return sorted(rootnode.childNodes, key=lambda c: sum(c.result) / len(c.result))[-1].move
