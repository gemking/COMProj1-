import sys
import re
with open(sys.argv[1], "r") as file: #opens file
    filelines = file.read().splitlines() # reads file and splits lines
    file.close() #closes file


insideComment = 0


keywords = ["if", "else", "while", "int", "float", "void", "return"] #denotes all keywords
symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]" #denotes symbols used
comparisionSymbols = ["==","<=",">=","!=","<",">"]
additionSubtractionSymbols = ["-","+"]
multiplicationDivisionSymbols = ["/", "*"]
miniKeywords = ["void", "int", "float"]
miniKeywordsTwo = ["while", "if", "return", "(", ";", "{"]
characters = "[a-zA-Z]+" #obtains all words for the IDs
digits = "[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?" #gets all decimal values, including integer values 0-9
errors = "\S" #reports errors
token = []  # creates a list that holds all of the tokens
x = 0  #value that holds the token counter for the parser

for importantLines in filelines: #receiving importantlines from filelines
    importantLine = importantLines #sets importantLine to importantLines


    if not importantLine:
        continue # if not an important line, it continues through the file

    list = "(%s)|(%s)|(%s)|(%s)" % (characters, digits, symbols, errors)  # puts entire library into a list of strings

    for word in re.findall(list, importantLine): #finds list
        if re.match(characters, word[0]) and insideComment == 0: #matches characters and makes sure insideComment is 0
            if word[0] in keywords:
                token.append(word[0]) #keyword is constructed out of characters a-zA-Z
            else:
                token.append(word[0]) #appends character values that are not keywords




        elif re.match(digits,word[1]) and insideComment == 0: #matches digits and makes sure inside comment is 0
            if "." in word[1]:
                token.append(word[1]) #checks if value is a decimal value and appends
            elif "E" in word[1]:
                token.append(word[1]) #checks if value is an expontential value and appends
            else:
                token.append(word[1]) #appends integer value
        elif re.match(symbols, word[4]): #matches symbols
            if "/*" in word[4]: #Checks when word approaches /*
                insideComment = insideComment + 1 #increments insideComment if inside
            elif "*/" in word[4] and insideComment > 0: #Checks when word approaches */
                insideComment = insideComment - 1 #decrements insideComment if outside
            elif "//" in word[4] and insideComment == 0: #If neither
                break
            elif insideComment == 0: #when inside counter is 0
                if "*/" in word[4]: #when it reaches terminal */
                    if "*/*" in importantLine: #when it's still sorting through comments
                        token.append("*")
                        insideComment += 1
                        continue #skips comments and continue through the program
                    else:
                        token.append("*") #appends multiplication symbol
                        token.append("/") #appends division symbol
                else:
                    # print t[5]
                    token.append(word[4]) #appends rest of symbols
        elif word[3] and insideComment == 0: #matches errors and makes sure insideComment is 0
            # print "ERROR:", t[6]
            token.append(word[3]) #appends error

                    # ----- end of lexer ----- #

token.append("$")  # add to end to check if done parsing
checkMain = 0  # check for 1 main function
checkFinalMain = 0  # check if main is last function
isCompleted = 0
leftExpression = 0
rightExpression = 0
expressionReturn = 0
matchParameter = 0
theParameter = 0

variableDeclaration = []  # list to hold declared variables, type, and scope
variableType = []  # list of type of variables
variableOperation = []  # check for operand and operator agreement, i.e. int x; x = "hi"
vars = []  # list to hold all declared variables
varsScope = []  # list of all variable scopes, as in what functions they are in
varsScopeBlock = []  # list of all variable scopes, as in block number

functionDeclaration = []  # list to hold declared functions with parms/args
functionIndex = 0  # index to keep track of parameters/args for a function
functionCall = []  # functions called
functionCallArguments = []  # list of argument types in a function's parameters
functionNames = []  # list of all function names
functionTypes = []  # list of all function types
functionName = 0  # function name, for scope
functionType = 0  # function type, determine if it needs return
currentScope = 0  # current scope
functionReturn = 0  # does function have a return
functionReturn = 0  # check if int/float function has return

# ---------------------------------- parsing functions ----------------------------------- #


def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def programDeclaration(): #runs program(Rule 1)
    global isCompleted
    declarationList()
    if "$" in token[x]:
        isCompleted = 1 #continues outside
    else:
        print ("REJECT") #if not, Reject


def declarationList(): #Rule 2
    declaration()
    declarationListPrime()


