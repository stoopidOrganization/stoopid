import time, sys, os, subprocess, json
from sys import exit

# initialize some default variables
configPath = "%userprofile%\\appdata\\roaming\\stoopid"
libs = {}
logging = 0
silent = 0
## list of all the default usable operators and comparators
operators = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "%": lambda x, y: x % y,
    "^": lambda x, y: x**y,
}
comparators = {
    "<<": lambda x, y: x < y,
    ">>": lambda x, y: x > y,
    "<=": lambda x, y: x <= y,
    ">=": lambda x, y: x >= y,
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
}
orderOfOps = [["+", "-"], ["*", "/"], ["%", "^"]]

## saves all used variables
vars = {}
arrs = {}
bools = {}
labels = {}

## line the interpreter is currently on
current_line = 0

# helper functions
def isNumber(num: str) -> bool:
    """Test if given string is a number

    Args:
        num (str): input number

    Returns:
        bool: if given string is number
    """
    try:
        float(num)
        return True
    except ValueError:
        return False

def getType(value):
    global vars,bools,arrs,labels
    if value in vars:
        return "var"
    elif value in bools:
        return "bool"
    elif value in arrs:
        return "arr"
    elif value in labels:
        return "label"
    elif isNumber(value):
        if isFloat(value):
            return "float"
        return "int"
    return "str"

def isFloat(num: str) -> bool:
    """Test if given number is a float

    Args:
        num : number to test

    Returns:
        boolean: if number is a float
    """
    try:
        if float(num) == int(float(num)):
            return False
        else:
            return True
    except ValueError:
        return False


def getNoNum(value: str, lineNum: int) -> str:
    """Test if given input is not a number

    Args:
        value (str) : input string
        lineNum (int): current line

    Returns:
        string: input as not a number
    """
    if isNumber(value):
        print(f"Error in line {lineNum + 1}: String expected, but got number: {value}")
    return value


def getValue(value: str) -> float | int | str | bool:
    """Gets current value of any variable

    Args:
        value (str): variable name

    Returns:
        (float | int | str | bool): value of given variable
    """
    global vars, bools
    value = str(value).strip()

    if isNumber(value):
        return getAsNumtype(value)
    elif value in vars:
        return vars[value]
    elif value in bools:
        return bools[value]

    try:
        return solveEquasion(value)
    except:
        return value


def getLinePieces(line: str) -> list[str]:
    """returns a list of all pieces in the line

    Args:
        line (string): the full line to be split

    Returns:
        (list[str]): list of all pieces in a line
    """
    line.strip()
    if line == "" or line.startswith("#"):
        return [""]
    line = line.split("#")[0]
    linepieces = line.split(":")
    for k in range(len(linepieces)):
        linepieces[k] = linepieces[k].strip()
    return linepieces


def findInString(value: str, arr: list[str]) -> int | str:
    """tests if an element in an array is in the string

    Args:
        value (str): string which should include something
        arr (list[str]): list of values which the string could include

    Returns:
        (str | int): value which is included in the string or -1
    """
    for k in range(len(arr)):
        if arr[k] in value:
            return arr[k]
    return -1


def convertToBool(value: str) -> str | bool:
    """Converts booleans as string to real booleans

    Args:
        value (str): Value to convert to boolean

    Returns:
        (str | bool): the boolean which was given or if it isnt a boolean it just returns the value
    """
    if value in ("True", "False"):
        return {"True": 1, "False": 0}[value]
    else:
        return value


