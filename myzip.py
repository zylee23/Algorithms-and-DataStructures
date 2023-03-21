"""
Lee Zi Yan
31264689
"""


import sys
import heapq
from bitarray import bitarray


# read data from given file
def read_file(file):
	with open(file, "r", encoding = "utf-8") as f:
		data = f.read()
	return data


# write a binary stream of bits to a .bin file
def write_file(filename, encoding):
	with open("".join((filename, ".bin")), "wb") as f:
		encoding.tofile(f)


# convert character to 8-bit ascii code
def char_8_bit_ascii(c):
	return bitarray(format(ord(c), "08b"))


# update the huffman encoding table
def update_encoding(arr, s, n):
	# for each character in string s
	for c in s:
		index = ord(c)

		# prepend bit n if character already has codeword
		if arr[index] is not None:
			arr[index] = bitarray(n) + arr[index]

		# add bit n
		else:
			arr[index] = bitarray(n)


# given a string, get the number of distinct characters
# and encoding table that contains the codewords for the distinct characters
def huffman_encoding(s):
	frequency = [0] * 255
	encoding = [None] * 128

	# calculate frequency of characters
	for c in s:
		frequency[ord(c)] += 1

	distinct = 0
	heap = []
	# create the array for heap
	for i in range(len(frequency)):
		if frequency[i] != 0:
			# calculate number of distinct characters
			distinct += 1
			# append (frequency, length of characters, characters)
			heap.append((frequency[i], 1, chr(i)))

	# base case if string only has 1 character
	if len(heap) == 1:
		update_encoding(encoding, heap[0][2], "0")

	else:
		heapq.heapify(heap)

		while heap:
			# pop two smallest items from heap
			a = heapq.heappop(heap)
			b = heapq.heappop(heap)

			# update codewords in encoding table
			update_encoding(encoding, a[2], "0")
			update_encoding(encoding, b[2], "1")

			# if heap is not empty, append (frequency of a+b, length of a+b, a+b)
			if len(heap) != 0:
				heapq.heappush(heap, ((a[0] + b[0], a[1] + b[1], "".join((a[2], b[2])))))

	return distinct, encoding


# elias encoding over non-negative integers
def elias(n):
	n = n + 1

	# convert n to binary
	cur = bitarray(format(n, "b"))
	# encoding array to get the all the encodings
	encoding = [cur]

	# while cur is not 1
	while len(cur) > 1:
		# binary(length of binary(cur) - 1)
		cur = bitarray(format(len(cur) - 1, "b"))
		# change msb to 0
		cur[0] = 0
		encoding.append(cur)

	# reverse the encodings to get the elias codeword
	res = bitarray()
	for i in range(len(encoding) - 1, -1, -1):
		res.extend(encoding[i])

	return res


# z-algorithm
def z_algo(s):
	n = len(s)
	# initialise z-array
	z = [0] * n
	z[0] = n

	l = 0
	r = 0
	for i in range(1, n):
		# if outside of z-box
		if i > r:
			l = i
			r = i
			while r < n and s[r] == s[r-l]:
				r += 1
			z[i] = r - l
			r -= 1

		# if within z-box
		else:
			k = i - l
			rem = r - i + 1

			if z[k] < rem:
				z[i] = z[k]

			elif z[k] == rem:
				l = i
				while r < n and s[r] == s[r-l]:
					r += 1
				z[i] = r - l
				r -= 1

			else:
				z[i] = rem

	return z


# get LZ77 3-tuples of the form (offset, length, next char)
def lz77_tuples(s, window, buffer):
	# initialise ptr, start of search window W, end of lookahead buffer L
	ptr = 0
	windowStart = 0
	bufferEnd = ptr + buffer if ptr + buffer < len(s) else len(s)

	tuples = []
	while ptr < len(s):
		# slice string s to get LWL
		sw = s[windowStart:ptr]
		lb = s[ptr:bufferEnd]
		z = z_algo(lb + sw + lb)

		offset = 0
		length = 0
		# iterte through the z-values in W
		for i in range(bufferEnd - ptr, bufferEnd - windowStart):
			# get the the longest length and calculate the offset from ptr
			if z[i] >= length:
				offset = bufferEnd - windowStart - i
				length = z[i]
				# ensure length is not longer than W
				if length > bufferEnd - ptr:
					length = bufferEnd - ptr

		# if no matches in W
		if length == 0:
			tuples.append((0, 0, s[ptr]))
		else:
			# if next character fall off s, length -= 1
			if ptr + length == len(s):
				length -= 1
			tuples.append((offset, length, s[ptr + length]))

		# update the ptr, start of W, end of L
		ptr = ptr + length + 1
		windowStart = ptr - window if ptr - window > 0 else 0
		bufferEnd = ptr + buffer if ptr + buffer < len(s) else len(s)

	return tuples


# encodes all the information in the input file over the header part and the data part
def encoder(filename, data, searchWindow, lookaheadBuffer):
	res = bitarray()

	# get the number of distinct characters and huffman encoding table
	distinct, huffman = huffman_encoding(data)

	# encode length of filename
	res.extend(elias(len(filename)))

	# encode filename
	for c in filename:
		res.extend(char_8_bit_ascii(c))

	# encode length of data
	res.extend(elias(len(data)))

	# encode number of distinct characters
	res.extend(elias(distinct))

	# 8-bit ascii code of distinct character, length of huffman codeword and huffman codeword
	for i in range(len(huffman)):
		if huffman[i] is not None:
			res.extend(char_8_bit_ascii(chr(i)))
			res.extend(elias(len(huffman[i])))
			res.extend(huffman[i])

	# get lz77 tuples
	tuples = lz77_tuples(data, searchWindow, lookaheadBuffer)
	# encode lz77 tuples
	for tuple in tuples:
		res.extend(elias(tuple[0]))
		res.extend(elias(tuple[1]))
		res.extend(huffman[ord(tuple[2])])

	return res


if __name__ == "__main__":
	# get arguments (python myzip.py <inputfilename> <W> <L>)
	filename = sys.argv[1]
	searchWindow = int(sys.argv[2])
	lookaheadBuffer = int(sys.argv[3])

	# read data
	data = read_file(filename)

	# encoding
	res = encoder(filename, data, searchWindow, lookaheadBuffer)

	# write to file
	write_file(filename, res)