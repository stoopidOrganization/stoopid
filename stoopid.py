import time, sys
from sys import exit

# get the system arguments

## get the filename
## always the first argument
overwrite = "" # this is used for debugging purposes only, and should be empty in production. It will force the interpreter to load a specific file, instead of the arguments.
if len(overwrite) == 0:
    try:
        file_name = sys.argv[1]
    except:
        print("see README.md for usage")
        time.sleep(5)
        exit()
else:
    print("Running in Override Mode")
    file_name = overwrite

with open(file_name, "r") as f:
    program_lines = f.readlines()

## prints the output of the stoopid script into a file
logging = 0
if "--log" in sys.argv:
    logging = 1
    #get the log file name
    try:
        log_file = sys.argv[sys.argv.index("--log")+1]
    except:
        print("please specify filename for log file")
        time.sleep(5)
        exit()
    log = open(log_file, "w")

## disables output completely
silent = "--silent" in sys.argv

# initialize some default variables

## list of all the default usable operators and comparators
operators = {
    "+": lambda x,y : x + y,
    "-": lambda x,y : x - y,
    "*": lambda x,y : x * y,
    "/": lambda x,y : x / y,
    "%": lambda x,y : x % y,
}
comparators = {
    "<<": lambda x,y : x < y,
    ">>": lambda x,y : x > y,
    "<=": lambda x,y : x <= y,
    ">=": lambda x,y : x >= y,
    "==": lambda x,y : x == y,
    "!=": lambda x,y : x != y,
}

## saves all used variables
vars = {}
arrs = {}
bools = {}
labels = {}

## line the interpreter is currently on
current_line = 0

# helper functions
## tests if the given input is a number
def isnumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

## checks if the given number is a float
def is_float(number):
    try:
    # check if the number could be represented as an int
        if float(number) == int(number):
            return False
        else:
            return True
    except ValueError:
        return False

## tests if the given input is not a number
def get_nonum(num, lineNum):
    global current_line
    if isnumber(num):
        print(f"Error in line {lineNum + 1}: String expected, but got number: {num}")
    return num

## gets the current value of any variable
def get_value(inp):
    global vars, bools
    inp=str(inp).strip()

    if isnumber(inp):
        if is_float(inp):
            return float(inp)
        else:
            return int(inp)
    else:
        if inp in vars:
            return vars[inp]
        elif inp in bools:
            if bools[inp]:
                return 1
            elif bools[inp] == 0:
                return 0
        else:
            try:
                return solveMath(inp, vars)
            except:
                return inp

## returns a list of all pieces in the line
def getline(line):
    line.strip()
    if line == "" or line.startswith("'"):
        return ""
    line = line.split("#")[0]
    linepieces = line.split(":")
    for k in range(len(linepieces)):
        linepieces[k] = linepieces[k].strip()
    return linepieces

## idk why this is here
def search_array(string, array):
    for k in range(len(array)):
        if array[k] in string:
            return array[k]
    return -1

## converts "booleans" to booleans
def convertToBool(var):
    if var == "True" or var == "False":
        return {"True":1, "False":0}[var]
    else:
        return var

def solveMath(equasion, vars):
    equasion = str(equasion)
    for i in vars:
        equasion = equasion.replace(i, str(vars[i]))
    allowed = "0123456789*+-/()% "
    if (all(ch in allowed for ch in equasion)):
        return eval(equasion)
    else:
        raise Exception("Invalid Equasion")

## checks bools and resolves them
def boolSolv(pieces):
    global current_line, comparators
    try:
        # get clean linepieces
        for k in range(len(pieces)):
            pieces[k] = pieces[k].replace("{", "").replace("}", "").replace(" ", "")

        cons = 1
        results = []
        combs = []

        # get all conditions to solve
        for k in pieces:
            if k.startswith("or") or k.startswith("and"):
                cons += 1
                combs.append(k)

        # solve all single conditions
        for k in range(cons):
            mop = pieces[k*2+0].replace("{","").replace("}","")
            
            comp = search_array(mop, [c for c in comparators])
            if comp == -1:
                if mop in bools:
                    results.append(get_value(mop))
                elif mop == "True":
                    results.append(1)
                elif mop == "False":
                    results.append(0)
                else:
                    print(f"Error in line {current_line + 1}: Invalid data type or comparitor not found: {mop}")
                    exit()
            else:
                var1 = get_value(mop.split(comp)[0])
                var2 = get_value(mop.split(comp)[1])

                var1 = convertToBool(var1)
                var2 = convertToBool(var2)

                results.append(comparators[comp](var1, var2))

        #solve the whole conditions
        res=results[0]
        for k in range(len(combs)):

            if combs[k].startswith("or"):
                if results[k+1] or res!=0:
                    res=1
                else:
                    res=0
            if combs[k].startswith("and"):
                if res==1 and results[k+1]==1:
                    res=1
                else:
                    res=0

        return res
    except Exception as e:
        print(f"Error in line {current_line + 1}: Boolean error, {e}")
        print("interpreter crashed at line: ", e.__traceback__.tb_lineno)
        exit()
