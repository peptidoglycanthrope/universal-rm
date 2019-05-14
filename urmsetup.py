from interpreter import setup
from misc import listToSeq, displayAsSeq
from smart_interp import run as runSmart

def run():
    (code, registers) = setup()
    codenums = []

    for line in code:
        instr = line[0]
        if instr == "inc":
            codenums += [0, line[1], line[2], 0] #inc is 0
        elif instr == "dec":
            codenums += [1, line[1], line[2], line[3]] #dec is 1
        else:
            codenums += [2, 0, 0, 0] #halt is 2
    
    print(codenums)

    codeSeq = listToSeq(codenums[4:])
    regSeq = listToSeq(registers[1:])

    ''' in order:
            code before current line
            current instr
            current target register
            current goto
            current zgoto
            code after current line
            registers to left of current
            current register
            registers to right of current
            program counter (line no)
            register number
    '''

    start = [0,codenums[0],codenums[1],codenums[2],codenums[3],codeSeq,0,registers[0],regSeq,1,0]

    regInput = str(start)[1:-1]

    print("Initial register state: %s\n Press Enter to begin:" %(regInput))
    input()

    end = runSmart("urm.rm", regInput)

    simEnd = displayAsSeq(end[8])
    print("Final simulated register state: %s" %(str(simEnd)))

if __name__ == "__main__": #if actually being run
  run()