def solveEquasion(equasion: str) -> float:
    """Solves the given equasion

    Args:
        equasion (str): the mathematical equasion to be solved

    Returns:
        float: solved equasion
    """
    global operators, vars, orderOfOps, current_line
    equasion = equasion.replace(" ", "")
    if "(" in equasion:
        start,end,stop=0,0,0
        for k in range(len(equasion)):
            if equasion[k] == "(":
                start = k
        end=1
        for j in range(start+1, len(equasion)):


            if equasion[j] == "(":
                end +=1
            if equasion[j] == ")":
                end -=1
            if end==0 :
                stop=j
                break
        else:
            print("No matching bracket")

        tmpequasion = equasion[:start]
        tmpequasion += str(int(solveEquasion(equasion[start + 1 : stop])))
        tmpequasion += equasion[stop + 1 :]
        return solveEquasion(tmpequasion)
    equasion = str(equasion)
    for i in vars:
        equasion = equasion.replace(i, str(vars[i]))
    ops = []
    values = []

    x = 0
    while x < len(equasion):
        if isNumber(equasion[x]):
            if x > 0 and (
                isNumber(equasion[x - 1])
                or values[len(values) - 1][len(values[len(values) - 1]) - 1]
                in ["-", "."]
            ):
                values[len(values) - 1] += equasion[x]
            else:
                values.append(str(equasion[x]))
        elif equasion[x] in [o for o in operators]:
            if (x == 0 and equasion[x] == "-") or (
                x > 0 and not isNumber(equasion[x - 1])
            ):
                values.append(equasion[x])
            else:
                ops.append(str(equasion[x]))
        elif equasion[x] == ".":
            if x > 0 and isNumber(equasion[x - 1]):
                values[len(values) - 1] += "."
            else:
                values.append("0.")
        x += 1

    # now we have the values and the operators, find the order in which they should be solved
    order = []
    for i in range(len(ops)):
        for k in range(len(orderOfOps)):
            if ops[i] in orderOfOps[k]:
                order.append(k)

    # now we have the order in which the operators should be solved, we need to solve them
    minorder = max(order)
    for i in range(len(ops)):
        if order[i] == minorder:
            values[i] = float(operators[ops[i]](float(values[i]), float(values[i + 1])))
            values.pop(i + 1)
            ops.pop(i)

            order.pop(i)
            break
    # after we have solved the first operator, we need to solve the rest
    if len(ops) > 1:
        # recreate the equation
        equasion = ""
        for i in range(len(ops)):
            equasion += str(values[i]) + str((ops[i]))
        equasion += str(values[-1])
        return getAsNumtype(str((solveEquasion(equasion))))

    elif len(ops) == 1:
        return getAsNumtype(operators[ops[0]](float(values[0]), float(values[1])))
    else:
        return getAsNumtype(values[0])


def findNextBracket(value: str, start: int) -> int:
    """finds the next bracket in a string

    Args:
        value (str): string which should include something
        start (int): index of the bracket whose closing bracket is searched for

    Returns:
        int: index of the next bracket in the string
    """
    count = 1
    for i in range(start + 1, len(value)):
        if value[i] == "(":
            count += 1
        elif value[i] == ")":
            count -= 1
        if count == 0:
            return i

    for i in range(start, len(value)):

        if value[i] == "(":
            return i
    return -1


def setVar(pieces: str) -> bool:
    """Sets the value of a variable without the var keyword

    Args:
        pieces (str): list of all pieces in the line

    Returns:
        bool: if variable was found
    """
    global vars
    piecestmp = pieces.split("=")
    if piecestmp[0].strip() in vars:
        vars[piecestmp[0].strip()] = getValue(piecestmp[1].strip())
        return True
    else:
        return False


def boolSolve(pieces: list[str]) -> bool:
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

            comp = findInString(mop, [c for c in comparators])
            if comp == -1:
                if mop in vars:
                    mop = vars[mop]
                if mop in bools:
                    results.append(getValue(mop))
                elif mop.lower() == "true" or mop == "1":
                    results.append(1)
                elif mop.lower() == "false" or mop == "0":
                    results.append(0)
                else:
                    print(
                        f"Error in line {current_line + 1}: Invalid data type or comparitor not found: {mop}"
                    )
                    exit()
            else:
                var1 = getValue(mop.split(comp)[0])
                var2 = getValue(mop.split(comp)[1])

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


def getAsNumtype(num: str) -> float | int:
    """converts a string to a number and checks if its a float or an int

    Args:
        num (str): number to convert

    Raises:
        Exception: if num isnt a number

    Returns:
        float or int: convertet number
    """
    try:
        num=num.strip()
        if isFloat(num):
            return float(num)
        else:
            return int(num)
    except:
        raise Exception(f"Invalid data type, {num} is not a number")


def getPath(path: str) -> str:
    """resolves the given path

    Args:
        path (string): path as string

    Returns:
        string: resolved path
    """
    try:
        pathlist = path.split("\\")
        for p in range(len(pathlist)):
            if "%" in pathlist[p]:
                pathlist[p] = os.getenv(pathlist[p].replace("%", ""))

        fetchedPath = ""
        for x in pathlist:
            fetchedPath = os.path.join(fetchedPath, x)

        subprocess.run(
            f"mkdir {fetchedPath}",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True,
        )

        return fetchedPath
    except Exception as e:
        print(
            f"Interpreter Error: {e}\nCould not resolve Path {path}\nCrashed in line {e.__traceback__.tb_lineno}"
        )
        exit()


