import time, sys

overwrite="" #this is used for debugging purposes only, and should be empty in production. It will force the interpreter to load a specific file, instead of the arguments.

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
        elif inp in bools:
            if bools[inp]:
                return 1
            elif bools[inp]==0:
                return 0
        else:
            return inp

def search_array(string, array):
    for k in range(len(array)):
        if array[k] in string:
            return array[k]
    global i
    print(f"Error in line {i+1}: String search failed. Element {string} not found in array: \n{array}")
    print("Keep in mind, that handeling booleans is currently partly disabled due to a bug, which will cause this message to appear.")
    print("If you want to force full boolean support, then add the --forcebool argument. This might cause issues with or & and statements.")
    exit()

def isnumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

    
def get_nonum(num):
    global i
    if isnumber(num):
        print(f"Error in line {i+1}: String expected, but got number: {num}")
    return num

def iscom(comm, linepieces):
    return comm == linepieces[0]

def convertToBool(var):
    if var == "True" or var == "False":
        return {"True":1, "False":0}[var]
    else:
        return var

def boolSolv(linepieces): #checks bools and resolves them
    try:
        for k in range(len(linepieces)):
            linepieces[k] = linepieces[k].replace("{", "").replace("}", "")
        #check if and how many conditions we have
        #figure out how many conditions we have
        if linepieces[0] in bools and forcebool:
            for bool in bools:
                if bool == linepieces[0]:
                    return bools[bool]#nils, you cant just return the first bool you find, pls fix this

        if linepieces[0] == "True":
            return 1
        elif linepieces[0] == "False":
            return 0
        #again, you need to check for ors and ands and comparisons.
        else:
            cons=1
            results=[]
            combs=[]
            for k in linepieces:
                if k.startswith("or") or k.startswith("and"):
                    cons+=1
                    combs.append(k)
            for k in range(cons):
                mop=linepieces[k*2+0].replace("{","").replace("}","")
                
                comp=search_array(mop,comparators)
                var1=get_value(mop.split(comp)[0])
                var2=get_value(mop.split(comp)[1])
                
                var1 = convertToBool(var1)
                var2 = convertToBool(var2)
                if comp=="==":
                    results.append(var1==var2)
                if comp=="!=":
                    results.append(var1!=var2)
                if comp=="<=":
                    results.append(var1<=var2)
                if comp==">=":
                    results.append(var1>=var2)
                if comp=="<<":
                    results.append(var1<var2)
                if comp==">>":
                    results.append(var1>var2)

            #solve the conditions
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
        print(f"Error in line {i+1}: Boolean error, {e}")
        print("interpreter crashed at line: ", e.__traceback__.tb_lineno)
        exit()
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


if "--forcebool" in sys.argv:
    forcebool=1
else:
    forcebool=0

with open(file_name, "r") as f:
    program_lines = f.readlines()

commands=["var","arr","app","getarr","setarr","string","out","goto","sleep","goif","math","end"]
operators=["+","-","*","/","%"]
comparators=["<<",">>","<=",">=", "==","!="]
vars={}
arrs={}
bools = {}
labels={}
i=0
interpreter = True
brackets = 0

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
        lstrip=line.replace(" ","").replace("\t","").replace("\n","")
    linepieces=lstrip.split(":")

    if linepieces[-1]=="label":# :name:label at the end of the line
        labels[get_nonum(linepieces[-2])]=i
    i+=1
i=0

def analyzeLine(line, linepieces):
    try:
        global i ,libs, vars, arrs, labels, interpreter, commands, operators, comparators, program_lines, brackets

        if iscom("var", linepieces): # var : name = value
            vars[get_nonum(linepieces[1]).split("=")[0]]=get_value((linepieces[1]).split("=")[1])

        elif iscom("arr", linepieces): # arr : name : size
            arrs[get_nonum(linepieces[1])]=[0 for i in range(int(linepieces[2]))]

        elif iscom("app", linepieces): # app : name : value
            arrs[get_nonum(linepieces[1])].append(float(get_value(linepieces[2])))

        elif iscom("getarr", linepieces): # getarr : name : index : destination
            vars[str(linepieces[3])]=arrs[str(linepieces[1])][get_value(linepieces[2])]

        elif iscom("setarr", linepieces): # setarr : name : index : value
            arrs[str(linepieces[1])][get_value(linepieces[2])]=get_value(linepieces[3])

        elif linepieces[0].strip()=="string": # string : name = value
            vars[str(linepieces[1]).split("=")[0].strip()]=str(linepieces[1]).split("=")[1]
        #strings are weird

        elif iscom("out", linepieces): #out : name
            if linepieces[1] in bools:
                out = ["False","True"][int(bools[linepieces[1]])]
            else:
                out = get_value(linepieces[1])
            print(out)
            if logging:
                log.write(str(out)+"\n")

        elif iscom("goto", linepieces): #goto : line
            if linepieces[1] in labels:
                i = labels[linepieces[1]]
                return
            try:
                i = int(linepieces[1])-1
            except:
                print(f"Error in line {i + 1}: Label not found {linepieces[1]}")
                exit()
            return

        elif iscom("sleep", linepieces):#sleep : time
            time.sleep(float(linepieces[1]))

        elif iscom("math", linepieces): #math : destination : value1 operator value2
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

        elif iscom("goif",linepieces): #goif : destination : var1  comparator  var2 (: or : var3 comparitor var4)
            res = boolSolv(linepieces[2:])

            if res==1:
                if linepieces[1] in labels:
                    i=labels[linepieces[1]]
                    return
                try:
                    i=int(linepieces[1])-1
                except:
                    print(f"Error in line {i+1}: Label not found {linepieces[1]}")
                    exit()
                return

        elif iscom("import", linepieces):
            #imports a stoopid library which is essentially a python library specifically for the language
            try:
                a=__import__(str(linepieces[1])) #set the name of the library to after the path
                libs.append(a)
                #print(libs)
            except:
                print(f"Error in line {i+1}: Library not found {linepieces[1]}")
                exit()

        elif iscom("if", linepieces): # if : var1 comparator var2 : {
            res = boolSolv(linepieces[1:])

            if not res:
                brackets=1
                while not brackets==0:
                    i+=1
                    if "}" in program_lines[i]:
                        brackets-=1
                    if "{" in program_lines[i]:
                        brackets+=1
                    if brackets<0:
                        print(f"Error in line {i+1}: Unmatched brackets")
                        exit()

                return

        elif iscom("bool", linepieces):
            name = get_nonum(linepieces[1]).split("=")[0]
            value = get_value(linepieces[1].split("=")[1])

            if value == "True":
                value = 1
            elif value == "False":
                value = 0
            else:
                value = boolSolv(get_nonum(linepieces[1]).split("=")[1:])

            bools[name] = value

        elif iscom("end", linepieces):
            exit()
        
        else:
            #check for any commands from the librarys
            for lib in libs:
                vars=lib.run(line,vars)
        
        i += 1

        return
    except Exception as e:
        print("Error at line "+str(i+1)+": "+str(e))
        print("interpreter crashed at line: ", e.__traceback__.tb_lineno)
        exit()

# main loop
while i < len(program_lines):

    try:
        # get the line
        line = program_lines[i]

        # cut off the comments
        line = line.split("#")[0]
        if line.startswith("string"):
            lstrip=line.replace("\n","")
        else:
            lstrip = line.replace(" ","").replace("\n","")
        
        # make an array of the line pieces
        linepieces = lstrip.split(":")
        analyzeLine(line, linepieces)
      
    except Exception as e:
        print("Critical error: " + str(e))
        exit()
