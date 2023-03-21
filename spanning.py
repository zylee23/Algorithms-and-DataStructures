"""
Lee Zi Yan
31264689
"""

import sys
import math

# read the input file
def read_file(file):
  f = open(file, "r", encoding = "UTF-8")
  input = [line.strip().split() for line in f]
  f.close()
  return input

# write the answer to output file
def write_file(mst1, weight1, mst2, weight2):
  f = open("output_spanning.txt", "w", encoding = "UTF-8")

  f.write("Smallest Spanning Tree Weight = " + str(weight1))
  f.write("\n#List of edges in the smallest spannnig tree:\n")
  mst1.sort(key = lambda x: (x[0], x[1]))
  for e in mst1:
    f.write(str(e[0]) + " " + str(e[1]) + " " + str(e[2]) + "\n")

  f.write("Second-smallest Spanning Tree Weight = " + str(weight2))
  f.write("\n#List of edges in the second smallest spannnig tree:\n")
  mst2.sort(key = lambda x: (x[0], x[1]))
  for e in mst2:
    f.write(str(e[0]) + " " + str(e[1]) + " " + str(e[2]) + "\n")

  f.close()

class Graph:
  def __init__(self, n):
    self.vertices = n
    self.edges = []
    # stores the smallest mst
    self.mst = [[] for i in range(n)]

  def add_edge(self, e):
    self.edges.append((int(e[0]), int(e[1]), int(e[2])))

  # create the adjacency list for smallest mst
  def build_mst(self, u, v, w):
    self.mst[u].append((v, w))
    self.mst[v].append((u, w))


# recursive find with path compression
def find(a, rank):
  if rank[a] < 0:
    return a
  else:
    rank[a] = find(rank[a], rank)
    return rank[a]

def union(u, v, rank):
  # if height_u < height_v
  if rank[u] > rank[v]:
    rank[u] = v
    rank[v] -= 1
  # if height_u > height_v or height_u == height_v
  else:
    rank[v] = u
    rank[u] -= 1

# find first mst and list the unused edges
def kruskal_mst(g):
  g.edges.sort(key = lambda x: x[2])
  rank = [-1] * (g.vertices)
  mst, unused = [], []
  total = 0
  n = 0
  for e in g.edges:
    u, v, w = e[0]-1, e[1]-1, e[2]
    rootu = find(u, rank)
    rootv = find(v, rank)
    if n < g.vertices-1 and rootu != rootv:
      union(rootu, rootv, rank)
      mst.append(e)
      g.build_mst(u, v, w)
      total += w
      n += 1
    else:
      unused.append(e)
  return mst, total, unused

# build the mst with first vertex as root with dfs
# calculate the depth of each vertex from the root
# record the parent of each vertex and the weight of edge to parent
def dfs(g):
  n = g.vertices
  visited = [False] * n
  parent = [-1] * n
  depth = [0] * n

  stack = []
  # the vertex with the most neighbours is the root
  stack.append(max(range(len(g.mst)), key=lambda i: g.mst[i]))
  while stack:
    s = stack[-1]
    stack.pop()

    if not visited[s]:
        visited[s] = True

    for e in g.mst[s]:
      d, w = e[0], e[1]
      if not visited[d]:
          stack.append(d)
          parent[d] = (s, w)
          depth[d] = depth[s] + 1
  return parent, depth

# find two mst for a graph
def two_smallest_mst(g):
  mst1, total1, unused = kruskal_mst(g)
  parent, depth = dfs(g)

  out = None
  add = None
  curr = None
  diff = math.inf
  # for each unused edge, insert into mst1, find the max edge from the cycle created
  # calculate the difference between the unused edge and heaviest edge in cycle
  # calculate the difference between mst1 and mst'
  for e in unused:
    u, v, w = e[0]-1, e[1]-1, e[2]
    res = -1
    while u != v:
      du = depth[u]
      dv = depth[v]
      if du >= dv:
        if parent[u][1] > res:
          res = parent[u][1]
          curr = u
        u = parent[u][0]
      if dv >= du:
        if parent[v][1] > res:
          res = parent[v][1]
          curr = v
        v = parent[v][0]

    # record the mst' with with the least difference
    if w - res < diff:
      out = (curr+1, parent[curr][0]+1, parent[curr][1]) if curr < parent[curr][0] else (parent[curr][0]+1, curr+1, parent[curr][1])
      add = e
      diff = w - res
      # if no difference after replacing edge, break
      if diff == 0:
        break

  mst2 = mst1[::]
  mst2.remove(out)
  mst2.append(add)

  return mst1, total1, mst2, total1+diff

if __name__ == "__main__":
  input = read_file(sys.argv[1])
  g = Graph(int(input[0][0]))
  for i in range(1, len(input)):
    g.add_edge(input[i])
  mst1, weight1, mst2, weight2 = two_smallest_mst(g)
  write_file(mst1, weight1, mst2, weight2)