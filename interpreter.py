def error(message):
  print("Error: %s"%(message))
  quit()

#i'm lazy and don't want to write list(map(...)) all the time
def lmap(f,L):
  return list(map(f,L))

def lfilter(f,L):
  return list(filter(f,L))

#parses .rm file into instructions
def parse(path):
  f = open(path)
  lines = f.readlines()
  lines = lmap(lambda x: tuple((x.strip()).split()), lines)
  lines = lmap(lambda x: removeComment(x), lines)
  return lines

#takes one line of code and returns only the necessary arguments as a tuple
def removeComment(t):
  instr = t[0]
  if instr == "inc":
    return t[:3]
  elif instr == "dec":
    return t[:4]
  elif instr == "halt":
    return t[:1]
  else:
    error("Invalid instruction \"%s\"."%(instr))

#runs a RM program, trace is shown by default
def run(path,trace = True):
  code = parse(path)
  
  #get non-halt instructions
  notHalt = lfilter(lambda x: x[0] != "halt", code)
  registersUsed = list(set(lmap(lambda x: x[1], notHalt)))
  print("Registers used: %s"%(str(registersUsed)))
