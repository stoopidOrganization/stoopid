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
keywords = {}

# helper functions

# keyword functions

# main loops