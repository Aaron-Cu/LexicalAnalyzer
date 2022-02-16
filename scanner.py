file = None

def openFile():
    global file 
    file = open(input("enter file name:\n"))

def printFile():
    global file
    for line in file:
        print(line)

openFile()
printFile()
