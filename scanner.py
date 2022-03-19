from curses.ascii import isdigit
from email.policy import default


file = None
fileMem = ""
lexeme = ''
white_space = ' '
new_line = '\n'
operands = ['<','>','=','+','-','(',')','~','\n','\t', '\r']
keywords = ['function', 'end', 'print', 'while', 'do', '//']
TermsDictionary = {
    'function' : 1,
    'end'      : 2,
    'print'    : 3,
    'while'    : 4,
    'do'       : 5,
    'integer'  : 6
}
TERMS = operands + keywords
lexemes = []
tokens = []

# Takes a user input file name, opens and saves the contents
# to fileMem. 
def openFile():
    global file 
    global fileMem
    file = open(input("enter file name:\n"))
    for line in file:
        fileMem = fileMem + line
    file.close()
    print("The opened file contains:\n")
    printFile()

# Prints the contents of fileMem to the console. 
def printFile():
    global fileMem
    print(fileMem)
        
# Prints every char in order of the file in fileMem.
def printChar():
    global fileMem
    for i, char in enumerate(fileMem):
        print('char', str(i+1).rjust(3, ' '), ':', char)

# Generates a list of lexemes from the source code file stored
# in fileMem. The list is stored in memory as lexmes, as well
# written to the file lex.txt.
def lexer():
    global fileMem
    global lexeme
    global white_space
    global new_line
    global TERMS
    global lexemes
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
                        f.write(str('lexeme'+str(counter+1).rjust(3, ' ')+':'+lexeme+'\n'))
                        lexemes.append(lexeme)
                        lexeme = ''
                        counter = counter + 1
        if lexeme == white_space:
            lexeme = ''
        if lexeme != '':
            lexeme = lexeme.replace('\n','<newline>')
            lexeme = lexeme.replace('\t','<tab>')
            lexeme = lexeme.replace('\r', '<return>')
            lexeme = lexeme.strip()
            f.write(str('lexeme'+str(counter+1).rjust(3, ' ')+':'+lexeme+'\n'))
            lexemes.append(lexeme)
        f.close()

# Prints the lexems of the scanned file. 
def printLexemes():
    global lexemes
    for lexeme in lexemes:
        print(lexeme)

def tokenLookUp(lexeme):
    global TERMS
    temp = ''
    if lexeme in TERMS:
        return TermsDictionary[lexeme]
    if lexeme.isdigit():
        return 'integer'
    else:
        return 'name?'
    # .isdigit() find out if 
        

def tokenizer():
    global lexemes
    global tokens
    with open('tkn.txt', 'w') as f:
        for lexeme in lexemes:
            tokens.appened(tokenLookUp(lexeme))



openFile()
lexer()
printLexemes()
print("lex.txt now contains the parsed lexemes of given file.")
