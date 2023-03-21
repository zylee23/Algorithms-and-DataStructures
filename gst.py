"""
Lee Zi Yan
31264689
"""

#%%
import sys

# read the input file, assuming that the file number is 1, 2, 3, ... N
def read_file(file):
  txt, pat = [], []
  f = open(file, "r", encoding = "UTF-8")

  numOfTexts = int(f.readline().strip("\n"))
  for _ in range(numOfTexts):
    txtFile = f.readline().strip().split()[1]
    txtFile = open(txtFile, "r", encoding = "UTF-8")
    text = txtFile.read() + "$"
    txtFile.close()
    txt.append(text)

  numOfPats = int(f.readline().strip("\n"))
  for _ in range(numOfPats):
    patFile = f.readline().strip().split()[1]
    patFile = open(patFile, "r", encoding = "UTF-8")
    pattern = patFile.readline().strip()
    patFile.close()
    pat.append(pattern)

  f.close()
  return txt, pat

# write the answer to the output file
def write_file(res):
  f = open("output_gst.txt", "w", encoding = "UTF-8")
  for i in range(len(res)):
    f.write(str(res[i][0]) + " " + str(res[i][1]) + " " + str(res[i][2]) + "\n")
  f.close()


# global end variable
class End:
  def __init__(self):
    self.n = -1

  def increment(self):
    self.n += 1

  def get(self):
    return self.n


class Node:
  def __init__(self, id = None):
    self.edges = [None] * 128
    # suffix link
    self.link = None
    self.id = []
    if id is not None:
      self.id.append(id)

  # add suffix id to node
  def add_id(self, id):
    self.id.append(id)


class Edge:
  def __init__(self, index, start, end, node):
    # the index of the text to compare
    self.index = index
    self.start = start
    self.end = end
    self.node = node


class Active:
  def __init__(self, node):
    self.node = node
    self.edge = None
    self.length = 0


class GST:
  def __init__(self, txt):
    self.root = Node()
    self.txt = txt
    self.build()

  def build(self):
    for i in range(len(self.txt)):
      ukkonen(self.root, self.txt, i, self.txt[i])

  def suffix_array(self):
    return self.traverse(self.root, [])

  # inorder traversel of tree
  def traverse(self, node, arr):
    if len(node.id) > 0:
      for i in range(len(node.id)):
        arr.append(node.id[i])
    else:
      for i in range(128):
        if node.edges[i] is not None:
          self.traverse(node.edges[i].node, arr)
    return arr

  # search for exact pattern in tree, return the suffix ids
  def search(self, pat):
    n, skip = 0, 0
    node = self.root
    edge = node.edges[ord(pat[n])]
    if edge is None:
      return []

    while edge is not None and n < len(pat):
      start = edge.start
      end = edge.end if isinstance(edge.end, int) else edge.end.get()

      # traverse down if at the end of edge
      if skip == end - start + 1:
        node = edge.node
        edge = node.edges[ord(pat[n])]
        skip = 0
        continue

      if self.txt[edge.index][edge.start + skip] == pat[n]:
        n += 1
        skip += 1
      else:
        break

    # if exact pattern is matched
    if n == len(pat):
      if edge is not None:
        node = edge.node
      return self.traverse(node, [])
    else:
      return []


