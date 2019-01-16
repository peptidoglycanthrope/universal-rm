from interpreter import error, lmap, lfilter
from string import ascii_letters

#TODO: Make sure that you can't just say "macro", "temp", "inc", "dec", or "halt" anywhere else

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

  def __str__(self):
    return "name: %s\nregArgs: %s\nnumRegArgs: %s\ntemp: %s\nlineArgs: %s\nnumLineArgs: %s\ncode:\ndependencies:"%(self.name, self.regArgs, self.numRegArgs, self.temp, self.lineArgs, self.numLineArgs)

  #TODO
  #name: only alphabetical characters allowed
  #regArgs: register arguments in expected order
  #numRegArgs: len(regArgs)
  #temps: names of temporary registers
  #lineArgs: line arguments in expected order
  #numLineArgs: len(lineArgs)
  #code: code with explicit line references converted to labels
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
  
  macros = []
  progress = []
  for line in rmmCode:
    if line[0] == "macro":
      if progress != []:
        macros.append(progress)
      progress = [line]
    else:
      progress.append(line)
  macros.append(progress)
  
  
  #debug
  for m in macros:
    print(Macro(m))
    print()

if __name__ == "__main__": #if actually being run
  run()
