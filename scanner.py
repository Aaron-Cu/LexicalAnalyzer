# 
# Class:       CS 4308 Section 
# Term:        Spring 2022
# Name:        Aaron Cummings
# Instructor:  Sharon Perry
# Project:     Deliverable P1-P3 Scanner/Parser/Interpreter 
# 

from curses.ascii import isdigit


file = None
fileMem = ""
lexemes = []
tokens = []
lexeme = ''
white_space = ' '
new_line = '\n'
operands = ['#','<','>','=','+','-','(',')','~','\n','\t', '\r','<newline>','<tab>','<return>']
keywords = ['if','else','function', 'end', 'print', 'while', 'do', '//', '==']
TermsDictionary = {
    'function' : 'FUNCTION_STATEMENT',
    'end'      : 'END_STATEMENT',
    'print'    : 'PRINT_STATEMENT',
    'while'    : 'WHILE_STATEMENT',
    'do'       : 'DO_STATEMENT',
    'if'       : 'IF_STATEMENT',
    'else'     : 'ELSE_STATEMENT',
    '//'       : 'COMMENT_STATEMENT',
    '<'        : 'LESS_THAN_OPERATOR',
    '>'        : 'GREATER_THAN_OPERATOR',
    '=='       : 'EQUAL_TO_OPERATOR',
    '='        : 'ASSIGNMENT_STATEMENT',
    '+'        : 'ADDITION_OPERATOR',
    '-'        : 'SUBTRACTION_OPERATOR',
    '('        : 'OPEN_PARENTHESIS',
    ')'        : 'CLOSED_PARENTHESIS',
    '~'        : 'APROXIMATION_OPERATOR',
    '<newline>': 'NEW_LINE',
    '<tab>'    : 'TAB',
    '<RETURN>' : 'RETURN',
    '#'        : 'COMMENT_STATEMENT'
}
TERMS = operands + keywords

class treeNode():
        nodeToken = None
        parentNode = None
        childNodes = None
        def __init__(self, nodeToken):
            self.childNodes = []
            self.nodeToken = nodeToken
            return
        
        def addChild(self, child):
            self.childNodes.append(child)
            return
        
        def setParent(self, parent):
            self.parentNode = parent
            return

class parseTree():
    tree = []
    global tokens
    def __init__(self):
        return
    
    def appendNode(self, parent, node):
        if parent == -1: #and len(self.tree)==0
            self.tree.append(treeNode(node))
        elif self.isNode(parent) and not self.isNode(node):
            self.tree.append(treeNode(node))
            self.tree[len(self.tree)-1].setParent(parent)
            self.findNode(parent).addChild(node)
        elif self.isNode(parent) and self.isNode(node):
            self.findNode(self.findNode(node).parentNode).childNodes.remove(node)
            self.findNode(parent).addChild(node)
            self.findNode(node).setParent(parent)
        return

    def isNode(self, node):
        for i in self.tree:
            if i.nodeToken == node:
                return True
        return False

    def findNode(self, node):
        for i in self.tree:
            if i.nodeToken == node:
                return i
        return
    
    def findIndex(self, node):
        counter = 0
        for i in self.tree:
            if i.nodeToken == node:
                return counter
            counter += 1
        return
    
    def printHelper(self, node):
        indent = ''
        hasParent = True
        parent = self.findNode(node).parentNode
        while hasParent == True:
            if parent != None:
                indent = indent + '\t'
                parent = self.findNode(parent).parentNode
            else:
             hasParent = False
        print(indent + str(node) + str(tokens[node])+str(self.findNode(node).parentNode))
        if len(self.findNode(node).childNodes) != 0:
            children = self.findNode(node).childNodes
            for child in children:
                self.printHelper(child)
        return

    def printTree(self):
        index = 0
        for node in self.tree:
            if self.tree[index].parentNode == None:
                self.printHelper(self.tree[index].nodeToken)
            index += 1
        return

