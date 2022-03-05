file = None
fileMem = ""
lexeme = ''
white_space = ' '
new_line = '\n'
operands = ['<','>','=','+','-','(',')','~','\n','\t', '\r']
keywords = ['function', 'end', 'print', 'while', 'do', '//']
TERMS = operands + keywords

def openFile():
    global file 
    global fileMem
    file = open(input("enter file name:\n"))
    for line in file:
        fileMem = fileMem + line
    file.close()
    print("The opened file contains:\n")
    printFile()
    printChar()

def printFile():
    global fileMem
    print(fileMem)
        
def printChar():
    global fileMem
    for i, char in enumerate(fileMem):
        print('char', str(i+1).rjust(3, ' '), ':', char)

def lexerToFile():
    global fileMem
    global lexeme
    global white_space
    global new_line
    global TERMS
    counter = 0
    with open('lex.txt', 'w') as f:
        for i, char in enumerate(fileMem):
            lexeme += char
            if (i+1 < len(fileMem)):
                if fileMem[i+1] == white_space or fileMem[i+1] in TERMS or lexeme in TERMS:
                    if lexeme == white_space:
                        lexeme = ''
                    if lexeme != '':
                        lexeme = lexeme.replace('\n','<newline>')
                        lexeme = lexeme.replace('\t','<tab>')
                        lexeme = lexeme.replace('\r', '<return>')
                        lexeme = lexeme.strip()
                        f.write(str('lexme'+str(counter+1).rjust(3, ' ')+':'+lexeme+'\n'))
                        lexeme = ''
                        counter = counter + 1
        if lexeme != '':
            lexeme = lexeme.strip()
            f.write(str('lexme'+str(counter+1).rjust(3, ' ')+':'+lexeme+'\n'))
        f.close()

openFile()
lexerToFile()
