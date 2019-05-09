from interpreter import error, lmap, lfilter
from string import ascii_letters

#TODO: Make sure that you can't just say "macro", "temp", "inc", "dec", or "halt" anywhere else
#TODO: Make sure macro names are unique?

protected = ["macro", "temp", "inc", "dec", "halt"]

class Macro:
  def error(self,string):
    #for some reason, your __init__ might go awry
    error(string)
  def __init__(self, macro):
    #macro is a list of lines including a "macro" line, optional "temp" line, and code
    lineMacro = macro[0]
    
    if lineMacro[0] != "macro":
      self.error("First instruction must be \"macro\".")
    name = lineMacro[1]
    if name == "":
      self.error("Macro name cannot be empty.")
    if name in protected:
      self.error("Macro name \"%s\" is a protected keyword.")
    for c in name:
      if c not in ascii_letters:
        self.error("Macro name \"%s\" is invalid; it must only contain alphabetical characters."%(name))
    self.name = name #name is valid and has been recorded

    if ":" not in lineMacro:
      self.error("Macro \"%s\" missing \":\" to separate name and register arguments"%(self.name))
    if "|" not in lineMacro:
      self.error("Macro \"%s\" missing \"|\" to separate register and line arguments"%(self.name))
    if "#" not in lineMacro:
      self.error("Macro \"%s\" missing \"#\" to separate arguments from mandatory comment (I'm sorry)."%(self.name))


    indColon = lineMacro.index(":")
    indPipe = lineMacro.index("|")
    indHash = lineMacro.index("#")
  
    regArgs = lineMacro[indColon+1:indPipe]
    if len(list(set(regArgs))) != len(regArgs):
      self.error("Macro \"%s\" must not have duplicate register argument names."%(self.name))
    self.regArgs = regArgs
    self.numRegArgs = len(self.regArgs)

    lineArgs = lineMacro[indPipe+1:indHash]
    if len(list(set(lineArgs))) != len(lineArgs):
      self.error("Macro \"%s\" must not have duplicate line argument names."%(self.name))
    self.lineArgs = lineArgs
    self.numLineArgs = len(self.lineArgs)
  
    temps = []
    if macro[1][0] == "temp":
      lineTemp = macro[1]
      for t in lineTemp[1:]:
        for c in t:
          if c not in ascii_letters:
            self.error("Temp register names in macro \"%s\" must be made only of alphabetical characters."%(self.name))
      temps = lineTemp[1:] #we now know that all temp registers are alphabetical-only
    self.temp = temps

    #finding dependencies
    self.dependencies = []
    self.code = []

    for line in macro:
      if line[0] not in protected: #not a macro or temp line
        #first token in the line is a line number, ignore it
        trimline = line[1:]
        self.code.append(trimline)
        if trimline[0] not in protected: #is actual instruction a macro?
          self.dependencies.append(trimline[0])
    

  def __str__(self):
    return "name: %s\nregArgs: %s\nnumRegArgs: %s\ntemp: %s\nlineArgs: %s\nnumLineArgs: %s\ncode: %s\ndependencies: %s"%(self.name, self.regArgs, self.numRegArgs, self.temp, self.lineArgs, self.numLineArgs, self.code, self.dependencies)

  #TODO
  #name: only alphabetical characters allowed
  #regArgs: register arguments in expected order
  #numRegArgs: len(regArgs)
  #temp: names of temporary registers
  #lineArgs: line arguments in expected order
  #numLineArgs: len(lineArgs)
  #code: code with explicit line references converted to labels, otherwise not validated
  #dependencies: macros that are referenced in the code

def run():
  fileName = input(".rmm file path to compile: ")
  if fileName.split(".")[-1] != "rmm":
    error("File must be a .rmm (register machine macro) file.")
  f = open(fileName)
  lines = f.readlines()
  
  lines = lmap(lambda x: x.strip(), lines) #remove newline
  lines = lfilter(lambda x: x != "", lines) #remove empty lines

  hasMacros = False
  if "MACROS" in lines:
    hasMacros = True
  
  if not hasMacros:
    pass #defer to the original interpreter
  
  if "MACROS" not in lines:
    error("\"MACROS\" divider must be in code before macros.")

  macroDiv = lines.index("MACROS") #line that divides rm from rmm code
  rmCode = lines[:macroDiv]
  rmmCode = lines[macroDiv+1:]

  rmmCode = lmap(lambda x: x.split(" "), rmmCode) #split into tokens
  
  macros = [] #list of all code snippets to convert into macros
  progress = []
  for line in rmmCode:
    if line[0] == "macro":
      if progress != []:
        macros.append(progress) #read until the next "macro" token, then add to list
      progress = [line]
    else:
      progress.append(line)
  macros.append(progress) 
  
  macroDict = {}

  for m in macros: #add all the macros to a dictionary for easy lookup
    mac = Macro(m)
    macroDict[mac.name] = mac
	
  #debug
  for m in macroDict:
    print(str(macroDict[m]) + "\n")

if __name__ == "__main__": #if actually being run
  run()
