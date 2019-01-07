from diagram import *
from interpreter import setup
from copy import deepcopy as copy

def run():
  (code,registers) = setup()
  diagram = Diagram(code)
  
  current = diagram.entry
  memo = {} #dictionary for keeping track of last state seen at given instruction

  #TODO
  style = False
  annPath = ''

  while True:
    if current in memo:
      print("Loop caught!") #TODO
      input() #ironically, an infinite loop
      #we found a loop!
    else:
      memo[current] = registers #log current register state
      #execute instruction
      tgt = current.target
      if current.instr == "I":
        registers[tgt] += 1
        display(registers, style, annPath)
        current = current.goto
      elif current.instr == "D":
        if registers[tgt] == 0:
          current = current.zgoto
        else:
          registers[tgt] -= 1
          display(registers, style, annPath)
          current = current.goto
      else: #halt
        break
      

#display current register state, however is appropriate
def display(registers, style, annPath):
  print(registers)

if __name__ == "__main__": #if actually being run
  run()
