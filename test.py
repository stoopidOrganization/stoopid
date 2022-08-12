#Tests for stoopid interpreter
import os
def test_file(file):
    with open(file, "r") as f:
        header = f.readlines()[0]

    if header.startswith("#expected"):
        print(f"{file} is a valid test file\n")
    else:
        print(f"{file} is not a valid test file")
        exit(1)
    #get the expected output
    with open(file,"r") as f:
        expected=header.split(":")[1].split(",")
    print("The expected output is:")
    for i in expected:
        print(i)
    os.system(f"python stoopid.py {file} --log output.txt --silent")
    with open("output.txt","r") as f:
        output=f.readlines()
    print("The output is:")
    o=[]
    for i in output:
        if i.strip().replace("\n","")!="":
            o.append(i.strip().replace("\n",""))
            print(i.strip().replace("\n",""))
    for i in range(len(expected)):
        try:
            if o[i].strip()!=expected[i].strip():
                print(f"{file} failed")
                return 0
        except Exception:
            print(f"{file} failed")
            return 0
    print(f"\n {file} passed")
    print("Cleaning up...")
    os.system("rm output.txt")
    return 1



test_file("test.stpd")