def searchInLib(pieces: list[str]) -> bool:
    """search all libraries for given keyword

    Args:
        pieces (list[str]): list of all pieces in the line

    Returns:
        bool: if keyword was found
    """
    global libs, vars, arrs, bools, labels, silent, operators, comparators, configPath, orderOfOps, current_line
    for l in libs:
        if pieces[0] in libs[l]["keywords"]:
            libs[l]["keywords"][pieces[0]](
                pieces,
                {
                    "vars": vars,
                    "arrs": arrs,
                    "bools": bools,
                    "labels": labels,
                    "logging": logging,
                    "silent": silent,
                    "operators": operators,
                    "comparators": comparators,
                    "configPath": configPath,
                    "orderOfOps": orderOfOps,
                    "current_line": current_line,
                },
            )
            return True
    return False


# keyword functions


def kwVar(pieces: list[str]) -> None:
    """Adds a variable to the list of variables

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    global vars, current_line

    vars[getNoNum(pieces[1], current_line).split("=")[0].strip()] = getValue(
        "".join((pieces[1]).split("=")[1:])
    )


def kwArr(pieces: list[str]) -> None:
    """Adds an array to the list of arrays

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    global arrs
    arrs[getNoNum(pieces[1], current_line)] = [0 for i in range(int(pieces[2]))]


def kwApp(pieces: list[str]) -> None:
    """Appends to an array

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    global arrs
    arrs[getNoNum(pieces[1], current_line)].append(float(getValue(pieces[2])))


def kwGetArr(pieces: list[str]) -> None:
    """Gets the value of an item in an array at a specific index

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    global vars, arrs
    vars[str(pieces[3])] = arrs[str(pieces[1])][getValue(pieces[2])+0.5]


def kwSetArr(pieces: list[str]) -> None:
    """Sets the value of a specific item in an array

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    global arrs
    arrs[str(pieces[1])][getValue(pieces[2])+0.5] = getValue(pieces[3])


def kwOut(pieces: list[str]) -> None:
    """Prints the given input

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    global bools, logging, log
    if pieces[1] in bools:
        out = ["False", "True"][int(bools[pieces[1]])]
    else:
        out = getValue(pieces[1])
    if not silent:
        print(out)
    if logging:
        log.write(str(out) + "\n")


def kwGoTo(pieces: list[str]) -> None:
    """Sets the current line of the interpreter

    Args:
        pieces (list[str]): list of all pieces in the line
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


def kwSleep(pieces: list[str]) -> None:
    """Sleeps the given time

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    time.sleep(float(pieces[1]))


def kwGoIf(pieces: list[str]) -> None:
    """Sets the current line of the interpreter if given condition is true

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    global current_line, labels
    res = boolSolve(pieces[2:])

    if res == 1:
        if pieces[1] in labels:
            current_line = labels[pieces[1]] - 1
            return
        try:
            current_line = int(pieces[1]) - 2
        except:
            print(f"Error in line {current_line + 1}: Label not found {pieces[1]}")
            exit()


def kwIf(pieces: list[str]) -> None:
    """Executes codeblock in curly brackets if condition is true

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    global current_line
    res = boolSolve(pieces[1:])

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


def kwBool(pieces: list[str]) -> None:
    """Creates a boolean

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    global bools
    name = getNoNum(pieces[1], current_line).split("=")[0].strip()
    value = getValue(pieces[1].split("=")[1])

    if value == "True":
        value = 1
    elif value == "False":
        value = 0
    else:
        value = boolSolve(getNoNum(pieces[1], current_line).split("=")[1:])

    bools[name] = value


def kwImport(pieces: list[str]) -> None:
    """Imports a library

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    try:
        global libs, keywords, vars, arrs, bools, labels, logging, silent, operators, comparators, orderOfOps, configPath
        lib = pieces[1]
        path = os.path.join(getPath(configPath), "libs")
        if not path in sys.path:
            sys.path.append(path)

        imp = __import__(lib)
        if lib not in libs:
            libs[lib] = {
                "bin": imp,
                "keywords": {},
            }

            for l in imp.main():
                libs[lib]["keywords"][str(f"{str(lib)}.{str(l)}")] = imp.main()[l]
    except Exception as e:
        print(f"Error in line {current_line + 1}: Library {lib} not found")
        print(e)
        print("interpreter crashed at line: ", e.__traceback__.tb_lineno)
        exit()