def declarationListPrime(): #Rule 3
    if token[x] in miniKeywords:
        declaration()
        declarationListPrime()
    elif "$" in token[x]:
        return
    else:
        return


def declaration():  # 4
    global x, checkMain, functionName, currentScope, functionType, functionReturn, checkFinalMain
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        if "main" in token[x]:
            checkMain += 1
            checkFinalMain = 1
            if token[x-1] != "void":
                print("REJECT")
                exit(0)
        else:
            checkFinalMain = 0

        x += 1  # Accept ID
        if ";" in token[x]:
            x += 1  # Accept ;
            k = 0
            for v in vars:  # check for duplicate declared variables
                if token[x-2] in v:
                    if variableType[k] in token[x - 3]:
                        print("REJECT")
                        exit(0)
                k += 1

            variableDeclaration.append(token[x - 3] + " " + token[x - 2] + " global 0")
            vars.append(token[x-2])
            variableType.append(token[x - 3])
            varsScope.append("global")
            varsScopeBlock.append(0)

            if "void" in token[x-3]:
                print("REJECT")
                exit(0)

        elif "[" in token[x]:
            x += 1  # Accept [
            k = 0
            for v in vars:  # check for duplicate declared variables
                if token[x-2] in v:
                    if variableType[k] in token[x - 3]:
                        print("REJECT")
                        exit(0)
                k += 1

            variableDeclaration.append(token[x - 3] + " " + token[x - 2] + " global 0")
            vars.append(token[x-2])
            variableType.append(token[x - 3])
            varsScope.append("global")
            varsScopeBlock.append(0)

            if "void" in token[x-3]:
                print("REJECT")
                exit(0)

            z = hasnum(token[x])
            if z is True:
                x += 1  # Accept NUM/FLOAT
                if "]" in token[x]:
                    x += 1  # Accept ]
                    if ";" in token[x]:
                        x += 1  # Accept ;
                    else:
                        print("REJECT")
                        exit(0)
                else:
                    print("REJECT")
                    exit(0)
            else:
                print("REJECT")
                exit(0)
        elif "(" in token[x]:
            x += 1  # Accept (
            for v in functionDeclaration:  # check for duplicate declared functions
                if token[x-2] in v:
                    print("REJECT")
                    exit(0)
            functionDeclaration.append(token[x - 3] + " " + token[x - 2])
            functionName = token[x - 2]
            functionNames.append(token[x - 2])
            functionTypes.append(token[x - 3])
            functionType = token[x-3]
            functionReturn = 0
            currentScope = 0

            parameters()

            if ")" in token[x]:
                x += 1  # Accept )
                compoundStatement()

                if functionReturn == 0 and "int" in functionType: #check if not funtype in "int"
                    print("REJECT")
                    exit(0)
                elif functionReturn == 0 and "float" in functionType:
                    print("REJECT")
                    exit(0)
                else:
                    functionReturn = 0

            else:
                print("REJECT")
                exit(0)
        else:
            print("REJECT")
            exit(0)
    else:
        print("REJECT")
        exit(0)


def theVariableDeclaration():  # 5
    global x, checkMain
    typeSpecifier()

    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        k = 0
        for v in vars:  # check for duplicate declared variables
            if token[x-1] in v:
                if varsScope[k] in functionName:
                    if varsScopeBlock[k] >= currentScope:
                        print("REJECT")
                        exit(0)
            k += 1
        variableDeclaration.append(token[x - 2] + " " + token[x - 1] + " " + str(functionName) + " " + str(currentScope))
        vars.append(token[x-1])
        variableType.append(token[x - 2])
        varsScope.append(functionName)
        varsScopeBlock.append(currentScope)

        if "void" in token[x-2]:  # check if ID is type void
            print("REJECT")
            exit(0)
    else:
        print("REJECT")
        exit(0)

    if ";" in token[x]:
        x += 1  # Accept ;
    elif "[" in token[x]:
        x += 1  # Accept [
        w = hasnum(token[x])
        if w is True:
            x += 1  # Accept NUM/FLOAT
            if "." in token[x-1]:  # check for float in array declaration
                print("REJECT")
                exit(0)
            if "E" in token[x-1]:  # check for float in array declaration
                print("REJECT")
                exit(0)
            if "]" in token[x]:
                x += 1  # Accept ]
                if ";" in token[x]:
                    x += 1  # Accept ;
                    return
                else:
                    print("REJECT")
                    exit(0)
            else:
                print("REJECT")
                exit(0)
        else:
            print("REJECT")
            exit(0)
    else:
        print("REJECT")
        exit(0)


