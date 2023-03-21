"""
Lee Zi Yan
31264689
"""


import sys
from bitarray import bitarray
from bitarray.util import ba2int


# node class for the binary search tree
class Node:
  def __init__(self):
    self.left = None
    self.right = None
    self.char = None


# binary search tree for huffman decoding
class BST:
  def __init__(self):
    self.root = Node()


# read binary stream of bits from a file and put it in a bitarray
def read_file(filename):
  res = bitarray()
  with open(filename, "rb") as f:
    res.fromfile(f)
  return res


# write data to a file
def write_file(filename, data):
  with open(filename, "w", encoding = "utf-8") as f:
    f.write(data)


# convert 8-bit ascii code to character
def decode_8_bit_ascii(input, ptr):
  res = chr(ba2int(input[ptr[0] : ptr[0] + 8]))
  ptr[0] += 8
  return res


# build the huffman decoding binary search tree (bst)
def huffman_decoding_bst(input, ptr, distinct):
  codes = []

  # get the characters and codewords
  for i in range(distinct):
    char = decode_8_bit_ascii(input, ptr)

    codeLength = elias_decoding(input, ptr)

    code = input[ptr[0] : ptr[0] + codeLength]
    ptr[0] += codeLength

    codes.append((char, code))

  bst = BST()
  # build bst with each codeword
  for c in codes:
    cur = bst.root

    for bit in c[1]:

      if bit == 0:
        if cur.left is None:
          cur.left = Node()
        cur = cur.left

      else:
        if cur.right is None:
          cur.right = Node()
        cur = cur.right

    # add character to the leaf
    cur.char = c[0]

  return bst


# huffman decoding with a bst
def huffman_decoding(input, ptr, bst):
  cur = bst.root

  # traverse bst until reach leaf
  while True:
    bit = input[ptr[0]]
    if bit == 0:
      cur = cur.left
    else:
      cur = cur.right
    ptr[0] += 1

    if cur.char is not None:
      return cur.char


# elias decoding over non-negative integers
def elias_decoding(input, ptr):
  length = 1
  cur = input[ptr[0] : ptr[0] + length]

  # while cur is not the integer
  while cur[0] == 0:
    # point to the start of next length
    ptr[0] += length
    # change msb to 1
    cur[0] = 1
    # convert binary to integer, add 1
    length = ba2int(cur) + 1
    # get the next length
    cur = input[ptr[0] : ptr[0] + length]

  # convert codeword to integer
  res = ba2int(cur) - 1
  ptr[0] += length

  return res


# decode lz77 tuples, return the list of lz77 3-tuples of the form (offset, length, next char)
def lz77_tuples_decoding(input, ptr, dataLength, bst):
  # number of characters of the string
  numOfChar = 0
  tuples = []

  # while encoded string is less than the length of data
  while numOfChar < dataLength:
    offset = elias_decoding(input, ptr)
    length = elias_decoding(input, ptr)
    nextChar = huffman_decoding(input, ptr, bst)
    tuples.append((offset, length, nextChar))

    numOfChar += length + 1

  return tuples


# build the string from lz77 tuples
def build_string(tuples):
  s = []

  for t in tuples:
    offset, length, nextChar = t[0], t[1], t[2]

    # add next character if offset is 0
    if offset == 0:
      s.append(nextChar)

    # else, add characters according to the offset over the range of length
    else:
      for _ in range(length):
        s.append(s[len(s) - offset])

      s.append(nextChar)

  return "".join(s)


# decode encoding that contains information of a file over the header part and the data part
def decoder(input):
  # pointer to the start of encoded segment
  ptr = [0]

  # decode filename length
  filenameLength = elias_decoding(input, ptr)

  # decode the filename
  filename = []
  for i in range(filenameLength):
    char = decode_8_bit_ascii(input, ptr)
    filename.append(char)
  filename = "".join(filename)

  # decode data length
  dataLength = elias_decoding(input, ptr)

  # decode number of distinct characters
  distinct = elias_decoding(input, ptr)

  # huffman decoding bst
  bst = huffman_decoding_bst(input, ptr, distinct)

  # lz77 tuples decoding
  tuples = lz77_tuples_decoding(input, ptr, dataLength, bst)

  # build string from lz77 tuples
  data = build_string(tuples)

  return filename, data


if __name__ == "__main__":
  # get argument filename
  filename = sys.argv[1]

  # read file
  input = read_file(filename)

  # decode
  filename, data = decoder(input)

  # write file
  write_file(filename, data)