def kwEnd(pieces: list[str]) -> None:
    """Ends the programm

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    exit()


def NONE(pieces: list[str]) -> None:
    """Placeholder for keywords that do nothing

    Args:
        pieces (list[str]): list of all pieces in the line
    """
    return


"""
- dictionary for all keywords and their functions
- add a keyword here
- create a function for it called kw<Keyword>
"""
keywords = {
    "var": kwVar,
    "arr": kwArr,
    "app": kwApp,
    "getarr": kwGetArr,
    "setarr": kwSetArr,
    "out": kwOut,
    "goto": kwGoTo,
    "sleep": kwSleep,
    "goif": kwGoIf,
    "if": kwIf,
    "bool": kwBool,
    "import": kwImport,
    "end": kwEnd,
    "}": NONE,
}

# get the system arguments

if "-v" in sys.argv or "--version" in sys.argv:
    for i in range(50):
        print("\n")
    print("  /$$$$$$   /$$                                   /$$       /$$")
    print(" /$$__  $$ | $$                                  |__/      | $$")
    print("| $$  \__//$$$$$$    /$$$$$$   /$$$$$$   /$$$$$$  /$$  /$$$$$$$")
    print("|  $$$$$$|_  $$_/   /$$__  $$ /$$__  $$ /$$__  $$| $$ /$$__  $$")
    print(" \____  $$ | $$    | $$  \ $$| $$  \ $$| $$  \ $$| $$| $$  | $$")
    print(" /$$  \ $$ | $$ /$$| $$  | $$| $$  | $$| $$  | $$| $$| $$  | $$")
    print("|  $$$$$$/ |  $$$$/|  $$$$$$/|  $$$$$$/| $$$$$$$/| $$|  $$$$$$$")
    print(" \______/   \___/   \______/  \______/ | $$____/ |__/ \_______/")
    print("                                       | $$                    ")
    print("                                       | $$                    ")
    print("                                       |__/                    ")
   
    print()
    
    with open("info.json", "r") as f:
        data = json.load(f)
        print(f"\t\tVersion: {data['versionName']}")
        print(f"\t\tNumeric Version: {data['versionNumber']}")
        print(f"\t\tStoopid Version: {data['stoopidStandart']}")
        
    exit()

## get the filename, always the first argument
overwrite = ""  # this is used for debugging purposes only, and should be empty in production. It will force the interpreter to load a specific file, instead of the arguments.
if len(overwrite) == 0:
    try:
        file_name = sys.argv[1]
    except:
        # launch console mode
        print("--- Using stoopid in console mode ---")
        while True:
            linepieces = getLinePieces(str(input(">> ")))
            if not linepieces:
                print("Error: No keyword given")
                continue
            elif linepieces[0] in keywords:
                keywords[linepieces[0].lower()](linepieces)
                linepieces = ""
            elif not searchInLib(linepieces) and not setVar(linepieces[0]):
                print("Error: Unknown keyword")
                continue
else:
    print("Running in Override Mode")
    file_name = overwrite

with open(file_name, "r") as f:
    program_lines = f.readlines()

## prints the output of the stoopid script into a file
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
silent: bool = "--silent" in sys.argv

# main loops

## resolve all lables
for i in range(len(program_lines)):
    try:
        linepieces = getLinePieces(program_lines[i])
        if linepieces[-1] == "label":  # :name:label at the end of the line
            labels[getNoNum(linepieces[-2], i)] = i
    except Exception as e:
        print(f"Error in line {i + 1} while resolving labels:\n{str(e)}")
        print("Interpreter crashed at line: ", e.__traceback__.tb_lineno)
        exit()

## runs the code
while current_line < len(program_lines):
    # get the line
    linepieces = getLinePieces(program_lines[current_line])

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
    elif not searchInLib(linepieces) and not setVar(linepieces[0]):
        print(f"Error in line {current_line + 1}: Unknown keyword: {linepieces[0]}")
        exit()
    current_line += 1