def typeSpecifier():  # 6
    global x
    if token[x] in miniKeywords:
        x += 1  # Accept int/void/float
    else:
        return


def parameter():  # 7
    global x, checkMain
    typeSpecifier()

    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        if "main" in token[x]:
            checkMain += 1
        x += 1  # Accept ID
    else:
        return

    if "(" in token[x]:
        x += 1  # Accept (
    else:
        print("REJECT")
        exit(0)

    parameters()

    if ")" in token[x]:
        x += 1  # Accept )
    else:
        print("REJECT")
        exit(0)

    compoundStatement()


def parameters():  # 8
    global x, functionIndex
    if token[x] in miniKeywords:
        parametersList()
        functionIndex += 1
    else:
        print("REJECT")
        exit(0)


def parametersList():  # 9
    parameterPrime()
    parametersListPrime()


def parametersListPrime():  # 10
    global x
    if "," in token[x]:
        x += 1  # Accept ,
        parameterPrime()
        parametersListPrime()
    elif ")" in token[x]:
        return
    else:
        return


def parameterPrime():  # 11
    global x, functionName, currentScope
    typeSpecifier()
    functionDeclaration[functionIndex] = functionDeclaration[functionIndex] + " " + token[x - 1]
    functionCallArguments.append("")
    functionCallArguments[functionIndex] = functionCallArguments[functionIndex] + " " + token[x - 1]
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        functionDeclaration[functionIndex] = functionDeclaration[functionIndex] + " " + token[x - 1]

        k = 0
        m = 0
        mc = 0
        ch = 0
        for v in vars:  # check for duplicate declared variables and with scope
            if token[x-1] in v:
                if "global" not in varsScope[k] and varsScope[k] not in functionName: #may not work
                    ch = 1
                    continue
                if "global" in varsScope[k]:
                    m = k
                    mc = 1
                    break
            k += 1

        currentScope = 1
        if not varsScope:
            ch = 1
        if ch == 0 and "global" in varsScope[m] and mc == 1:
            variableDeclaration.append(token[x - 2] + " " + token[x - 1] + " global 0")
            vars.append(token[x-1])
            variableType.append(token[x - 2])
            varsScope.append("global")
            varsScopeBlock.append(0)

        else:
            variableDeclaration.append(token[x - 2] + " " + token[x - 1] + " " + str(functionName) + " " + str(currentScope))
            vars.append(token[x-1])
            variableType.append(token[x - 2])
            varsScope.append(functionName)
            varsScopeBlock.append(currentScope)

        currentScope = 0

        if "[" in token[x]:
            x += 1  # Accept [
            if "]" in token[x]:
                x += 1  # Accept ]
                return
            else:
                print("REJECT")
                exit(0)
        else:
            return
    else:
        if "void" in token[x-1]:
            return
        else:
            print("REJECT")
            exit(0)


def compoundStatement():  # 12
    global x, currentScope
    if "{" in token[x]:
        x += 1  # Accept {
        currentScope += 1
    else:
        return

    localDeclarations()
    statementList()

    if "}" in token[x]:
        x += 1  # Accept }
    else:
        print("REJECT")
        exit(0)


def localDeclarations():  # 13
    localDeclarationsPrime()


def localDeclarationsPrime():  # 14
    if token[x] in miniKeywords:
        theVariableDeclaration()
        localDeclarationsPrime()
    else:
        return


def statementList():  # 15
    statementListPrime()


def statementListPrime():  # 16
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        statement()
        statementListPrime()
    elif z is True:
        statement()
        statementListPrime()
    elif token[x] in miniKeywordsTwo:
        statement()
        statementListPrime()
    elif "}" in token[x]:
        return
    else:
        return


def statement():  # 17
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        expressionStatement()
    elif z is True:
        expressionStatement()
    elif "(" in token[x] or ";" in token[x]:
        expressionStatement()
    elif "{" in token[x]:
        compoundStatement()
    elif "if" in token[x]:
        selectionStatement()
    elif "while" in token[x]:
        iterationStatement()
    elif "return" in token[x]:
        returnStatement()
    else:
        print("REJECT")
        exit(0)


