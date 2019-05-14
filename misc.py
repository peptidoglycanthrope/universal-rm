#miscellaneous functions used in other files

#i'm lazy and don't want to write list(map(...)) all the time
def lmap(f,L):
  return list(map(f,L))

def lfilter(f,L):
  return list(filter(f,L))

#takes list of ints, puts them in sequence encoding
def listToSeq(L):
  L = L[::-1]
  result = 0
  for n in L:
    result = result * 3 + 2 #place an "2" to mark end of number
    while n > 0:
      result *= 3
      result += n % 2
      n //= 2 #take a base 2 digit from n, put in seq encoding
  return result

def displayAsSeq(n):
  seq = []
  current = 0 #keeps track of current number being read
  while n > 0:
    digit = n % 3
    n //= 3
    if digit == 2:
      seq = [current] + seq
      current = 0
    else:
      current = current*2 + digit #"append" to current
  return str(seq[::-1])