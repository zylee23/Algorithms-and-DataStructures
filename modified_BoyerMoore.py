"""
Lee Zi Yan
31264689
"""

import sys


def read_file(filename):
  # read a string from a file
  with open(filename, "r", encoding="utf-8") as f:
    string = f.read()
  f.close()
  return string


def write_file(matches):
  # write the output of boyer moore to a file
  with open("output_modified_BoyerMoore.txt", "w", encoding="utf-8") as f:
    for i in range(len(matches)):
      output = str(matches[i]) + "\n"
      f.write(output)
  f.close()


def z_algo(pat):
  # process a pattern string to return a z-array
  zArr = [0] * len(pat)
  zArr[0] = len(pat)

  L, R = 0, 0
  for i in range(1, len(pat)):

    if i >= R:   # outside z-box
      ptr = 0
      for j in range(i, len(pat)):
        if pat[j] == pat[ptr]:
          zArr[i] += 1
          ptr += 1
        else:
          break
      L, R = i, i + zArr[i]

    else:   # inside z-box
      k, remainder = i - L, R - i

      if zArr[k] < remainder:   # case 2a
        zArr[i] = zArr[k]
      elif zArr[k] == remainder:   #case 2b
        zArr[i] = zArr[k]
        ptr = remainder
        for j in range(R, len(pat)):
          if pat[j] == pat[ptr]:
            zArr[i] += 1
            ptr += 1
          else:
            break
        L, R = i, i + zArr[i]
      elif zArr[k] > remainder:   #case 2c
        zArr[i] = remainder

  return zArr


def z_suffix(pat):
  # runs z algo from right to left
  zSuf = [0] * len(pat)
  zSuf[-1] = len(pat)
  n = len(pat) - 1

  L, R = n, n
  for i in range(n - 1, -1, -1):

    if i <= L:   # outside z-box on the left
      ptr = n
      for j in range(i, -1, -1):
        if pat[j] == pat[ptr]:
          zSuf[i] += 1
          ptr -= 1
        else:
          break
      L, R = i - zSuf[i], i

    else:   # inside z-box
      k, remainder = i + n - R, i - L

      if zSuf[k] < remainder:
        zSuf[i] = zSuf[k]
      elif zSuf[k] == remainder:
        zSuf[i] = zSuf[k]
        ptr = n - 1
        for j in range(L, -1, -1):
          if pat[j] == pat[ptr]:
            zSuf[i] += 1
            ptr -= 1
          else:
            break
        L, R = i - zSuf[i], i
      elif zSuf[k] > remainder:
        zSuf[i] = remainder

  return zSuf


def bad_character_table(pat):
  # Bad character table for extended bad character rule

  # Initialise to an array instead of matrix to save space
  table = [None] * 96   # 95 printable ascii

  for i in range(len(pat)-1, -1, -1):
    character = ord(pat[i]) - 32

    if table[character] is None:
      # only initialise when character exist
      table[character] = [-1] * len(pat)
    table[character][i] = i

    # loop to the right to update until it reaches another index/end
    k = i
    while k < len(pat)-1 and table[character][k+1] < 0:
      table[character][k+1] = i
      k += 1

  return table


def modified_good_suffix(pat):
  # Good suffix array
  n = len(pat)
  goodSuf = [0] * (n+1)
  zSuf = z_suffix(pat)

  for i in range(0, n-1):
    k = n - zSuf[i]
    goodSuf[k] = i

  return goodSuf


# def modified_good_suffix(pat):
#   # character before the good suffix position matches the mismatched character
#   # second element is the shift to the next suffix
#   pass


def matched_prefix(pat):
  # Matched prefix array

  # +1 to shift when len(pat)=1 matches on the last char of text
  matchedPrefix = [0] * (len(pat)+1)
  zArr = z_algo(pat)

  for i in range(len(pat)-1, -1, -1):
    if zArr[i] + i == len(pat):
      matchedPrefix[i] = zArr[i]
    else:
      if i < len(pat)-1:
        matchedPrefix[i] = matchedPrefix[i+1]
  return matchedPrefix


def boyer_moore(txt, pat):
  """
  Runs boyer moore with Galil's optimisation. Returns 1-indexed occurrences where pattern matches text
  """
  # edge case
  if len(txt) == 0 or len(pat) == 0:
    return []

  badCharacter = bad_character_table(pat)
  goodSuffix = modified_good_suffix(pat)
  matchedPrefix = matched_prefix(pat)
  res = []

  i = 0   # left side of alignment of pattern to text
  skip = None   # shifting for Galil's optimisation

  while i < len(txt) - len(pat) + 1:
    j = i + len(pat) - 1   # text index
    k = len(pat) - 1   # pattern index

    while k > -1 and txt[j] == pat[k]:
      if skip != None and k == skip[0]+1:
        k = skip[1] - 1
        j = i + k
      else:
        j -= 1
        k -= 1

    # mismatch
    if k > -1:
      mismatch = ord(txt[j]) -32

      # bad character rule
      if badCharacter[mismatch] == None:
        bcShift = k + 1
      else:
        bcShift = k - badCharacter[mismatch][k]

      # good suffix shift
      if goodSuffix[k+1] > 0:
        gsShift = len(pat) - goodSuffix[k+1] - 1
        skip_ = [goodSuffix[k+1], goodSuffix[k+1] - len(pat) + k + 1]

      # matched prefix shift
      else:
        gsShift = len(pat) - matchedPrefix[k+1]
        skip_ = [matchedPrefix[k+1], 0]

      # shift
      i += max(bcShift, gsShift)

      # galil's optimisation
      skip = skip_ if bcShift > bcShift else None

    # complete match
    else:
      res.append(i+1)
      i += len(pat) - matchedPrefix[1]
      skip = [matchedPrefix[1], 0]

  return res


if __name__ == "__main__":
  txt = read_file(sys.argv[1])
  pat = read_file(sys.argv[2])
  # get the number of matches of pattern in text
  matches = boyer_moore(txt, pat)
  write_file(matches)