def expressionStatement():  # 18
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accept ;
        else:
            print("REJECT")
            exit(0)
    elif z is True:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accept ;
        else:
            print("REJECT")
            exit(0)
    elif "(" in token[x]:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accept ;
        else:
            print("REJECT")
            exit(0)
    elif ";" in token[x]:
        x += 1  # Accept ;
    else:
        print("REJECT")
        exit(0)


def selectionStatement():  # 19
    global x
    if "if" in token[x]:
        x += 1  # Accept if
    else:
        return

    if "(" in token[x]:
        x += 1  # Accept (
    else:
        print("REJECT")
        exit(0)

    expressionPrime()
    if ")" in token[x]:
        x += 1  # Accept )
    else:
        print("REJECT")
        exit(0)
    statement()
    if "else" in token[x]:
        x += 1  # Accept else
        statement()
    else:
        return


def iterationStatement():  # 20
    global x
    if "while" in token[x]:
        x += 1  # Accept while
    else:
        return

    if "(" in token[x]:
        x += 1  # Accept (
    else:
        print("REJECT")
        exit(0)

    expressionPrime()

    if ")" in token[x]:
        x += 1  # Accept )
    else:
        print("REJECT")
        exit(0)

    statement()


def returnStatement():  # 21
    global x, expressionReturn, expressionType, functionReturn
    if "return" in token[x]:
        x += 1  # Accept return
        if "int" in functionType:
            functionReturn = 1
        else:
            functionReturn = 1
    else:
        return
    w = token[x].isalpha()
    z = hasnum(token[x])
    if ";" in token[x]:
        x += 1  # Accept ;
        if "void" not in functionType:  # check if int or float function does not return a value
            print("REJECT")
            exit(0)
        return
    elif token[x] not in keywords and w is True:
        if "void" in functionType:  # check if void has return with value
            print("REJECT")
            exit(0)

        if "int" in functionType:
            expressionType = "int"
        else:
            expressionType = "float"
        expressionReturn = 1
        expressionPrime()
        expressionReturn = 0

        if ";" in token[x]:
            x += 1  # Accept ;
            return
        else:
            print("REJECT")
            exit(0)
    elif z is True:
        if "void" in functionType:  # check if void has return with value
            print("REJECT")
            exit(0)

        if "int" in functionType:
            expressionType = "int"
        else:
            expressionType = "float"
        expressionReturn = 1

        expressionPrime()
        expressionReturn = 0
        if ";" in token[x]:
            x += 1  # Accept ;
            return
        else:
            print("REJECT")
            exit(0)
    elif "(" in token[x]:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accept ;
            return
        else:
            print("REJECT")
            exit(0)
    else:
        print("REJECT")
        exit(0)


