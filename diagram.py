from interpreter import parse, validate, error

class Instruction:
  def __init__(self, instr, target):
    #instr is the name of the instruction, internally abbreviated (str)
    #target is the register being modified, None otherwise (int)
    #we will assume these have been ensured to be valid before creating nodes

    abbr = {"halt": "H", "inc": "I", "dec": "D"}
    self.instr = abbr[instr]

    if self.instr == "H":
      self.target = None
    else:
      self.target = target
    
    self.goto = None
    self.zgoto = None
    self.comeFrom = [] #list of nodes leading to this

  def __repr__(self):
    return self.instr + " " + str(self.target)
  
  def __eq__(self,other): #effectively a redundancy test
    return self.instr == other.instr and self.target == other.target

  #debug
  def printGotos(self):
    print(self)
    print("Goto: %s"%(str(self.goto)))
    print("Zgoto: %s"%(str(self.zgoto)))
    print("ComeFrom: %s"%(str(self.comeFrom)))

  def setTarget(self, target):
    #assume target is valid and is an int
    if self.instr == "H":
      error("Halt instructions have no target.")
    else:
      self.target = target

  def setGoto(self, goto):
    #goto is an instruction node
    if self.instr == "H":
      error("Halt instructions have no goto.")
    else:
      self.goto = goto

  def setZgoto(self, zgoto):
    #zgoto is an instruction node
    if self.instr == "D":
      self.zgoto = zgoto
    else:
      error("Only decrement instructions have a zgoto.")

def makeDiagram(path):
  code = parse(path)
  registers = validate(code)

  #we now know that the code is valid and can start making nodes and connecting them

  lineToNode = {} #keep track of which lines we have made nodes for already
  
  for i in range(len(code)):
    line = code[i] 
    if line[0] == "halt":
      lineToNode[i+1] = Instruction("halt", None)
    else:
      lineToNode[i+1] = Instruction(line[0],line[1])

  for i in range(len(code)):
    this = lineToNode[i+1]
    line = code[i]
    instr = this.instr
    if instr == "I":
      goto = line[2]
      this.goto = lineToNode[goto]
      lineToNode[goto].comeFrom.append(this)
    elif instr == "D":
      goto = line[2]
      this.goto = lineToNode[goto]
      lineToNode[goto].comeFrom.append(this)
      zgoto = line[3]
      this.zgoto = lineToNode[zgoto]
      lineToNode[zgoto].comeFrom.append(this)
  
  for i in range(len(code)):
    lineToNode[i+1].printGotos()
    print()
  
  return lineToNode