parseT = parseTree()
# parseT.appendNode(-1, 34857)
# print(parseT.tree[0].nodeToken)
# parseT.appendNode(34857, 89724)
# print(parseT.findNode(34857).childNodes)
# print(parseT.findNode(parseT.findNode(34857).childNodes[0]).parentNode)


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
                        if lexeme == '=' and fileMem[i+1] == '=':
                            counter = counter + 1
                        else:
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
            if lexeme == '=' and fileMem[i+1] == '==':
                            counter = counter + 1
                            i = i + 1
                            lexeme += fileMem[i]
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

parent = [-1]
def recursiveParse(count = 0):
    global parseT
    global parent
    #print(parent)
    indent = ''
    for i in range(len(parent)):
        indent = indent+'\t|'
    if count == 0:
        with open('par.txt', 'w') as f:
            f.write('[START_FILE] ->')
            print('[START_FILE] ->')
            f.close()
    global tokens
    with open('par.txt', 'a') as f:
        counter = count
        if counter > len(tokens)-1:
                print('\t|[END_FILE]')
                f.write(str('\t|[END_FILE]'+'\n'))
                f.close()
        elif tokens[counter][0] == 'NEW_LINE':
            f.close()
            recursiveParse(counter+1)
        elif tokens[counter][0] == 'COMMENT_STATEMENT':
            skip = counter+1
            while tokens[skip][0] != 'NEW_LINE':
                skip = skip+1
            f.close()
            recursiveParse(skip+1)
        elif tokens[counter][0] == 'FUNCTION_STATEMENT':
            print(indent+'[FUNCTION_STATEMENT] ->')
            f.write(str(indent+'[FUNCTION_STATEMENT] ->'+'\n'))
            f.close()
            parseT.appendNode(parent[len(parent)-1], counter)
            parent.append(counter)
            recursiveParse(counter+1)
        elif tokens[counter][0] == 'END_STATEMENT':
            if parent == []:
                f.close()
            elif parent == [-1]:
                print("here"+ str(parent))
                print('[END_FILE]')
                f.write(str('[END_FILE]'+'\n'))
                f.close()
            else:
                parent.pop()
                indent = ''
                for i in range(len(parent)):
                    indent = indent+'\t|'
                print(indent+'[END_STATEMENT]')
                f.write(str(indent+'[END_STATEMENT]'+'\n'))
                f.close()
                parseT.appendNode(parent[len(parent)-1], counter)
                recursiveParse(counter+1)
        elif tokens[counter][0] == 'ID' or tokens[counter][0] == 'INTEGER':
            f.close()
            parseT.appendNode(parent[len(parent)-1], counter)
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
            print(indent+'['+(tokens[counter][0])+'] -> [ID] [INTEGER] | [ID] [ARITHMETIC_STATEMENT]')
            f.write(str(indent+'['+(tokens[counter][0])+'] -> [ID] [INTEGER] | [ID] [ARITHMETIC_STATEMENT]'+'\n'))
            parseT.appendNode(parent[len(parent)-1], counter)
            if tokens[counter-1][0] == 'ID':
                print(indent+'\t|[ID] -> ['+(tokens[counter-1][1])+']')
                f.write(str(indent+'\t|[ID] -> ['+(tokens[counter-1][1])+']'+'\n'))
                parseT.appendNode(counter, counter-1)
            else:
                print('[ERROR]')
                f.write(str('[ERROR]'+'\n'))
            if tokens[counter+1][0] == 'INTEGER':
                print(indent+'\t|[INTEGER] -> ['+(tokens[counter+1][1])+']')
                f.write(str(indent+'\t|[INTEGER] -> ['+(tokens[counter+1][1])+']'+'\n'))
                parseT.appendNode(counter, counter+1)
            elif tokens[counter+2][0] == ('ADDITION_OPERATOR'):
                print(indent+'\t|[ADDITION_OPERATOR] ->')
                f.write(str(indent+'\t|[ADDITION_OPERATOR] ->'+'\n'))
                parseT.appendNode(counter, counter+2)
                parent.append(counter)
            else:
                print('[ERROR]')
                f.write(str('[ERROR]'+'\n'))
            f.close()
            recursiveParse(counter+2)
        elif tokens[counter][0] == 'PRINT_STATEMENT':
            print(indent+'['+(tokens[counter][0])+'] -> [ID] | [INTEGER]')
            f.write(str(indent+'['+(tokens[counter][0])+'] -> [ID]'+'\n'))
            parseT.appendNode(parent[len(parent)-1], counter)
            if (tokens[counter+2][0] == 'ID') and (tokens[counter+1][0] == 'OPEN_PARENTHESIS') and (tokens[counter+3][0] == 'CLOSED_PARENTHESIS'):
                print(indent+'\t|[ID] -> ['+(tokens[counter+2][1])+']')
                f.write(str(indent+'\t|[ID] -> ['+(tokens[counter+2][1])+']'+'\n'))
                parseT.appendNode(counter, counter+2)
            elif (tokens[counter+2][0] == 'INTEGER') and (tokens[counter+1][0] == 'OPEN_PARENTHESIS') and (tokens[counter+3][0] == 'CLOSED_PARENTHESIS'):
                print(indent+'\t|[INTEGER] -> ['+(tokens[counter+2][1])+']')
                f.write(str(indent+'\t|[INTEGER] -> ['+(tokens[counter+2][1])+']'+'\n'))
                parseT.appendNode(counter, counter+2)
            else:
                print('[ERROR]')
                f.write(str('[ERROR]'+'\n'))
            f.close()
            recursiveParse(counter+4)
        elif tokens[counter][0] == 'WHILE_STATEMENT':
            parseT.appendNode(parent[len(parent)-1], counter)
            parent.append(counter)
            print(indent+'['+(tokens[counter][0])+'] -> [STATEMENT] [DO]')
            f.write(str(indent+'['+(tokens[counter][0])+'] -> [STATEMENT] [DO]'+'\n'))
            f.close()
            recursiveParse(counter+2)
        elif tokens[counter][0] == 'ADDITION_OPERATOR':
            parseT.appendNode(parent[len(parent)-1], counter)
            if counter not in parent:
                print(indent+'['+(tokens[counter][0])+'] -> [ID] [INTEGER] | [ID] [ARITHMETIC_STATEMENT]')
                f.write(str(indent+'['+(tokens[counter][0])+'] -> [ID] [INTEGER]'+'\n'))
            if tokens[counter-1][0] == 'ID':
                parseT.appendNode(counter, counter-1)
                print(indent+'\t|[ID] -> ['+(tokens[counter-1][1])+']')
                f.write(str(indent+'\t|[ID] -> ['+(tokens[counter-1][1])+']'+'\n'))
            else:
                print('[ERROR]')
                f.write(str('[ERROR]'+'\n'))
            if tokens[counter+1][0] == 'INTEGER':
                parseT.appendNode(counter, counter+1)
                print(indent+'\t|[INTEGER] -> ['+(tokens[counter+1][1])+']')
                f.write(str(indent+'\t|[INTEGER] -> ['+(tokens[counter+1][1])+']'+'\n'))
                f.close()
                parent.pop()
                #recursiveParse(counter+2)
            elif tokens[counter+2][0] == ('ADDITION_OPERATOR'):
                parseT.appendNode(counter, counter+2)
                print(indent+'\t|[ADDITION_OPERATOR] ->')
                f.write(str(indent+'\t|[ADDITION_OPERATOR] ->'+'\n'))
                parent.append(counter)
            else:
                print('[ERROR]')
                f.write(str('[ERROR]'+'\n'))
            if counter in parent:
                parent.pop()
            f.close()
            recursiveParse(counter+2)
        elif tokens[counter][0] == 'IF_STATEMENT':
            parseT.appendNode(parent[len(parent)-1], counter)
            parent.append(counter)
            print(indent+'['+(tokens[counter][0])+']')
            f.write(str(indent+'['+(tokens[counter][0])+']'+'\n'))
            f.close()
            recursiveParse(counter+2)
        elif tokens[counter][0] == 'ELSE_STATEMENT':
            ifState = parent.pop()
            if tokens[ifState][0] == 'IF_STATEMENT':
                indent = ''
                for i in range(len(parent)):
                    indent = indent+'\t|'
                parseT.appendNode(parent[len(parent)-1], counter)
                parent.append(counter)
                print(indent+'['+(tokens[counter][0])+']')
                f.write(str(indent+'['+(tokens[counter][0])+']'+'\n'))
            else:
                print('[ERROR]')
                f.write(str('[ERROR]'+'\n'))
            f.close()
            recursiveParse(counter+1)
        elif tokens[counter][0] == 'EQUAL_TO_OPERATOR' or 'LESS_THAN_OPERATOR' or 'GREATER_THAN_OPERATOR':
            parseT.appendNode(parent[len(parent)-1], counter)
            if counter not in parent:
                print(indent+'['+(tokens[counter][0])+'] -> [ID] [INTEGER] | [ID] [ARITHMETIC_STATEMENT]')
                f.write(str(indent+'['+(tokens[counter][0])+'] -> [ID] [INTEGER]'+'\n'))
            if tokens[counter-1][0] == 'ID':
                parseT.appendNode(counter, counter-1)
                print(indent+'\t|[ID] -> ['+(tokens[counter-1][1])+']')
                f.write(str(indent+'\t|[ID] -> ['+(tokens[counter-1][1])+']'+'\n'))
            else:
                print('[ERROR]')
                f.write(str('[ERROR]'+'\n'))
            if tokens[counter+1][0] == 'INTEGER':
                parseT.appendNode(counter, counter+1)
                print(indent+'\t|[INTEGER] -> ['+(tokens[counter+1][1])+']')
                f.write(str(indent+'\t|[INTEGER] -> ['+(tokens[counter+1][1])+']'+'\n'))
                f.close()
            elif tokens[counter+2][0] == ('ADDITION_OPERATOR'):
                parseT.appendNode(counter, counter+2)
                print(indent+'\t|[ADDITION_OPERATOR] ->')
                f.write(str(indent+'\t|[ADDITION_OPERATOR] ->'+'\n'))
                parent.append(counter)
            else:
                print('[ERROR]')
                f.write(str('[ERROR]'+'\n'))
            if counter in parent:
                parent.pop()
            f.close()
            recursiveParse(counter+2) 
        else:
            print(indent+'['+(tokens[counter][0])+']')
            f.write(str(indent+'['+(tokens[counter][0])+']'+'\n'))
            f.close()
            recursiveParse(counter+1)   

