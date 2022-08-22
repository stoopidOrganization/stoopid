import sys,os
installdir="%appdata%\\stoopid"
if input("Do you want to install or update stoopid? (y/n)")=="y":
    #resolve path
    installdir=installdir.replace("%appdata%",os.getenv("APPDATA"))
    if not os.path.exists(installdir):
        os.mkdir(installdir)
    files=[
        "stoopid.py",
        "build.bat",
        "stoopid.exe"
    ]
    #install the requirements
    os.system("pip install -r requirements.txt")
    for file in files:
        os.system("copy %s %s" % (file,installdir))
    #add the path to the environment variables
    user=os.getenv("USERNAME")
    #get the path for the current user
    cpath=os.popen("reg query \"HKCU\Environment\" /v PATH").read()
    cpath=cpath.split("REG_SZ")[1].strip()
    #print(cpath)
    if not installdir in cpath and input("Do you want to add stoopid to path? [y/n]").strip()=="y":
        cpath+=";%s" % installdir
        #print(cpath)
        command="setx PATH \"%s\"" % cpath
        #print(command)
        os.system(command)
        print("Added %s to PATH" % installdir)
        print("You can now run stoopid by typing stoopid in your terminal")
    else:
        if installdir in cpath:
            print("Stoopid is already in path")
        print("Not adding to path...")
    print("Installation complete!")
else:
    print("Installation cancelled")