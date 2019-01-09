from diagram import *
from interpreter import setup, lmap, lfilter, error
from copy import deepcopy as copy

def run():
  (code,registers) = setup()
  diagram = Diagram(code)
  
  current = diagram.entry
  memo = {} #dictionary for keeping track of last state seen at given instruction
  
  trace = [] #list for keeping track of instructions since last loop
  # (Instruction object, identifier, target)
  # I: increment
  # D: decrement
  # Z: zero check (register was unable to be decremented)

  #TODO
  style = False
  annPath = ''

  while True:
    if current in memo:
      print("Loop caught!") #TODO
      memo = {} #clear memo table

      instrTrace = lmap(lambda x: x[0],trace)
      loop = trace[instrTrace.index(current):] #from current instruction forward
      
      trace = [] #clear trace list
      
      decd = [] #indices of decremented registers
      for t in loop:
        if t[1] == "D":
          if t[2] not in decd:
            decd.append(t[2]) #add decremented register to list
      
      autoIters = float("inf") #number of safe iterations we can do

      for i in decd: #for each decremented register
        thisReg = lfilter(lambda x: x[2] == i, loop)
        seq = lmap(lambda x: x[1], thisReg) #sequence of things happening to this register

        if "Z" in seq:
          pass
          #TODO
        else:
          lowest = 0
          running = 0
          for c in seq:
            if c == "I":
              running += 1
            else:
              running -= 1
              lowest = min(lowest,running)
          safe = lowest * -1 #smallest value of the register without it getting decremented while 0
          #running is the net change from the loop
          if running < 0:
            safeIters = (registers[i]-safe)//(running*-1)
            autoIters = min(autoIters,safeIters)
      
      if autoIters == float("inf"):
        error("Infinite loop detected")

      if autoIters > 0:
        net = [0] * len(registers) #net change to each register
        for t in loop:
          tgt = t[2]
          if t[1] == "I":
            net[tgt] += 1
          elif t[1] == "D":
            net[tgt] -= 1
        for i in range(len(net)):
          net[i] *= autoIters #net change after all safe iterations

        for i in range(len(registers)):
          registers[i] += net[i]

      display(registers, style, annPath)
      
      if autoIters >= 2:
        print("%i iterations skipped!"%(autoIters))

    else:
      memo[current] = copy(registers) #log current register state
      #execute instruction
      tgt = current.target
      if current.instr == "I":
        registers[tgt] += 1
        display(registers, style, annPath)
        trace.append((current,"I",tgt))
        current = current.goto
      elif current.instr == "D":
        if registers[tgt] == 0:
          trace.append((current,"Z",tgt))
          current = current.zgoto
        else:
          registers[tgt] -= 1
          display(registers, style, annPath)
          trace.append((current,"D",tgt))
          current = current.goto
      else: #halt
        print("~DONE~")
        break

#display current register state, however is appropriate
def display(registers, style, annPath):
  print(registers)

if __name__ == "__main__": #if actually being run
  run()