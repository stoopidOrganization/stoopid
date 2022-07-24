import time, sys

libs=[]
def is_float(number):
    try:
    #check if the number could be represented as an int
        if float(number) == int(number):
            return False
        else:
            return True
    except ValueError:
        return False

def get_value(inp): #checks if the input is a number or a variable
    if isnumber(inp):
        if is_float(inp):
            return float(inp)
        else:
            return int(inp)
    else:
        if inp in vars:
            return vars[inp]
        else:
            return inp

def search_array(string, array):
    for k in range(len(array)):
        if array[k] in string:
            return array[k]
    global i
    print(f"Error in line {i+1}: String search failed. Element {string} not found in array: \n{array}")
    exit()

def isnumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_comparator(line):
    #search for the comparator in the line
    for comparator in comparators:
        if comparator in line:
            return comparator

def get_nonum(num):
    global i
    if isnumber(num):
        print(f"Error in line {i+1}: Cannot use numbers in this context")
    return num

def iscom(comm):
    global linepieces
    return comm==linepieces[0]


overwrite=""#this is used for debugging purposes only, and should be empty in production. It will force the interpreter to load a specific file, instead of the arguments.
if len(overwrite)==0:
    try:
        file_name = sys.argv[1]
    except:
        print("see README.md for usage")
        time.sleep(5)
        exit()
else:
    file_name = overwrite

if "--log" in sys.argv:
    logging=1
    #get the log file name
    try:
        log_file = sys.argv[sys.argv.index("--log")+1]
    except:
        print("please specify filename for log file")
        time.sleep(5)
        exit()
    log=open(log_file, "w")
else:
    logging=0


if "--validate" in sys.argv:
    val=1
else:
    val=0

program=open(file_name,"r")
program_lines=program.readlines()
program.close()
commands=["var","arr","app","getarr","setarr","string","out","goto","sleep","goif","math","end"]
operators=["+","-","*","/","%"]
comparators=["<<",">>","<=",">=", "==","!="]
vars={}
arrs={}
labels={}
i=0
#validate every line (breaks external libraries)
if val:
    for i in range(len(program_lines)):
        lp=program_lines[i].replace(" ","").split(":")
        if len(program_lines[i].replace(" ",""))>1:
            if lp[0] in commands:
                continue
            elif lp[0].startswith("#"):
                continue
            else:
                print(f"Error in line {i+1}: Command not found {lp[0]}")
                exit()
#resolve all lables
i=0
while i<len(program_lines):
    line=program_lines[i]
    if line[0].startswith=="#" or line=="\n":
        i+=1
        continue
    line=line.split("#")[0]
    if line.startswith("string"):
        lstrip=line.replace("\n","")
    else:
        lstrip=line.replace(" ","").replace("\n","")
    linepieces=lstrip.split(":")

    if linepieces[-1]=="label":# :name:label at the end of the line
        labels[get_nonum(linepieces[-2])]=i
    i+=1
i=0

while i<len(program_lines):
    try:
        line=program_lines[i]

        if line[0].startswith=="#" or line=="\n":
            i+=1
            continue
        #cut off the comments
        line=line.split("#")[0]
        if line.startswith("string"):
            lstrip=line.replace("\n","")
        else:
            lstrip=line.replace(" ","").replace("\n","")
        linepieces=lstrip.split(":")

        if iscom("var"): # var : name = value
            vars[get_nonum(linepieces[1]).split("=")[0]]=get_value((linepieces[1]).split("=")[1])
            
        if iscom("arr"): # arr : name : size
            arrs[get_nonum(linepieces[1])]=[0 for i in range(int(linepieces[2]))]

        if iscom("app"): # app : name : value
            arrs[get_nonum(linepieces[1])].append(float(get_value(linepieces[2])))

        if iscom("getarr"): # getarr : name : index : destination
            vars[str(linepieces[3])]=arrs[str(linepieces[1])][get_value(linepieces[2])]

        if iscom("setarr"): # setarr : name : index : value
            arrs[str(linepieces[1])][get_value(linepieces[2])]=get_value(linepieces[3])

        if linepieces[0].strip()=="string": # string : name = value
            vars[str(linepieces[1]).split("=")[0].strip()]=str(linepieces[1]).split("=")[1]
        #strings are weird

        if iscom("out"): #out : name
            out=get_value(linepieces[1])
            print(out)
            if logging:
                log.write(str(out)+"\n")

        if iscom("goto"): #goto : line
            if linepieces[1] in labels:
                i=labels[linepieces[1]]
                continue
            try:
                i=int(linepieces[1])-1
            except:
                print(f"Error in line {i+1}: Label not found {linepieces[1]}")
                exit()
            continue

        if iscom("sleep"):#sleep : time
            time.sleep(float(linepieces[1]))
            
        if iscom("math"):#math : destination : value1 operator value2
            vardest=str(linepieces[1])
            op=search_array(linepieces[2],operators)
            var1=get_value(linepieces[2].split(op)[0])
            var2=get_value(linepieces[2].split(op)[1])
            if op=="+":
                vars[vardest]=var1+var2
            if op=="-":
                vars[vardest]=var1-var2
            if op=="*":
                vars[vardest]=var1*var2
            if op=="/":
                vars[vardest]=var1/var2
            if op=="%":
                vars[vardest]=var1%var2

        if iscom("goif"): #goif : destination : var1  comparator  var2 
            comp=search_array(linepieces[2],comparators)
            var1=get_value(str(linepieces[2]).split(comp)[0])
            var2=get_value(str(linepieces[2]).split(comp)[1])
            if linepieces[1] in labels:
                destination=labels[linepieces[1]]
            else:
                
                destination=get_value(linepieces[1])
                if not isnumber(destination):
                    print(f"Error in line {i+1}: Destination is not a number")
                    exit()
                else:
                    destination=int(destination)-1
            
            if comp=="<<":
                if var1<var2:
                    i=destination
                    continue
            if comp==">>":
                if var1>var2:
                    i=destination
                    continue
            if comp=="<=":
                if var1<=var2:
                    i=destination
                    continue
            if comp==">=":
                if var1>=var2:
                    i=destination
                    continue
            if comp=="==":
                if var1==var2:
                    i=destination
                    continue
            if comp=="!=":
                if var1!=var2:
                    i=destination
                    continue
        
        if iscom("import"):
            #imports a stoopid library which is essentially a python library specifically for the language
            a=__import__(str(linepieces[1]))
            libs.append(a)

        if iscom("end"):
            exit()
        #check for any commands from the librarys
        for lib in libs:
            lib.run(line)
        i+=1

    except Exception as e:
        print("Error at line "+str(i+1)+": "+str(e))
        print("interpreter crashed at line: ", e.__traceback__.tb_lineno)
        break
