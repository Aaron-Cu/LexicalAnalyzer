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
    'do'       : 5
}
TERMS = operands + keywords
tokens = []

def openFile():
    global file 
    global fileMem
    file = open(input("enter file name:\n"))
    for line in file:
        fileMem = fileMem + line
    file.close()
    print("The opened file contains:\n")
    printFile()

def printFile():
    global fileMem
    print(fileMem)
        
def printChar():
    global fileMem
    for i, char in enumerate(fileMem):
        print('char', str(i+1).rjust(3, ' '), ':', char)

def tokenizer():
    global fileMem
    global lexeme
    global white_space
    global new_line
    global TERMS
    global tokens
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
                        f.write(str('token'+str(counter+1).rjust(3, ' ')+':'+lexeme+'\n'))
                        tokens.append(lexeme)
                        lexeme = ''
                        counter = counter + 1
        if lexeme == white_space:
            lexeme = ''
        if lexeme != '':
            lexeme = lexeme.replace('\n','<newline>')
            lexeme = lexeme.replace('\t','<tab>')
            lexeme = lexeme.replace('\r', '<return>')
            lexeme = lexeme.strip()
            f.write(str('token'+str(counter+1).rjust(3, ' ')+':'+lexeme+'\n'))
            tokens.append(lexeme)
        f.close()

def printTokens():
    global tokens
    for token in tokens:
        print(token)

openFile()
tokenizer()
print("lex.txt now contains the parsed tokens of given file.")
printTokens()
