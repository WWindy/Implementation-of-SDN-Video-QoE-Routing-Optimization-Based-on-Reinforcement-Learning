# -*-coding:UTF-8 -*-
import heapq
import numpy as np
class Dijkstra():
	# 矩阵转图
	def matrix_to_graph(self,matrix):
	    graph = {}
	    size = len(matrix)
	    for i in range(size):
		for j in range(size):
		    if i == j:
		        continue
		    weight = matrix[i][j]
		    if weight == 0:
		        continue
		    if i not in graph:
		        graph[i] = []
		    graph[i].append((j, weight))
	    return graph

	# Dijkstra算法
	def dijkstra(self, graph, start, end):
	    heap = [(0, [start])]
	    visited = set()
	    while heap:
		(cost, path) = heapq.heappop(heap)
		node = path[-1]
		if node in visited:
		    continue
		visited.add(node)
		if str(node) == str(end):
		    return path
		for neighbor, weight in graph.get(node, []):
		    new_cost = cost + weight
		    new_path = path + [neighbor]
		    heapq.heappush(heap, (new_cost, new_path))
	    return None

	# 获取路径上的边权重
	def get_path_weights(self,path, graph):
	    weights = []
	    for i in range(len(path)-1):
		node1, node2 = path[i], path[i+1]
		for neighbor, weight in graph.get(node1, []):
		    if neighbor == node2:
		        weights.append(weight)
		        break
	    return weights

	# 以列表形式显示路径上的节点和边权重
	def format_path(self,path, weights):
	    res = str(path[0])
	    for i in range(1, len(path)):
		res +=str(path[i]+1)
	    return res
	def get_a(self,s):
		print(s)
		graph = self.matrix_to_graph(s)
		start = 0 # 交换机1对应的节点编号为0
		end = 1   # 交换机2对应的节点编号为1
		path = self.dijkstra(graph, start, end)
		a=""
		for i in range(len(path)):
			a+=str(path[i]+1)
		return a










