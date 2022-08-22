#Tests for stoopid interpreter
import os,sys
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
    failed="Passed"
    for i in range(len(expected)):
        try:
            if o[i].strip()!=expected[i].strip():
                print(f"{file} failed in line {i+1}")
                failed="Failed"
        except Exception:
            print(f"{file} failed in line {i+1} (something happened, idk)")
            failed="Failed"
    print(f"\n {file} {failed}")

    os.system("del output.txt")
    return 1



test_file(sys.argv[1])