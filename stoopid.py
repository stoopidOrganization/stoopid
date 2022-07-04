import time, sys
operators=["+","-","*","/","%"]
comparators=["<",">","<=",">=", "==","!="]
#get the file name which is the first argument
try:
    file_name = sys.argv[1]
except:
    file_name= "fallback.stpd"
program=open(file_name,"r")
program_lines=program.readlines()
program.close()
funcs=["var","out","goto","string","math",]
vars={}
arrs={}
labels={}
def is_float(number):
    try:
    #check if the number could be represented as an int
        if float(number) == int(number):
            return False
        else:
            return True
    except ValueError:
        return False
def get_operator(line):
    #search for the operator in the line
    for operator in operators:
        if operator in line:
            return operator
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
def getafterequals(line):
    return line.split("=")[1]
i=0
while i<len(program_lines):
    line=program_lines[i]
    #print(line)
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

    if linepieces[0]=="var": # var : name = value
        vars[str(linepieces[1]).split("=")[0]]=float(str(linepieces[1]).split("=")[1])
    if linepieces[0]=="arr": # arr : name : size
        arrs[str(linepieces[1]).split("=")[0]]=[]
    if linepieces[0]=="app": # app : name : value
        arrs[str(linepieces[1]).split("=")[0]].append(float(str(linepieces[1]).split("=")[1]))
    if linepieces[0]=="getarr": # getarr : name : index : destination
        vars[str(linepieces[3]).split("=")[0]]=arrs[str(linepieces[1]).split("=")[0]][int(str(linepieces[2]).split("=")[1])]
    if linepieces[0].strip()=="string": # string : name = value
        vars[str(linepieces[1]).split("=")[0].strip()]=str(linepieces[1]).split("=")[1]
    if linepieces[0]=="out": #out : name
        #if the variable is a number, print it as a number
        try:
            if isnumber(vars[linepieces[1]]):
                if is_float(vars[linepieces[1]]):
                    print(float(vars[linepieces[1]]))
                else:
                    print(int(vars[linepieces[1]]))
            else:
                print(str(vars[linepieces[1]]))
        except Exception:
            print(linepieces[1])
    if linepieces[0]=="goto": #goto : line
        if linepieces[1] in labels:
            i=labels[linepieces[1]]
            continue
        i=int(linepieces[1])-1
        continue
    if linepieces[0]=="sleep":#sleep : time
        time.sleep(float(linepieces[1]))
    if linepieces[0]=="math":#math : destination : value1 operator value2
        vardest=str(linepieces[1])
        op=get_operator(linepieces[2])
        var1=str(linepieces[2]).split(op)[0]
        var2=str(linepieces[2]).split(op)[1]
        if isnumber(var1):
            var1=float(var1)
        else:
            var1=vars[var1]
        if isnumber(var2):
            var2=float(var2)
        else:
            var2=vars[var2]
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
    if linepieces[0]=="goif": #goif : destination : var1  comparator  var2 

        comp=get_comparator(linepieces[2])
        var1=str(linepieces[2]).split(comp)[0]
        var2=str(linepieces[2]).split(comp)[1]
        if isnumber(var1):
            var1=float(var1)
        else:
            var1=float(vars[var1])
        if isnumber(var2):
            var2=float(var2)
        else:
            var2=float(vars[var2])
        if comp=="<":
            if var1<var2:
                i=int(linepieces[1])-1
                continue
        if comp==">":
            if var1>var2:
                i=int(linepieces[1])-1
                continue
        if comp=="<=":
            if var1<=var2:
                i=int(linepieces[1])-1
                continue
        if comp==">=":
            if var1>=var2:
                i=int(linepieces[1])-1
                continue
        if comp=="==":
            if var1==var2:
                i=int(linepieces[1])-1
                continue
        if comp=="!=":
            if var1!=var2:
                i=int(linepieces[1])-1
                continue
    if linepieces[-1]=="label":# :name:label at the end of the line
        labels[linepieces[-2]]=i
    i+=1
#print("Finished")