def interpret():
    global parseT
    global tokens
    ifCondition = False
    functions = []
    variables = []

    def interpretTreeFunctions():
        global parseT
        nonlocal functions
        global tokens
        index = 0
        for node in parseT.tree:
            if parseT.tree[index].parentNode == None:
                if tokens[parseT.tree[index].nodeToken][0] == 'FUNCTION_STATEMENT':
                    functions.append([tokens[parseT.tree[index].childNodes[0]][1], index])
            index += 1
        for id in functions:
            print('Function Name: '+id[0])
        return
    
    def findVarIndex(name):
        nonlocal variables
        counter = 0
        for var in variables:
            if var[0] == name:
                return counter
            else:
                counter += 1
    
    def isVar(name):
        nonlocal variables
        for var in variables:
            if var[0] == name:
                return True
        return False

    def interpretFunction(functionNode):
        global parseT
        global tokens
        nonlocal variables
        nonlocal ifCondition
        if (tokens[parseT.tree[functionNode].nodeToken][0] == 'FUNCTION_STATEMENT') or (tokens[parseT.tree[functionNode].nodeToken][0] =='IF_STATEMENT') or (tokens[parseT.tree[functionNode].nodeToken][0] =='ELSE_STATEMENT'):
            if tokens[parseT.tree[functionNode].nodeToken][0] == 'IF_STATEMENT':
                if interpretFunction(parseT.findIndex(parseT.tree[functionNode].childNodes[0])) == False:
                    return
                else:
                    ifCondition = True
            
            for child in parseT.tree[functionNode].childNodes:
                # print("Current child:" + str(child) + str(tokens[child][0]))
                if tokens[child][0] == 'ID':
                    print('Function ID:'+str(tokens[child][1]))
                if tokens[child][0] == 'ASSIGNMENT_STATEMENT':
                    #print(parseT.findIndex(child))
                    interpretFunction(parseT.findIndex(child))
                if tokens[child][0] == 'PRINT_STATEMENT':
                    #print(parseT.findIndex(child))
                    interpretFunction(parseT.findIndex(child))
                if tokens[child][0] == 'WHILE_STATEMENT':
                    #print(parseT.findIndex(child))
                    interpretFunction(parseT.findIndex(child))
                if tokens[child][0] == 'IF_STATEMENT':
                    #print(parseT.findIndex(child))
                    interpretFunction(parseT.findIndex(child))
                if tokens[child][0] == 'ELSE_STATEMENT':
                    #print(parseT.findIndex(child))
                    if ifCondition == False:
                        interpretFunction(parseT.findIndex(child))
                    else:
                        ifCondition = False
        elif tokens[parseT.tree[functionNode].nodeToken][0] == 'ADDITION_OPERATOR':
            first = None
            second = None
            if tokens[parseT.tree[functionNode].childNodes[0]][0] == 'ID':
                if isVar(tokens[parseT.tree[functionNode].childNodes[0]][1]):
                    first = variables[findVarIndex(tokens[parseT.tree[functionNode].childNodes[0]][1])][1]
                    #print(first)
            elif tokens[parseT.tree[functionNode].childNodes[0]][0] == 'INTEGER':
                first = tokens[parseT.tree[functionNode].childNodes[0]][1]
                #print(first)
            if tokens[parseT.tree[functionNode].childNodes[1]][0] == 'ID':
                if isVar(tokens[parseT.tree[functionNode].childNodes[1]][1]):
                    second = variables[findVarIndex(tokens[parseT.tree[functionNode].childNodes[1]][1])][1]
                    #print(second)
            elif tokens[parseT.tree[functionNode].childNodes[1]][0] == 'INTEGER':
                second = tokens[parseT.tree[functionNode].childNodes[1]][1]
                #print(second)
            return int(first) + int(second)
        elif tokens[parseT.tree[functionNode].nodeToken][0] == 'ASSIGNMENT_STATEMENT':
            if isVar(tokens[parseT.tree[functionNode].childNodes[0]][1]) == False:
                variables.append([tokens[parseT.tree[functionNode].childNodes[0]][1],tokens[parseT.tree[functionNode].childNodes[1]][1]])
            elif tokens[parseT.tree[functionNode].childNodes[1]][0] == 'INTEGER':
                variables[findVarIndex(tokens[parseT.tree[functionNode].childNodes[0]][1])][1] = tokens[parseT.tree[functionNode].childNodes[1]][1]
            elif tokens[parseT.tree[functionNode].childNodes[1]][0] == 'ADDITION_OPERATOR':
                variables[findVarIndex(tokens[parseT.tree[functionNode].childNodes[0]][1])][1] = interpretFunction(parseT.findIndex(parseT.tree[functionNode].childNodes[1]))
            print("CURRENT_MEM: " +str(variables))
        elif tokens[parseT.tree[functionNode].nodeToken][0] == 'PRINT_STATEMENT':
            if (tokens[parseT.tree[functionNode].childNodes[0]][0] == 'ID') and (isVar(tokens[parseT.tree[functionNode].childNodes[0]][1]) == True):
                print("consoleout$ " +str(variables[findVarIndex(tokens[parseT.tree[functionNode].childNodes[0]][1])][1]))
            elif (tokens[parseT.tree[functionNode].childNodes[0]][0] == 'INTEGER'):
                print("consoleout$ " +str(tokens[parseT.tree[functionNode].childNodes[0]][1]))
            else:
                print("INTERPRETOR ERROR")
        elif tokens[parseT.tree[functionNode].nodeToken][0] == 'WHILE_STATEMENT':
            if tokens[parseT.tree[functionNode].childNodes[0]][0] == 'EQUAL_TO_OPERATOR' or 'LESS_THAN_OPERATOR' or 'GREATER_THAN_OPERATOR':
                #print(parseT.findIndex(parseT.tree[functionNode].childNodes[0]))
                if interpretFunction(parseT.findIndex(parseT.tree[functionNode].childNodes[0])) == True:
                    for child in parseT.tree[functionNode].childNodes:
                        #print("Current child:" + str(child) + str(tokens[child][0]))
                        if tokens[child][0] == 'ID':
                            print('Function ID:'+str(tokens[child][1]))
                        if tokens[child][0] == 'ASSIGNMENT_STATEMENT':
                            #print(parseT.findIndex(child))
                            interpretFunction(parseT.findIndex(child))
                        if tokens[child][0] == 'PRINT_STATEMENT':
                            #print(parseT.findIndex(child))
                            interpretFunction(parseT.findIndex(child))
                        if tokens[child][0] == 'END_STATEMENT':
                            #print(parseT.findIndex(child))
                            interpretFunction(functionNode)
                    interpretFunction(functionNode)
        elif tokens[parseT.tree[functionNode].nodeToken][0] =='EQUAL_TO_OPERATOR' or 'LESS_THAN_OPERATOR' or 'GREATER_THAN_OPERATOR':
            first = None
            second = None
            if tokens[parseT.tree[functionNode].childNodes[0]][0] == 'ID':
                if isVar(tokens[parseT.tree[functionNode].childNodes[0]][1]):
                    first = variables[findVarIndex(tokens[parseT.tree[functionNode].childNodes[0]][1])][1]
                    #print(first)
            elif tokens[parseT.tree[functionNode].childNodes[0]][0] == 'INTEGER':
                first = tokens[parseT.tree[functionNode].childNodes[0]][1]
                #print(first)
            if tokens[parseT.tree[functionNode].childNodes[1]][0] == 'ID':
                if isVar(tokens[parseT.tree[functionNode].childNodes[1]][1]):
                    second = variables[findVarIndex(tokens[parseT.tree[functionNode].childNodes[1]][1])][1]
                    #print(second)
            elif tokens[parseT.tree[functionNode].childNodes[1]][0] == 'INTEGER':
                second = tokens[parseT.tree[functionNode].childNodes[1]][1]
                #print(second)
            if tokens[parseT.tree[functionNode].nodeToken][0] =='EQUAL_TO_OPERATOR':
                if int(first) == int(second):
                    return True
            if tokens[parseT.tree[functionNode].nodeToken][0] =='LESS_THAN_OPERATOR':
                if int(first) < int(second):
                    return True
            if tokens[parseT.tree[functionNode].nodeToken][0] =='GREATER_THAN_OPERATOR':
                if int(first) > int(second):
                    return True
            return False
        return
    
    interpretTreeFunctions()
    while input('Enter "y" to interpret a function, enter to quit.\n') == 'y':
        find = input('enter function name\n')
        for i in functions:
            if find == i[0]:
                variables = []
                print("----output-----")
                interpretFunction(i[1])
                print("---------------")
    return

while input('Enter "y" to interpret a .jl file, enter to quit.\n') == 'y':
    file = None
    fileMem = ""
    lexeme = ''
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
    # for node in parseT.tree:
    #     print(tokens[node.nodeToken],node.nodeToken,node.parentNode,node.childNodes)
    # print()
    # parseT.printTree()
    interpret()
    #for token, lex in tokens:
    #    print(token+" : "+lex)