# keyword functions

## function for out keyword
def kwVar(pieces):
    global vars, current_line
    vars[get_nonum(pieces[1], current_line).split("=")[0].strip()] = get_value((pieces[1]).split("=")[1])
    # print(vars)

def kwArr(pieces):
    global arrs
    arrs[get_nonum(pieces[1], current_line)] = [0 for i in range(int(pieces[2]))]

def kwApp(pieces):
    global arrs
    arrs[get_nonum(pieces[1], current_line)].append(float(get_value(pieces[2])))

def kwGetArr(pieces):
    global vars, arrs
    vars[str(pieces[3])] = arrs[str(pieces[1])][get_value(pieces[2])]

def kwSetArr(pieces):
    global arrs
    arrs[str(pieces[1])][get_value(pieces[2])] = get_value(pieces[3])

def kwOut(pieces):
    global bools, logging, log
    if pieces[1] in bools:
        out = ["False","True"][int(bools[pieces[1]])]
    else:
        out = get_value(pieces[1])
    if not silent:
        print(out)
    if logging:
        log.write(str(out)+"\n")

def kwGoTo(pieces):
    global labels, current_line
    if pieces[1] in labels:
        current_line = labels[pieces[1]] - 1
        return
    try:
        current_line = int(pieces[1]) - 2
    except:
        print(f"Error in line {current_line + 1}: Label not found {pieces[1]}")
        exit()

def kwSleep(pieces):
    time.sleep(float(pieces[1]))

# def kwMath(pieces):
#     global operators, vars
#     lp = []
#     for k in pieces:
#         lp.append(k.replace(" ", ""))
#     vardest = str(lp[1])
#     op = search_array(lp[2], [o for o in operators])
#     var1 = get_value(lp[2].split(op)[0])
#     var2 = get_value(lp[2].split(op)[1])
#     vars[vardest] = operators[op](var1, var2)

def kwMath(pieces):
    global vars
    vars[str(pieces[1])] = get_value(pieces[2])
def kwGoIf(pieces):
    global current_line, labels
    res = boolSolv(pieces[2:])

    if res == 1:
        if pieces[1] in labels:
            current_line = labels[pieces[1]] - 1
            return
        try:
            current_line = int(pieces[1]) - 2
        except:
            print(f"Error in line {current_line + 1}: Label not found {pieces[1]}")
            exit()

def kwIf(pieces):
    global current_line
    res = boolSolv(pieces[1:])

    if not res:
        brackets = 1
        while not brackets == 0:
            current_line += 1
            if "}" in program_lines[current_line]:
                brackets -= 1
            if "{" in program_lines[current_line]:
                brackets += 1
            if brackets < 0:
                print(f"Error in line {current_line + 1}: Unmatched brackets")
                exit()

def kwBool(pieces):
    global bools
    name = get_nonum(pieces[1], current_line).split("=")[0].strip()
    value = get_value(pieces[1].split("=")[1])

    if value == "True":
        value = 1
    elif value == "False":
        value = 0
    else:
        value = boolSolv(get_nonum(pieces[1], current_line).split("=")[1:])

    bools[name] = value

def kwEnd(pieces):
    exit()

def NONE(pieces):
    return

################
# dictionary for all keywords and their functions
# add a keyword here
# create a function for it called kw<Keyword>
################
keywords = {
    'var' : kwVar,
    'arr' : kwArr,
    'app' : kwApp,
    'getarr' : kwGetArr,
    'setarr' : kwSetArr,
    'out' : kwOut,
    'goto' : kwGoTo,
    'sleep' : kwSleep,
    'math'  : kwMath,
    'goif' : kwGoIf,
    'if' : kwIf,
    'bool' : kwBool,
    'end' : kwEnd,
    '}' : NONE,
}

# main loops

## resolve all lables
for i in range(len(program_lines)):
    try:
        linepieces = getline(program_lines[i])

        if linepieces[-1] == "label":# :name:label at the end of the line
            labels[get_nonum(linepieces[-2], i)] = i
    except Exception as e:
        print(f"Error in line {i + 1} while resolving labels:\n{str(e)}")
        exit()

## runs the code
while current_line < len(program_lines):
    # get the line
    linepieces = getline(program_lines[current_line])
    
    if linepieces[0] == "":
        current_line += 1
        continue
    
    # run the code
    if linepieces[0] in keywords:
        try:
            keywords[linepieces[0].lower()](linepieces)
        except Exception as e:
            print(f"Error in line {current_line + 1}:\n{str(e)}")
            print("interpreter crashed at line: ", e.__traceback__.tb_lineno)
            exit()
    else:
        print(f"Error in line {current_line + 1}: Unknown keyword: {linepieces[0]}")
        exit()
    current_line += 1
