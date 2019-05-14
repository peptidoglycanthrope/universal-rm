from copy import deepcopy as copy
from misc import lmap, lfilter

def error(message):
  print("Error: %s"%(message))
  quit()

#attempts to convert given string to int and quits if it fails
def stringToInt(s):
  try:
    return int(s)
  except:
    error("\"%s\" is not a positive integer."%(s))

#takes a code "tuple" with numbers as strings and converts them to ints
def makeValid(t):
  for i in range(1,len(t)):
      t[i] = stringToInt(t[i])
  return tuple(t)

#parses .rm file into instructions
def parse(path):
  f = open(path)
  lines = f.readlines()
  lines = lmap(lambda x: x.strip().split(), lines)
  lines = lmap(lambda x: removeComment(x), lines)
  lines = lmap(lambda x: makeValid(x), lines)
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

#checks that the RM code is valid, then returns a list of registers
def validate(code):
  #get non-halt instructions
  notHalt = lfilter(lambda x: x[0] != "halt", code)
  registersUsed = list(set(lmap(lambda x: x[1], notHalt)))
  
  numRegisters = max(registersUsed) + 1
  
  if min(registersUsed) < 0:
    error("Register numbers must be non-negative.")
  
  totalLines = len(code)
  linesReferenced = sum(lmap(lambda x: x[2:], code),())
  if min(linesReferenced) <= 0 or max(linesReferenced) > totalLines:
    error("All line numbers must refer to existing lines of code.")
  
  return [0] * numRegisters

#common setup steps, requesting code file and parsing it
def setup():
  path = input("File to be run: ")
  code = parse(path)
 
  registers = validate(code)
  regInput = input("Starting register configuration, comma-separated: ")
  
  if regInput != "":
    regInput = regInput.split(",")
    
    for i in range(len(regInput)):
      regInput[i] = stringToInt(regInput[i])
      if regInput[i] < 0:
        error("A register cannot have a negative value.")
  else:
    regInput = []

  if len(regInput) < len(registers): #more registers than were inputted
    for i in range(len(regInput)):
      registers[i] = regInput[i]
  else:
    registers = regInput
  return (code, registers)

#runs a RM program, trace is shown by default
def run():
  (code, registers) = setup()

  tracePrompt = input("Show trace? (y/n): ")
  trace = (tracePrompt.lower() == "y")

  stylizedPrompt = input("Stylized output? (y/n): ")
  stylized = (stylizedPrompt.lower() == "y")

  hasAnn = False

  if stylized:
    annPath = input("Annotation file path? (blank for no file): ")
    if annPath != "":
      hasAnn = True
      annFile = open(annPath)
      annLines = annFile.readlines()

  if trace: #don't want to go step-by step if there's no trace
    sbsPrompt = input("Step-by-step? (y/n): ")
    sbs = (sbsPrompt.lower() == "y")

  outputPrompt = input("Output to file? (y/n): ")
  output = (outputPrompt.lower() == "y")

  if output:
    outpath = input("File path to output to: ")
    outfile = open(outpath,"w")

  #default labels are R0, R1, ...
  defaultLab = lmap(lambda x: "R" + str(x),range(len(registers)))
  labels = copy(defaultLab)
  comment = ""

  pc = 1
  while True:
    if hasAnn:
      aLine = annLines[pc-1]
      semiSplit = aLine.split(";")
      
      aRegLabels = semiSplit[0]
      comment = semiSplit[1]

      if aRegLabels != "": #empty means do nothing
        if aRegLabels[0] == "&":
          labels = copy(defaultLab)
        else:
          someLabels = aRegLabels.split(",")
          for i in range(len(labels)):
            if someLabels[i] != "":
              labels[i] = someLabels[i]
          
    line = code[pc-1]
    instr = line[0]
    if instr == "inc":
      reg = line[1]
      goto = line[2]
      registers[reg] += 1 #increment register, goto specified line
      pc = goto
    elif instr == "dec":
      reg = line[1]
      goto = line[2]
      zgoto = line[3]
      if registers[reg] == 0:
        pc = zgoto
        continue
      else:
        registers[reg] -= 1
        pc = goto
    else:
      if not trace:
        if stylized:
          print(tableFormat(labels,registers,comment))
        else:
          print(registers) #show final state of registers
      print("~DONE~")
      return
    
    if trace: #show middle steps
      if stylized:
        print(tableFormat(labels,registers,comment))
      else:
        print(registers)
      
      if sbs:
        input()

    if output:
      if stylized:
        outfile.write(tableFormat(labels,registers,comment)+"\n")
      else:
        outfile.write(str(registers)+"\n") 

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

def tableFormat(cLabels, iData, comment):
  columnLabels = copy(cLabels)
  intData = copy(iData) #whoops, aliasing

  if len(columnLabels) != len(intData):
    #this shouldn't actually happen, just a sanity check
    error("Number of column labels does not match amount of data given.")

  for i in range(len(columnLabels)):
    if columnLabels[i][0] == "!":
      columnLabels[i] = columnLabels[i][1:] #remove bang
      intData[i] = displayAsSeq(intData[i])

  data = lmap(lambda x: str(x), intData)
  
  numItems = len(data)
  
  columnWidth = []
  for i in range(numItems):
    columnWidth.append(max(len(columnLabels[i]), len(data[i])) + 2)

  columnFormatted = []
  dataFormatted = []
  for i in range(numItems):
    target = columnWidth[i]
    col = columnLabels[i]
    dat = data[i]
    columnFormatted.append(" " + col + " " * (target - len(col) - 1))
    dataFormatted.append(" " + dat + " " * (target - len(dat) - 1))

  singleMid = ""
  doubleTop = ""
  doubleBot = ""
  for width in columnWidth:
    singleMid += chr(9472) * width
    doubleTop += "═" * width
    doubleBot += "═" * width
    
    singleMid += "┼"
    doubleTop += "╤"
    doubleBot += "╧"

  singleMid = singleMid[:-1] #last character
  doubleTop = doubleTop[:-1]
  doubleBot = doubleBot[:-1]

  topLine = "╔" + doubleTop + "╗"
  columns = "║" + "│".join(columnFormatted) + "║"
  midLine = "╟" + singleMid + "╢ " + comment.strip()
  data    = "║" + "│".join(dataFormatted) + "║"
  bottomLine = "╚" + doubleBot + "╝"
  
  return "\n".join([topLine, columns, midLine, data, bottomLine])

if __name__ == "__main__": #if actually being run
  run()