def expressionPrime():  # 22
    global x, expressionType, rightExpression, leftExpression, expressionReturn, matchParameter, theParameter
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        if theParameter == 1:
            o = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v in token[x-1]:
                    check = variableType[o]
                o += 1
            matchParameter = matchParameter + " " + check

        if leftExpression == 1 and theParameter == 0:
            if "(" in token[x]:
                o = 0
                check = 0
                for v in functionNames:  # get the type of the function for operand/operator checking
                    if v in token[x-1]:
                        check = functionTypes[o]
                    o += 1
                if expressionType != check:
                    print("REJECT")
                    exit(0)

            else:
                o = 0
                ch = 0
                check = 0
                for v in vars:  # check variable before checking if operator/operand agree
                    if v in token[x-1]:
                        if "global" not in varsScope[o] and varsScope[o] not in functionName:
                            ch = 1
                        if varsScope[o] in functionName:
                            ch = 0
                            check = variableType[o]
                            break
                        check = variableType[o]
                    o += 1
                if ch == 1:
                    print("REJECT")
                    exit(0)
                if expressionType != check:
                    print("REJECT")
                    exit(0)

        if rightExpression == 1:
            o = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v in token[x-1]:
                    check = variableType[o]
                o += 1
            if expressionType not in check:
                print("REJECT")
                exit(0)

        if expressionReturn == 1:
            o = 0
            check = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v in token[x-1]:
                    check = variableType[o]
                o += 1
            if expressionType not in check:
                print("REJECT")
                exit(0)

        if "(" in token[x] and leftExpression == 0 and theParameter == 0:
            if token[x-1] not in functionNames:
                print("REJECT")
                exit(0)

        ch = 0
        k = 0
        for v in vars:  # check for duplicate declared variables
            if v in token[x-1]:
                if functionName not in varsScope[k] and "global" not in varsScope[k]:
                    ch = 1
                if functionName in varsScope[k]:
                    ch = 0
            k += 1

        if token[x-1] not in vars and "(" not in token[x]:
            print("REJECT")
            exit(0)

        if ch == 1:
            print("REJECT")
            exit(0)

        expression()

    elif "(" in token[x]:
        x += 1  # Accept (
        expressionPrime()
        if ")" in token[x]:
            x += 1  # Accept )
            termPrime()
            addExpressionPrime()
            if token[x] in comparisionSymbols:
                simpleExpressionPrime()
            elif token[x] in additionSubtractionSymbols:
                addExpressionPrime()
                if token[x] in comparisionSymbols:
                    simpleExpressionPrime()
            elif token[x] in comparisionSymbols:
                simpleExpressionPrime()
        else:
            print("REJECT")
            exit(0)
    elif z is True:
        x += 1  # Accept NUM/FLOAT
        if theParameter == 1:
            if "." in token[x-1]:
                matchParameter = matchParameter + " float"
            elif "E" in token[x-1]:
                matchParameter = matchParameter + " float"
            else:
                matchParameter = matchParameter + " int"

        ch = 0
        if "." in token[x-1]:
            ch = 1
        if "E" in token[x-1]:
            ch = 1

        if expressionReturn == 1 and ch == 1:
            if "float" not in expressionType:
                print("REJECT")
                exit(0)

        if expressionReturn == 1 and ch == 0:
            if "int" not in expressionType:
                print("REJECT")
                exit(0)

        if rightExpression == 1 and "E" in token[x - 1]:
            print("REJECT")
            exit(0)
        if rightExpression == 1 and "." in token[x - 1]:
            print("REJECT")
            exit(0)

        if leftExpression == 1:
            if ch != 1 and "float" in expressionType:
                if "." not in token[x+1] and "E" not in token[x+1]:
                    print("REJECT")
                    exit(0)

        termPrime()
        addExpressionPrime()
        if token[x] in comparisionSymbols:
            simpleExpressionPrime()
        elif token[x] in additionSubtractionSymbols:
            addExpressionPrime()
            if token[x] in comparisionSymbols:
                simpleExpressionPrime()
        elif token[x] in comparisionSymbols:
            simpleExpressionPrime()
    else:
        print("REJECT")
        exit(0)


def expression():  # 22X
    global x, expressionType, rightExpression, leftExpression, theParameter, matchParameter
    if "=" in token[x]:
        x += 1  # Accept =
        k = 0
        for v in vars:  # find the type of the first ID for the exp
            if token[x-2] == v:
                expressionType = variableType[k]
                leftExpression = 1
            k += 1
        expressionPrime()
        leftExpression = 0
    elif "[" in token[x]:
        x += 1  # Accept [
        expressionType = "int"
        rightExpression = 1
        expressionPrime()
        rightExpression = 0
        if "[" in token[x-1]:
            print("REJECT")
            exit(0)
        if "]" in token[x]:
            x += 1  # Accept ]
            if "=" in token[x]:
                x += 1  # Accept =
                expressionPrime()
            elif token[x] in multiplicationDivisionSymbols:
                termPrime()
                addExpressionPrime()
                if token[x] in comparisionSymbols:
                    simpleExpressionPrime()
            elif token[x] in additionSubtractionSymbols:
                addExpressionPrime()
                if token[x] in comparisionSymbols:
                    simpleExpressionPrime()
            elif token[x] in comparisionSymbols:
                simpleExpressionPrime()
        else:
            print("REJECT")
            exit(0)
    elif "(" in token[x]:
        x += 1  # Accept (
        k = 0
        for v in functionNames:
            if v in token[x-2]:
                break
            k += 1
        arguments()
        theParameter = 0
        u = 0
        if not matchParameter:
            u = 1
        if u == 0 and matchParameter not in functionCallArguments[k]:
            print("REJECT")
            exit(0)

        if ")" in token[x]:
            x += 1  # Accept )
            if token[x] in multiplicationDivisionSymbols:
                termPrime()
                addExpressionPrime()
                if token[x] in comparisionSymbols:
                    simpleExpressionPrime()
            elif token[x] in additionSubtractionSymbols:
                addExpressionPrime()
                if token[x] in comparisionSymbols:
                    simpleExpressionPrime()
            elif token[x] in comparisionSymbols:
                simpleExpressionPrime()
        else:
            print("REJECT")
            exit(0)
    elif token[x] in multiplicationDivisionSymbols:
        termPrime()
        addExpressionPrime()
        if token[x] in comparisionSymbols:
            simpleExpressionPrime()
    elif token[x] in additionSubtractionSymbols:
        addExpressionPrime()
        if token[x] in comparisionSymbols:
            simpleExpressionPrime()
    elif token[x] in comparisionSymbols:
        simpleExpressionPrime()


