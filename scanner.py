file = None
fileMem = ""

def openFile():
    global file 
    global fileMem
    file = open(input("enter file name:\n"))
    for line in file:
        fileMem = fileMem + line
    print("The opened file contains:\n")
    printFile()

def printFile():
    global fileMem
    print(fileMem)

openFile()

