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
operators = ["+","-","*","/","%"]
comparators = ["<<",">>","<=",">=", "==","!="]

## saves all used variables
vars = {}
arrs = {}
bools = {}
labels = {}

## line the interpreter is currently on
current_line = 0

################
# dictionary for all keywords and their functions
# add a keyword here
# create a function for it called kw<Keyword>
################
keywords = {
    "out" : "kwOut",
}

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

# keyword functions

## function for out keyword
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

# main loops

## resolve all lables
for i in range(len(program_lines)):
    try:
        line = program_lines[i]
        if line[0].startswith == "#" or line == "\n":
            continue
        line = line.split("#")[0]
        if line.startswith("string"):
            lstrip = line.replace("\n","")
        else:
            lstrip = line.replace(" ","").replace("\t","").replace("\n","")
        linepieces = lstrip.split(":")

        if linepieces[-1] == "label":# :name:label at the end of the line
            labels[get_nonum(linepieces[-2], i)] = i
    except Exception as e:
        print(f"Error in line {i + 1} while resolving labels:\n{str(e)}")
        exit()

## runs the code
while current_line < len(program_lines):
    # get the line
    line = program_lines[i]

    linepieces = getline(line)

    # run the code
    if linepieces[0] in keywords:
        try:
            keywords[linepieces[0]](linepieces)
        except Exception as e:
            print(f"Error in line {current_line + 1}:\n{str(e)}")
            exit()
    else:
        print(f"Error in line {current_line + 1}: Unknown keyword: {linepieces[0]}")
        exit()
