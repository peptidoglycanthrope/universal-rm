#miscellaneous functions used in other files

#i'm lazy and don't want to write list(map(...)) all the time
def lmap(f,L):
  return list(map(f,L))

def lfilter(f,L):
  return list(filter(f,L))