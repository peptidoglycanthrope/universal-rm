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
    return (self.instr == other.instr and self.target == other.target
            and self.goto == other.goto and self.zgoto == other.zgoto)
  
  def __hash__(self):
    return id(self)

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

class Diagram:
  def __init__(self, path):
    lineToNode = makeDiagram(path)
    self.entry = lineToNode[1] #first line of code is the entry point

  def writeToFile(self, path):
    nodeToLine = {} #lets us track which nodes have been given a line number
    queue = [self.entry] #which node next to search in DFS
    while queue != []:
      current = queue.pop(0)
      if current not in nodeToLine: #if this node does not have a line number assigned
        numLines = len(nodeToLine) #number of lines already assigned
        nodeToLine[current] = numLines + 1
        if current.instr != "H": #add next things to search into queue
          if current.instr == "D":
            queue = [current.zgoto] + queue
          queue = [current.goto] + queue
    
    outfile = open(path,"w")
    
    lines = [None]*len(nodeToLine)
    for node in nodeToLine:
      lines[nodeToLine[node]-1] = node

    for node in lines:
      if node.instr == "H":
        outfile.write("halt\n")
      elif node.instr == "I":
        gotoNum = nodeToLine[node.goto]
        outfile.write("inc %i %i\n"%(node.target, gotoNum))
      else:
        gotoNum = nodeToLine[node.goto]
        zgotoNum = nodeToLine[node.zgoto]
        outfile.write("dec %i %i %i\n"%(node.target, gotoNum, zgotoNum))

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
  
  #for i in range(len(code)):
    #lineToNode[i+1].printGotos()
    #print()
  
  return lineToNode
