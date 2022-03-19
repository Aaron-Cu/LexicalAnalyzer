from curses.ascii import isdigit    # requires '$ pip install windows-curses' on windows based systems.


file = None
fileMem = ""
lexemes = []
tokens = []
lexeme = ''
white_space = ' '
new_line = '\n'
operands = ['<','>','=','+','-','(',')','~','\n','\t', '\r','<newline>','<tab>','<return>']
keywords = ['function', 'end', 'print', 'while', 'do', '//']
TermsDictionary = {
    'function' : 'FUNCTION_STATEMENT',
    'end'      : 'END_STATEMENT',
    'print'    : 'PRINT_STATEMENT',
    'while'    : 'WHILE_STATEMENT',
    'do'       : 'DO_STATEMENT',
    '//'       : 'COMMENT_STATEMENT',
    '<'        : 'LESS_THAN_OPERATOR',
    '>'        : 'GREATER_THAN_OPERATOR',
    '='        : 'ASSIGNMENT_STATEMENT',
    '+'        : 'ADDITION_OPERATOR',
    '-'        : 'SUBTRACTION_OPERATOR',
    '('        : 'OPEN_PARENTHESIS',
    ')'        : 'CLOSED_PARENTHESIS',
    '~'        : 'APROXIMATION_OPERATOR',
    '<newline>': 'NEW_LINE',
    '<tab>'    : 'TAB',
    '<RETURN>' : 'RETURN'
}
TERMS = operands + keywords


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
        return 'INTEGER'
    else:
        return 'ID'
    # .isdigit() find out if 
        

def tokenizer():
    global lexemes
    global tokens
    with open('tkn.txt', 'w') as f:
        for lexeme in lexemes:
            tempToken = tokenLookUp(lexeme)
            tokens.append([tempToken,lexeme])
            f.write(str(tempToken+':'+lexeme+'\n'))
    f.close()

def printTokens():
    global tokens
    tempToken = ''
    for token in tokens:
        for i in token:
            if tempToken == '':
                tempToken+=(i+':')
            else:
                tempToken+=i
        print(tempToken)
        tempToken=''

def recursiveParse(count = 0):
    if count == 0:
        with open('par.txt', 'w') as f:
            f.write('')
            f.close()
    global tokens
    with open('par.txt', 'a') as f:
        if count > len(tokens):
            print('went over')
            return
        counter = count
        if tokens[counter][0] == 'NEW_LINE':
            f.close()
            recursiveParse(counter+1)
        elif tokens[counter][0] == 'COMMENT_STATEMENT':
            skip = counter+1
            while tokens[skip][0] != 'NEW_LINE':
                skip = skip+1
            f.close()
            recursiveParse(skip+1)
        elif tokens[counter][0] == 'FUNCTION_STATEMENT':
            print('[start] ->')
            f.write(str('[start] ->'+'\n'))
            f.close()
            recursiveParse(counter+1)
        elif tokens[counter][0] == 'END_STATEMENT':
            print('[end]')
            f.write(str('[end]'+'\n'))
            f.close()
        elif tokens[counter][0] == 'ID' or tokens[counter][0] == 'INTEGER':
            f.close()
            recursiveParse(counter+1)
        elif tokens[counter][0] == 'TAB':
            f.close()
            recursiveParse(counter+1)
        elif tokens[counter][0] == 'OPEN_PARENTHESIS':
            f.close()
            recursiveParse(counter+1)
        elif tokens[counter][0] == 'CLOSED_PARENTHESIS':
            f.close()
            recursiveParse(counter+1)
        elif tokens[counter][0] == 'ASSIGNMENT_STATEMENT':
            print('['+(tokens[counter][0])+'] -> [ID] [INTEGER]')
            f.write(str('['+(tokens[counter][0])+']'+'\n'))
            if tokens[counter-1][0] == 'ID':
                print('\t|[ID] -> ['+(tokens[counter-1][1])+']')
                f.write(str('\t|[ID] -> ['+(tokens[counter-1][1])+']'+'\n'))
            else:
                print('[ERROR]')
                f.write(str('[ERROR]'+'\n'))
            if tokens[counter+1][0] == 'INTEGER':
                print('\t|[INTEGER] -> ['+(tokens[counter+1][1])+']')
                f.write(str('\t|[INTEGER] -> ['+(tokens[counter+1][1])+']'+'\n'))
            else:
                print('[ERROR]')
                f.write(str('[ERROR]'+'\n'))
            f.close()
            recursiveParse(counter+2)
        elif tokens[counter][0] == 'PRINT_STATEMENT':
            print('['+(tokens[counter][0])+'] -> [ID]')
            f.write(str('['+(tokens[counter][0])+']'+'\n'))
            if tokens[counter+2][0] == 'ID' and tokens[counter+1][0] == 'OPEN_PARENTHESIS' and tokens[counter+3][0] == 'CLOSED_PARENTHESIS':
                print('\t|[ID] -> ['+(tokens[counter+2][1])+']')
                f.write(str('\t|[ID] -> ['+(tokens[counter+2][1])+']'+'\n'))
            else:
                print('[ERROR]')
                f.write(str('[ERROR]'+'\n'))
            f.close()
            recursiveParse(counter+4)
        else:
            print('['+(tokens[counter][0])+']')
            f.write(str('['+(tokens[counter][0])+']'+'\n'))
            f.close()
            recursiveParse(counter+1)   



while input('Enter "y" to interpret a .jl file, enter to quit.\n') == 'y':
    file = None
    fileMem = ""
    lexemes = []
    tokens = []
    openFile()
    print('----------------------------------')
    lexer()
    printLexemes()
    print("lex.txt now contains the parsed lexemes of given file.")
    print('----------------------------------')
    tokenizer()
    printTokens()
    print('----------------------------------')
    print('Starting Parse..')
    recursiveParse()
