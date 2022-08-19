import time, sys, json, os
from sys import exit

# get the system arguments

## get the filename
## always the first argument
overwrite = ""  # this is used for debugging purposes only, and should be empty in production. It will force the interpreter to load a specific file, instead of the arguments.
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
    # get the log file name
    try:
        log_file = sys.argv[sys.argv.index("--log") + 1]
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
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "%": lambda x, y: x % y,
}
comparators = {
    "<<": lambda x, y: x < y,
    ">>": lambda x, y: x > y,
    "<=": lambda x, y: x <= y,
    ">=": lambda x, y: x >= y,
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
}

## saves all used variables
vars = {}
arrs = {}
bools = {}
labels = {}

## line the interpreter is currently on
current_line = 0

# helper functions
def isnumber(string):
    """Test if given string is a number

    Args:
        string (string): input string

    Returns:
        boolean: if given string is number
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_float(number):
    """Test if given number is a float

    Args:
        number : number to test

    Returns:
        boolean: if number is a float
    """
    try:
        if float(number) == int(number):
            return False
        else:
            return True
    except ValueError:
        return False


def get_nonum(inp, lineNum):
    """Test if given input is not a number

    Args:
        inp : input string
        lineNum (int): current line

    Returns:
        string: input as not a number
    """
    global current_line
    if isnumber(inp):
        print(f"Error in line {lineNum + 1}: String expected, but got number: {inp}")
    return inp


def get_value(inp):
    """Gets current value of any variable

    Args:
        inp (string): variable name

    Returns:
        any: value of given variable
    """
    global vars, bools
    inp = str(inp).strip()

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
                return solveMath(inp)
            except:
                return inp


def getline(line):
    """returns a list of all pieces in the line

    Args:
        line (string): the full line to be split

    Returns:
        string list: list of all pieces in a line
    """
    line.strip()
    if line == "" or line.startswith("'"):
        return ""
    line = line.split("#")[0]
    linepieces = line.split(":")
    for k in range(len(linepieces)):
        linepieces[k] = linepieces[k].strip()
    return linepieces


def search_array(string, array):
    """tests if an element in an array is in the string

    Args:
        string (string): string which should include something
        array (string array): list of values which the string could include

    Returns:
        string or int: value which is included in the string or -1
    """
    for k in range(len(array)):
        if array[k] in string:
            return array[k]
    return -1


def convertToBool(val):
    """Converts booleans as string to real booleans

    Args:
        val (string): Value to convert to boolean

    Returns:
        string or bool: the boolean which was given or if it isnt a boolean it just returns the value
    """
    if val == "True" or val == "False":
        return {"True": 1, "False": 0}[val]
    else:
        return val


def solveMath(equasion):
    """Solves an equasion

    Args:
        equasion (string): equasion to solve

    Raises:
        Exception: Invalid Equasion

    Returns:
        string: solved equasion
    """
    global vars
    equasion = str(equasion)
    for i in vars:
        equasion = equasion.replace(i, str(vars[i]))
    allowed = "0123456789*+-/()% "
    if all(ch in allowed for ch in equasion):
        return eval(equasion)
    else:
        raise Exception("Invalid Equasion")


def boolSolv(pieces):
    """checks bools and resolves them

    Args:
        pieces (string array): Pieces of current lines

    Returns:
        boolean: returns the solved condition
    """
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
            mop = pieces[k * 2 + 0].replace("{", "").replace("}", "")

            comp = search_array(mop, [c for c in comparators])
            if comp == -1:
                if mop in bools:
                    results.append(get_value(mop))
                elif mop == "True" or mop == "1":
                    results.append(1)
                elif mop == "False" or mop == "0":
                    results.append(0)
                else:
                    print(
                        f"Error in line {current_line + 1}: Invalid data type or comparitor not found: {mop}"
                    )
                    exit()
            else:
                var1 = get_value(mop.split(comp)[0])
                var2 = get_value(mop.split(comp)[1])

                var1 = convertToBool(var1)
                var2 = convertToBool(var2)

                results.append(comparators[comp](var1, var2))

        # solve the whole conditions
        res = results[0]
        for k in range(len(combs)):

            if combs[k].startswith("or"):
                if results[k + 1] or res != 0:
                    res = 1
                else:
                    res = 0
            if combs[k].startswith("and"):
                if res == 1 and results[k + 1] == 1:
                    res = 1
                else:
                    res = 0

        return res
    except Exception as e:
        print(f"Error in line {current_line + 1}: Boolean error, {e}")
        print("interpreter crashed at line: ", e.__traceback__.tb_lineno)
        exit()

def getPath(path):
    try:
        pathlist = path.replace("%", "").split("\\")

        for p in range(len(pathlist)):
            if os.getenv(pathlist[p]) != None:
                pathlist[p] = os.getenv(pathlist[p])

        fetchedPath = os.path.join(pathlist[0])
        p = 1
        while p < len(pathlist):
            fetchedPath = os.path.join(fetchedPath, pathlist[p])
            p += 1

        return fetchedPath
    except Exception as e:
        print(f"Interpreter Error: {e}\nCould not resolve Path {path}\nCrashed in line {e.__traceback__.tb_lineno}")
        exit()

# keyword functions


def kwVar(pieces):
    """Adds a variable to the list of variables

    Args:
        pieces (String List): list of all pieces in the line
    """
    global vars, current_line

    vars[get_nonum(pieces[1], current_line).split("=")[0].strip()] = get_value(
        "".join((pieces[1]).split("=")[1:])
    )
    # print(vars)


def kwArr(pieces):
    """Adds an array to the list of arrays

    Args:
        pieces (String List): list of all pieces in the line
    """
    global arrs
    arrs[get_nonum(pieces[1], current_line)] = [0 for i in range(int(pieces[2]))]


def kwApp(pieces):
    """Appends to an array

    Args:
        pieces (String List): list of all pieces in the line
    """
    global arrs
    arrs[get_nonum(pieces[1], current_line)].append(float(get_value(pieces[2])))


def kwGetArr(pieces):
    """Gets the value of an item in an array at a specific index

    Args:
        pieces (String List): list of all pieces in the line
    """
    global vars, arrs
    vars[str(pieces[3])] = arrs[str(pieces[1])][get_value(pieces[2])]


def kwSetArr(pieces):
    """Sets the value of a specific item in an array

    Args:
        pieces (String List): list of all pieces in the line
    """
    global arrs
    arrs[str(pieces[1])][get_value(pieces[2])] = get_value(pieces[3])


def kwOut(pieces):
    """Prints the given input

    Args:
        pieces (String List): list of all pieces in the line
    """
    global bools, logging, log
    if pieces[1] in bools:
        out = ["False", "True"][int(bools[pieces[1]])]
    else:
        out = get_value(pieces[1])
    if not silent:
        print(out)
    if logging:
        log.write(str(out) + "\n")


def kwGoTo(pieces):
    """Sets the current line of the interpreter

    Args:
        pieces (String List): list of all pieces in the line
    """
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
    """Sleeps the given time

    Args:
        pieces (String List): list of all pieces in the line
    """
    time.sleep(float(pieces[1]))


def kwMath(pieces):
    global vars
    vars[str(pieces[1])] = get_value(pieces[2])


def kwGoIf(pieces):
    """Sets the current line of the interpreter if given condition is true

    Args:
        pieces (String List): list of all pieces in the line
    """
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
    """Executes codeblock in curly brackets if condition is true

    Args:
        pieces (String List): list of all pieces in the line
    """
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
    """Creates a boolean

    Args:
        pieces (String List): list of all pieces in the line
    """
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

def kwImport(pieces):
    with open("config.json", "r") as f:
        config = json.load(f)
        newPath = getPath(config["path"])
            
        print(newPath)
        

def kwEnd(pieces):
    """Ends the programm

    Args:
        pieces (String List): list of all pieces in the line
    """
    exit()


def NONE(pieces):
    """Placeholder for keywords that do nothing

    Args:
        pieces (String List): list of all pieces in the line
    """
    return


################
# dictionary for all keywords and their functions
# add a keyword here
# create a function for it called kw<Keyword>
################
keywords = {
    "var": kwVar,
    "arr": kwArr,
    "app": kwApp,
    "getarr": kwGetArr,
    "setarr": kwSetArr,
    "out": kwOut,
    "goto": kwGoTo,
    "sleep": kwSleep,
    "math": kwMath,
    "goif": kwGoIf,
    "if": kwIf,
    "bool": kwBool,
    "import": kwImport,
    "end": kwEnd,
    "}": NONE,
}

# main loops

## resolve all lables
for i in range(len(program_lines)):
    try:
        linepieces = getline(program_lines[i])

        if linepieces[-1] == "label":  # :name:label at the end of the line
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
