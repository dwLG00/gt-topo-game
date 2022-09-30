import random
import math

S = 0
T = 0

class Graph:
	def __init__(self, nodes, edges):
		self.nodes = nodes
		self.edges = edges[:]
		for edge in edges:
			s, d = edge
			if (d, s) not in self.edges:
				self.edges.append((d, s))

	def source_edges(self, node):
		return [edge for edge in self.edges if edge[0] == node]

	def dest_edges(self, node):
		return [edge for edge in self.edges if edge[1] == node]

def game_eval(s1, s2, s=S, t=T):
	if s1 == 0 and s2 == 0:
		return 1
	if s1 == 1 and s2 == 1:
		return 0
	if s1 == 1 and s2 == 0:
		return t
	if s1 == 0 and s2 == 1:
		return s

def rchange(p, c):
	r = random.random()
	return c if r > p else (1 if c == 0 else 0)

class Game:
	def __init__(self, graph, agents):
		self.graph = graph
		self.agents = agents

	def play(self, t, beta, S, T):
		strategies = [{}]
		for ag in self.agents:
			strategies[0][ag] = random.choice([0, 1])

		#evaluate
		pchange = {}
		for ag in self.agents:
			strat = strategies[-1][ag]
			cstrat = 1 if strat == 0 else 0

			next_to = [edge[1] for edge in self.graph.source_edges(ag) if edge[1] in self.agents]
			payoff = sum( (game_eval(strat, strategies[-1][op], s=S, t=T) for op in next_to))
			cpayoff = sum( (game_eval(cstrat, strategies[-1][op], s=S, t=T) for op in next_to))
			dpayoff = payoff - cpayoff
			p = 1 / (1 + math.e**(-beta * dpayoff))
			pchange[ag] = p

		for _ in range(t):
			strategies.append({})
			for ag in self.agents:
				strategies[-1][ag] = rchange(pchange[ag], strategies[-2][ag])

			for ag in self.agents:
				strat = strategies[-1][ag]
				cstrat = 1 if strat == 0 else 0

				next_to = [edge[1] for edge in self.graph.source_edges(ag) if edge[1] in self.agents]
				payoff = sum( (game_eval(strat, strategies[-1][op], s=S, t=T) for op in next_to))
				cpayoff = sum( (game_eval(cstrat, strategies[-1][op], s=S, t=T) for op in next_to))
				dpayoff = cpayoff - payoff
				p = 1 / (1 + math.e**(-beta * dpayoff))
				pchange[ag] = p

		return strategies
