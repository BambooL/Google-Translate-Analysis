import re
from collections import deque
from tarjan import tarjan


f = open('res', 'r+')
graph = {}
self_not_contain = []
false = 0
while True:
	line = f.readline()
	if not line:
		break
	else:
		if ("is better than" in line):
			false = false + 1
			u1 = line.split(" is better than ")[0]
			u2 = line.split(" is better than ")[1][:-1]
			if (not u1 == u2):
				if (u1 in graph.keys()):
					if (u2 in graph[u1]): 
						newlist = graph[u1]
						newlist = newlist.remove(u2)
						if newlist is None:
							newlist = []
						graph[u1] = newlist
						self_not_contain.append([u1, u2])
						continue
				if (u2 in graph.keys()):
					graph[u2].append(u1)
				else:
					graph[u2] = [u1]
# print graph
print "The Google Ranking of Universities:"
print tarjan(graph)
 








