from diagram import *
from interpreter import setup, error
from misc import lmap, lfilter
from copy import deepcopy as copy

def run(path = None, regInput = None): #arguments passed through to naive interpreter setup
  (code,registers) = setup(path, regInput)

  diagram = Diagram(code)
  
  current = diagram.entry
  
  trace = [] #list for keeping track of instructions since last loop
  # (Instruction object, identifier, target)
  # I: increment
  # D: decrement
  # Z: zero check (register was unable to be decremented)

  #TODO
  style = False
  annPath = ''

  while True:
    if current in lmap(lambda x: x[0], trace):
      print("Loop caught!") 

      instrTrace = lmap(lambda x: x[0],trace)
      loop = trace[instrTrace.index(current):] #from current instruction forward
      #print("Loop: %s"%(str(loop))) 
      trace = [] #clear trace list
      
      decd = [] #indices of decremented registers
      for t in loop:
        if t[1] == "D" or t[1] == "Z":
          if t[2] not in decd:
            decd.append(t[2]) #add decremented register to list
      
      autoIters = float("inf") #number of safe iterations we can do

      for i in decd: #for each decremented register
        thisReg = lfilter(lambda x: x[2] == i, loop)
        seq = lmap(lambda x: x[1], thisReg) #sequence of things happening to this register
        
        #print("%i: %s"%(i,seq))

        if "Z" in seq:
          running = registers[i]
          for c in seq:
            if c == "I":
              running += 1
            elif c == "D":
              if running == 0:
                autoIters = 0 #already broke behavior
              else:
                running -= 1
            else:
              if running != 0:
                autoIters = 0
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
        
        if autoIters == 0: #whoops, no point
          break
      
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
        return registers

#display current register state, however is appropriate
def display(registers, style, annPath):
  print(registers)

if __name__ == "__main__": #if actually being run
  run()
