"""
Lee Zi Yan
31264689
"""

#%%
import sys
import math
import random


# write output to file
def write_file(primes):
  # open file
  with open("output_threeprimes.txt", "w", encoding = "utf-8") as f:
    # write to file if input is not an empty list
    if len(primes) != 0:
      f.write(str(primes[0]) + " " + str(primes[1]) + " " + str(primes[2]))


# modular exponentiation, a^b mod p
def mod_exp(a, b, p):

  # result
  ret = 1

  # while exponent is more than 0
  a = a % p
  while b > 0:
    # If b is odd, multiply a and result
    if b % 2 == 1:
        ret = (ret * a) % p
    b = b>>1
    a = (a * a) % p

  return ret


# Miller-Rabin primality test
def miller_rabin_test(n, k):

  # base case
  if n == 3:
    return True

  # calculate s and t
  s = 0
  t = n-1
  while t % 2 == 0:
    s += 1
    t = t >> 1

  for _ in range(k):
    a = random.randint(2, n-2)

    # if a^(n-1) mod n does not equal to 1
    if mod_exp(a, n-1, n) != 1:
      return False

    # calculate a^t mod n
    prev = mod_exp(a, t, n)

    for _ in range(1, s):

      # repeated squaring
      curr = (prev*prev) % n
      if curr == 1 and prev != 1 and prev != n - 1:
        return False
      prev = curr

  return True


# if step > 0, find closest prime larger than start
# else, closest prime smaller than end
def closest_prime(start, end, step, k):
  for n in range(start, end, step):
    if miller_rabin_test(n, k):
      return n


# sum of three odd prime numbers for n
def three_primes(n):

  # if n is even
  if n % 2 == 0:
    return []

  k = math.ceil(math.log(n))

  x = 3
  y = 3
  z = closest_prime(n-6, 2, -2, k)

  # if True, increase y, else set x = y
  ptr = True
  while y <= z:
    sum = x + y + z

    if sum == n:
      return [x, y, z]

    # if sum if more, decrease z
    elif sum > n:
      z = closest_prime(z-2, 2, -2, k)

    else:
      # increase y
      if ptr:
        y = closest_prime(y+2, z+1, 2, k)
        ptr = False

      # increase x
      else:
        x = y
        ptr = True

  return []


if __name__ == "__main__":
  # get argument n
  n = int(sys.argv[1])

  # output three odd prime numbers that add up to n to a file
  write_file(three_primes(9))