"""
Lee Zi Yan
31264689
"""

import sys

def read_file(filename):
  # read string from file
  with open(filename, "r", encoding="utf-8") as f:
    s = f.read()
  f.close()
  return s


def write_file(occ):
  # write output to file
  with open("output_hd1_patmatch.txt", "w", encoding="utf-8") as f:
    # print from back to front, so occurences are in ascending order
    for i in range(len(occ)):
      output = str(occ[i][0]) + " " + str(occ[i][1]) + "\n"
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


def hd_patmatch(txt, pat):
  # 2 array implementation
  # Find occurrences of pattern that matches text within a Hamming distance <= 1
  matches = []

  if len(txt) == 0 or len(pat) == 0:
    return matches

  if len(pat) == 1:
    for i in range(len(txt)):
      if txt[i] == pat:
        matches.append((i+1, 0))
      else:
        matches.append((i+1, 1))
    return matches

  n, m = len(txt), len(pat)
  zArr = z_algo(pat + txt)
  zSuf = z_suffix(txt + pat)

  for i in range(m, n+1):
    hd = zArr[i] + zSuf[i-1]
    if hd == m-1:
      matches += [(i-m+1, 1)]
    elif hd >= m:
      matches += [(i-m+1, 0)]

  return matches


if __name__ == "__main__":
  txt = read_file(sys.argv[1])
  pat = read_file(sys.argv[2])
  occ = hd_patmatch(txt, pat)
  write_file(occ)