# def ukkonen(root, txt, index, s, first=False):
# index is the index of word being inserted into the tree
def ukkonen(root, txt, index, s):
  active = Active(root)
  end = End()
  i, j = 0, 0
  remainder = 0

  # function to move to the next active node and edge
  def next(slink, j, remainder):
    # check if there is suffix link
    if not slink and active.node.link is not None and active.node.link is not root:
      slink = True
    # if there is suffix link, follow. active length unchanged
    if slink and active.node is not root:
      active.node = active.node.link
      if active.edge is not None:
        active.edge = active.node.edges[ord(txt[active.edge.index][active.edge.start])]
    # if no suffix link, intermediate node goes back to root
    # find next edge
    # decrease active length by setting to remainder
    else:
      if active.node.link is not None:
        active.node = active.node.link
      active.edge = active.node.edges[ord(s[j])]
      active.length = remainder
    return slink

  # traverse down if active length is more than length of edge
  def traverse(i, index):
    while active.edge is not None and isinstance(active.edge.end, int) and active.length > active.edge.end - active.edge.start:
      edgeLength = active.edge.end - active.edge.start + 1
      active.node = active.edge.node
      # active length is more than edge length, go down to the next active edge
      if active.length > edgeLength:
        active.length -= edgeLength
        active.edge = active.node.edges[ord(txt[index][i-active.length])]
      else:
      # active length is the same as edge length
        active.edge = None
        active.length = 0

  while i < len(s):
    # increase global end
    end.increment()
    # remember the new node created in same i for suffix link
    pred = None
    # current i is following suffix link
    slink = False

    while j <= i:
      # traverse down
      if active.edge is not None and remainder != 0:
        traverse(i, index)

      c = ord(s[i])
      # skip count
      skip = i-j if active.edge is None else active.edge.start + active.length

      # if reach the end of string and the last char of string is $, add suffix id
      if i == len(s)-1 and active.edge is not None and ord(txt[active.edge.index][active.edge.start + active.length]) == 36:
        active.edge.node.add_id((index, j))
        j += 1
        remainder -= 1
        if j == len(s):
          i += 1
          break
        slink = next(slink, j, remainder)

      # if reach the end of string and the last char of string is $, add suffix id
      elif i == len(s)-1 and active.edge is None and active.node.edges[c] is not None:
        active.node.edges[c].node.add_id((index, j))
        j += 1
        remainder -= 1
        if j == len(s):
          i += 1
          break
        slink = next(slink, j, remainder)

      # rule 2: branching if there is no leaf
      elif active.node.edges[c] is None and active.edge is None:
        # increase i and j if i == j
        if i == j:
          active.node.edges[c] = Edge(index, j, end, Node((index, j)))
          i += 1
          j += 1
          break
        else:
          # increase j if i is at the end of string
          active.node.edges[c] = Edge(index, i, end, Node((index, j)))
          j += 1
          remainder -= 1
          slink = next(slink, j, remainder)

      # rule 2: branching for intermediate node
      elif active.edge is not None and active.length != 0 and txt[active.edge.index][skip] != s[i]:
        curNode = active.edge.node
        curEnd = active.edge.end
        # set the end for current active edge
        active.edge.end = skip - 1
        # create intermediate node
        active.edge.node = Node()
        active.edge.node.edges[ord(txt[active.edge.index][skip])] = Edge(active.edge.index, skip, curEnd, curNode)
        active.edge.node.edges[c] = Edge(index, i, end, Node((index, j)))

        # link new node to root
        active.edge.node.link = root
        if pred is not None:
          # if a node is created in same i, link together
          pred.link = active.edge.node
        pred = active.edge.node

        # increase j, look for next node and edge
        j += 1
        remainder -= 1
        slink = next(slink, j, remainder)

      # rule 3: showstopper
      else:
        i += 1
        if active.edge is None:
          active.edge = active.node.edges[c]
        active.length += 1
        remainder +=1
        break


# return all the combinations of uppercase and lowercase of a text
def all_combo(s):
  if len(s) == 1:
    if ord(s) > 64 and ord(s) < 91 or ord(s) > 96 and ord(s) < 122:
      return [s.upper(), s.lower()]
    else:
      return [s]
  else:
    return [i+j for i in all_combo(s[0]) for j in all_combo(s[1:])]

# find pattern in  gst
def pattern_matching(gst, pat):
  res = []
  # create all possible combination
  for i in range(len(pat)):
    patCombo = all_combo(pat[i])
    # for each string in possible combination
    for j in range(len(patCombo)):
      match = gst.search(patCombo[j])
      # query in gst, change pattern, text and character to 1-indexed
      for k in range(len(match)):
        res.append((i+1, match[k][0]+1, match[k][1] + 1))

  return res


if __name__ == "__main__":
  txt, pat = read_file(sys.argv[1])
  gst = GST(txt)
  answer = pattern_matching(gst, pat)
  write_file(answer)