def variable():  # 23
    global x
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
    else:
        return
    if "[" in token[x]:
        x += 1  # Accept [
        expressionPrime()
        if "]" in token[x]:
            x += 1  # Accept ]
        else:
            print("REJECT")
            exit(0)
    else:
        return


def simpleExpression():  # 24
    addExpression()
    simpleExpressionPrime()

def simpleExpressionPrime():
    if token[x] in comparisionSymbols:
        comparisonOperation()
        addExpression()
    else:
        return


def comparisonOperation():  # 25
    global x
    if token[x] in comparisionSymbols:
        x += 1  # Accept <=, <, >, >=, ==, or !=
    else:
        return


def addExpression():  # 26
    term()
    addExpressionPrime()


def addExpressionPrime():  # 27
    if token[x] in additionSubtractionSymbols:
        additiveOperation()
        term()
        addExpressionPrime()
    else:
        return


def additiveOperation():  # 28
    global x
    if token[x] in additionSubtractionSymbols:
        x += 1  # Accept +, -
    else:
        return


def term():  # 29
    factor()
    termPrime()


def termPrime():  # 30
    if token[x] in multiplicationDivisionSymbols:
        multiplicativeOperation()
        factor()
        termPrime()
    else:
        return


def multiplicativeOperation():  # 31
    global x
    if token[x] in multiplicationDivisionSymbols:
        x += 1  # Accept *, /
    else:
        return


def factor():  # 32
    global x, leftExpression, expressionReturn
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID

        if leftExpression == 1:
            o = 0
            ch = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v in token[x-1]:
                    if "global" not in varsScope[o] and functionName not in varsScope[o]:
                        ch = 1
                    if functionName in varsScope[o]:
                        ch = 0
                        check = variableType[o]
                        break
                    check = variableType[o]
                o += 1
            if expressionType not in check:
                print("REJECT")
                exit(0)
            if ch == 1:
                print("REJECT")
                exit(0)

        if expressionReturn == 1:
            o = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v in token[x-1]:
                    check = variableType[o]
                o += 1
            if expressionType not in check:
                print("REJECT")
                exit(0)


        if "[" in token[x]:
            x += 1  # Accept [
            expressionPrime()
            if "]" in token[x]:
                x += 1  # Accept ]
            else:
                return
        elif "(" in token[x]:
            x += 1  # Accept (
            arguments()
            if ")" in token[x]:
                x += 1  # Accept )
            else:
                return
        else:
            return
    elif z is True:
        x += 1  # Accept NUM/FLOAT
    elif "(" in token[x]:
        x += 1  # Accept (
        expressionPrime()
        if ")" in token[x]:
            x += 1  # Accept )
        else:
            return
    else:
        print("REJECT")
        exit(0)


def factorPrime():  # 33
    global x
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        if "(" in token[x]:
            x += 1  # Accept (
            arguments()
            if ")" in token[x]:
                x += 1  # Accept )
            else:
                print("REJECT")
                exit(0)
        else:
            print("REJECT")
            exit(0)
    else:
        return


def arguments():  # 34
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        argumentsList()
    elif z is True:
        argumentsList()
    elif "(" in token[x]:
        argumentsList()
    elif ")" in token[x]:
        return
    else:
        return


def argumentsList():  # 35
    global matchParameter, theParameter
    theParameter = 1
    matchParameter = ""
    expressionPrime()
    argumentsListPrime()


def argumentsListPrime():  # 36
    global x
    if "," in token[x]:
        x += 1  # Accept ,
        expressionPrime()
        argumentsListPrime()
    elif ")" in token[x]:
        return
    else:
        return


# ----------------------------- end of parsing functions --------------------------------- #

# begin parsing
programDeclaration()

print(variableDeclaration)
print(functionDeclaration)

if checkMain == 1 and checkFinalMain == 1:  # check if contains 1 main function
    print("ACCEPT")
else:
    print("REJECT")