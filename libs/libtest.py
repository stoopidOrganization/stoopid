# testLib
defaults = {}


def testcmd(pieces):
    print("this is a test and i am testing: " + pieces[1])


def main(mainDefaults):
    global defaults
    defaults = mainDefaults

    keywords = {"test": testcmd}

    return keywords
