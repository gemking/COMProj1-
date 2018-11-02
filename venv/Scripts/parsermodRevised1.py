import sys
import re
with open(sys.argv[1], "r") as file: #opens file
    filelines = file.read().splitlines() # reads file and splits lines
    file.close() #closes file


insideComment = 0
keywords = ["if", "else", "while", "int", "float", "void", "return"] #denotes all keywords
symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]" #denotes symbols used
comparisonSymbols = "<" or "<=" or  ">" or ">=" or "==" or"!=" #holds relational operations
addSubtractSymbols = "+" or "-" #holds addition and subtraction operations
multiplyDivideSymbols = "*" or "/" #holds multiplication and division operations
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

token.append("$")  #appended to determine when the program is done programming
checkMain = 0 #checks if there is 1 main function
checkLastMain = 0 #check if the last function is main
finished = 0
exception0 = 0
exception1 = 0
exceptionReturn = 0
parameterMatch = 0
parameter  = 0

variableDeclaration = [] #list which holds declared scope, type, and variables
variableType = [] #list that holds the type of variables
variableOperation = [] #checks for operator and operand agreement
vars = [] #list to hold all of the declared variables
varsScope = [] #list of all variable scopes
varsScopeBlock = [] #list of all variable scopes in bllock number
functionDeclaration =[] #list to hold declared functions with parms/arguments
functionIndex = 0 #index to keep track of apramters/arguments
functionCall = [] #functions called
functionCallArguments = [] #list of argument types in a function's paramters
functionNames = [] #list of all function names
functionTypes = [] #list of all function types
functionName = 0 #function name for scope
functionType = 0 #function type and sees if ti needs return
currentScope = 0 #current scope
functionReturn = 0 # does function have a return?
functionReturnIntFloat = 0 #check if int/float function has return

                 # ----- beginning of parser ----- #

def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def programDeclaration(): #runs program(Rule 1)
    global completed
    declarationList()
    if "$" in token[x]:
        finished = 1 #continues outside
    else:
        print ("REJECT") #if not, Reject


def declarationList(): #Rule 2
    declaration()
    declarationListPrime()


def declarationListPrime(): #Rule 3
    if "int" in token[x] or "void" in token[x] or "float" in token[x]:
        declaration()
        declarationListPrime()
    elif "$" in token[x]:
        return
    else:
        return


def declaration(): #Rule 4
    global x
    global checkMain
    global checkLastMain
    global currentScope
    global functionName
    global functionType
    global functionReturn
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        if "main" in token[x]: #if main is in the file
            checkMain += 1
            checkLastMain += 1
        if token[x-1] != "void": #if void is not in the file
            print("REJECT")
            exit(0)
        else:
            checkLastMain = 0

        x += 1  # Accepts ID
        if ";" in token[x]:
            x += 1  # Accepts ;
            m = 0
            for duplicates in vars: #checking for duplicates of declared variables
                if duplicates in token[x-2]:
                    if variableType in token[x-3]:
                        print("REJECT")
                        exit(0)
                m += 1

            variableDeclaration.append(token[x-3] + " " + token[x-2] + " global 0")
            vars.append(token[x-2])
            variableType.append(token[x-3])
            varsScope.append("global")
            varsScopeBlock.append(0)

            if "void" in token[x-3]:
                print("REJECT")
                exit(0)

        elif "[" in token[x]:
            x += 1  # Accepts [
            m = 0
            for duplicates in vars: #checking for duplicates of declared variables
                if duplicates in token[x-2]:
                    if variableType in token[x-3]:
                        print("REJECT")
                        exit(0)
                m += 1

                variableDeclaration.append(token[x - 3] + " " + token[x - 2] + " global 0")
                vars.append(token[x - 2])
                variableType.append(token[x - 3])
                varsScope.append("global")
                varsScopeBlock.append(0)

                if "void" in token[x-3]:
                    print("REJECT")
                    exit(0)

            z = hasnum(token[x])
            if z is True:
                x += 1  # Accepts NUM/FLOAT
                declarationPrime()
                if "]" in token[x]:
                    x += 1  # Accepts ]
                    if ";" in token[x]:
                        x += 1  # Accepts ;
                    else:
                        print("REJECT")
                        exit(0)
                else:
                    print("REJECT")
                    exit(0)
            else:
                print("REJECT")
                exit(0)

def declarationPrime(): #Rule 5
    global x
    typeSpecifier()
    #variableDeclaration()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
    else:
        return

    if "(" in token[x]:
        x += 1  # Accepts (
        for duplicates in functionDeclaration:  # check if there is duplicates of declared functions
            if duplicates in token[x - 2]:
                print("REJECT")
                exit(0)
        functionDeclaration.append(token[x - 3] + " " + token[x - 2])
        functionName = token[x - 2]
        functionNames.append(token[x - 2])
        functionTypes.append(token[x - 3])
        functionType = token[x - 3]
        functionReturn = 0
        currentScope = 0

        parameters()

        if ")" in token[x]:
            x += 1 #Accepts )
            compoundStatement()

            if 0 in functionReturn and "int" in functionType:
                print ("REJECT")
                exit(0)
            elif 0 in functionReturn and "float" in functionType:
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

def variableDeclaration(): #Rule 6
    global x
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
        m = 0
        for duplicates in vars: #check for duplicated declared variables
            if duplicates in token[x-1]:
                if functionName in varsScope[m]:
                    if currentScope <= varsScopeBlock[m]:
                        print ("REJECT")
                        exit(0)

            m += 1
        variableDeclaration.append(token[x-2] + " " + token[x-1] + " " + str(functionName) + " " + str(currentScope))
        vars.append(token[x-1])
        variableType.append(token[x-2])
        varsScope.append(functionName)
        varsScopeBlock.append(currentScope)

        if "void" in token[i-2]: # check if ID is type void
            print("REJECT")
            exit(0)
    else:
        print("REJECT")
        exit(0)

    variableDeclarationPrime()

def variableDeclarationPrime(): #Rule 7
    global x
    if ";" in token[x]:
        x += 1  # Accepts ;
    elif "[" in token[x]:
        x += 1  # Accepts [
        w = hasnum(token[x])
        if w is True:
            x += 1  # Accepts NUM/FLOAT
            if "." in token[x-1]: # check for float in the array declaration
                print("REJECT")
                exit(0)
            if "E" in token[x-1]: #check for float in the array declaration
                print("REJECT")
                exit(0)

            if "]" in token[x]:
                x += 1  # Accepts ]
                if ";" in token[x]:
                    x += 1  # Accepts ;
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

# checking to see if in keyword throws an error during the execution of the program

def typeSpecifier(): #Rule 8
    global x
    if "int" in token[x] or "void" in token[x] or "float" in token[x]:
        x += 1  # Accepts int/void/float
    else:
        return



def parameter(): #Rule 9
    global x
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
    else:
        return

    parameterPrime()

def parameterPrime(): #Rule 10
    global x
    global currentScope
    global functionName
    typeSpecifier()
    functionDeclaration[functionIndex] - functionDeclaration[functionIndex] + " " + token[x-1]
    functionCallArguments.append("")
    functionCallArguments[functionIndex] = functionCallArguments[functionIndex] + " " + token[x-1]
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1 #Accepts ID
        functionDeclaration[functionIndex] = functionDeclaration[functionIndex] + " " + token[x-1]

        m = 0
        g = 0
        gh = 0
        cz = 0
        for duplicates in vars: #check for duplicate declared variables and with scope
            if duplicates in token[x-1]:
                if "global" not in varsScope[m] and functionName not in varsScope[m]: #may not work
                    cz = 1
                    continue
                if "global" in varsScope[m]:
                    m = g
                    gh = 1
                    break
            m += 1

        currentScope = 1
        if not varsScope:
            cz = 1
        if 0 in cz and "global" in varsScope[m] and 1 in gh:  #may not work
            variableDeclaration.append(token[x-2] + " " + token[x-1] + " global 0")
            vars.append(token[x-1])
            vartype.append(token[x-2])
            varsScope.append("global")
            varsScopeBlock.append(0)
        else:
            variableDeclaration.append(token[i-2] + " " + token[i-1] + " " + str(functionName) + " " + str(currentScope))
            vars.append(token[i-1])
            variableType.append(token[i-2])
            varsScope.append(functionName)
            varsScopeBlock.append(currentScope)

        currentScope = 0


        if "[" in token[x]:
            x += 1  # Accepts [
            if "]" in token[x]:
                x += 1  # Accepts ]
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

def parameters(): #Rule 11
    global x
    global functionIndex
    if "int" in token[x] or "float" in token[x]:
        parametersList()
    elif "void" in token[x]:
        x += 1  # Accepts void
        parametersPrime()
        functionIndex += 1
    else:
        print("REJECT")
        exit(0)



def parametersPrime(): #Rule 12
    global x
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
        parameterPrime()
        parametersListPrime()
    else:
        return




def parametersList(): #Rule 13
    parameter()
    parametersListPrime()


def parametersListPrime(): #Rule 14
    global x
    if "," in token[x]:
        x += 1  # Accepts ,
        parameter()
        parametersListPrime()
    elif  ")" in token[x]:
        return
    else:
        return





def compoundStatement(): #Rule 15
    global x
    if "{" in token[x]:
        x += 1  # Accepts {
        currentScope += 1
    else:
        return

    localDeclarations()
    statementList()

    if "}" in token[x]:
        x += 1  # Accepts }
    else:
        print("REJECT")
        exit(0)


def localDeclarations(): #Rule 16
    localDeclarationsPrime()


def localDeclarationsPrime(): #Rule 17
    if token[x] == "void" or token[x] == "float" or token[x] == "int":
        variableDeclaration()
        localDeclarationsPrime()
    else:
        return


def statementList(): #Rule 18
    statementListPrime()


def statementListPrime(): #Rule 19
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        statement()
        statementListPrime()
    elif z is True:
        statement()
        statementListPrime()
    elif "(" in token[x] or ";" in token[x] or "{" in token[x] or "if" in token[x] or "while" in token[x] or "return" in token[x]:
        statement()
        statementListPrime()
    elif "}" in token[x]:
        return
    else:
        return


def statement(): #Rule 20
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


def expressionStatement(): #Rule 21
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accepts ;
        else:
            print("REJECT")
            exit(0)
    elif z is True:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accepts ;
        else:
            print("REJECT")
            exit(0)
    elif "(" in token[x]:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accepts ;
        else:
            print("REJECT")
            exit(0)
    elif ";" in token[x]:
        x += 1  # Accepts ;
    else:
        print("REJECT")
        exit(0)


def selectionStatement(): #Rule 22
    global x
    if "if" in token[x]:
        x += 1  # Accepts if
    else:
        return

    if "(" in token[x]:
        x += 1  # Accepts (
    else:
        print("REJECT")
        exit(0)

    expressionPrime()

    if ")" in token[x]:
        x += 1  # Accepts )
    else:
        print("REJECT")
        exit(0)

    statement()
    selectionStatementPrime()


def selectionStatementPrime(): #Rule 23
    global x
    if "else" in token[x]:
        x += 1  # Accepts else
        statement()
    else:
        return


def iterationStatement(): #Rule 24
    global x
    if "while" in token[x]:
        x += 1  # Accepts while
    else:
        return

    if "(" in token[x]:
        x += 1  # Accepts (
    else:
        print("REJECT")
        exit(0)

    expressionPrime()

    if ")" in token[x]:
        x += 1  # Accepts )
    else:
        print("REJECT")
        exit(0)

    statement()


def returnStatement(): #Rule 25
    global x
    global functionReturn
    if "return" in token[x]:
        x += 1  # Accepts return
        if "int" in functionType:
            functionReturn = 1
        else:
            functionReturn = 1
    else:
        return
    returnStatementPrime()


def returnStatementPrime(): #Rule 26
    global x
    global functionReturn
    global exceptionReturn
    global expressionType
    w = token[x].isalpha()
    z = hasnum(token[x])
    if ";" in token[x]:
        x += 1  # Accepts ;
        if "void" not in functionType: #may not work; check if int or float function does not return value
            print("REJECT")
            exit(0)
        return
    elif token[x] not in keywords and w is True:
        if "void" in functionType: #Check if void has return with value
            print("REJECT")
            exit(0)

        if "int" in functionType:
            expressionType = "int"
        else:
            expressionType = "float"
        exceptionReturn = 1
        expressionPrime()
        exceptionReturn = 0

        if ";" in token[x]:
            x += 1  # Accepts ;
            return
        else:
            print("REJECT")
            exit(0)
    elif z is True:
        if "void" in functionType: # check if void has return with value
            print("REJECT")
            exit(0)

        if "int" in functionType:
            expressionType = "int"
        else:
            expressionType = "float"
        exceptionReturn = 1
        expressionPrime()
        exceptionReturn = 0
        if ";" in token[x]:
            x += 1  # Accepts ;
            return
        else:
            print("REJECT")
            exit(0)
    elif "(" in token[x]:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accepts ;
            return
        else:
            print("REJECT")
            exit(0)
    else:
        print("REJECT")
        exit(0)




def expression(): #Rule 27
    global x
    global exception0
    global exception1
    global expressionType
    global parameter
    global parameterMatch
    if "=" in token[x]:
        x += 1  # Accepts =
        m = 0
        for duplicates in vars: #find the type of the first ID for the expression
            if v in token[x-2]:
                expressionType = variableType[m]
                exception0 = 1
            k += 1
        expressionPrime()
        exception0 = 0
    elif "[" in token[x]:
        x += 1  # Accepts [
        expressionType = "int"
        exception1 = 1
        expressionPrime()
        exception1 = 0
        if "[" in token[x-1]:
            print("REJECT")
            exit(0)
        if "]" in token[x]:
            x += 1  # Accepts ]
            if "=" in token[x]:
                x += 1  # Accepts =
                expressionPrime()
            elif multiplyDivideSymbols in token[x]:
                termPrime()
                addExpressionPrime()
                simpleExpressionPrime()
            elif addSubtractSymbols in token[x]:
                addExpressionPrime()
                if comparisonSymbols in token[x]:
                    comparisonOperation()
                    addExpression()
            elif comparisonSymbols in token[x]:
                comparisonOperation()
                addExpression()
            else:
                return
        else:
            print("REJECT")
            exit(0)
    elif "(" in token[x]:
        x += 1  # Accepts (
        m = 0
        for duplicates in functionNames:
            if token[i-2] in v:
                break
            m += 1
        arguments()
        parameter = 0
        r = 0
        if not parameterMatch:
            r = 1
        if 0 in r and  parameterMatch not in functionCallArguments[m]:
            print("REJECT")
            exit(0)
        if ")" in token[x]:
            x += 1  # Accepts )
            if multiplyDivideSymbols in token[x]:
                termPrime()
                addExpressionPrime()
                simpleExpressionPrime()
            elif addSubtractSymbols in token[x]:
                addExpressionPrime()
                if comparisonSymbols in token[x]:
                    comparisonOperation()
                    addExpression()
            elif comparisonSymbols in token[x]:
                comparisonOperation()
                addExpression()
            else:
                return
        else:
            print("REJECT")
            exit(0)
    elif multiplyDivideSymbols in token[x]:
        termPrime()
        addExpressionPrime()
        simpleExpressionPrime()
        # error begins
    elif addSubtractSymbols in token[x]:
        addExpressionPrime()
        simpleExpressionPrime()
    elif comparisonSymbols in token[x]:
        comparisonOperation()
        addExpression()
    else:
        return


def expressionPrime(): #Rule 28
    global x
    global expressionType
    global exception0
    global exception1
    global exceptionReturn
    global parameterMatch
    global parameter
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
        if 1 in parameter:
            q = 0
            for duplicates in vars: #get the type of the var for operand/operator checking
                if token[x-1] in duplicates:
                    check = variableType[q]
                q += 1
            parameterMatch = parameterMatch + " " + check
        if 1 in exception0 and 0 in parameter:
            if "(" in token[x]:
                q = 0
                check = 0
                for duplicates in functionNames: #get the type of the function for operand/operator checking
                    if token[x-1] in v:
                        check = functionTypes[q]
                    q += 1
                if check not in expressionType:
                    print("REJECT")
                    exit(0)
                if 1 in exceptionReturn:
                    q = 0
                    check = 0
                    for duplicates in vars: #get the type of the var for operand/operator checking
                        if token[x-1] in duplicates:
                            check = variableType[q]
                        q += 1
                    if check not in expressionType:
                        print("REJECT")
                        exit(0)

                    if "(" in token[x] and 0 in exceptionReturn and 0 in parameter:
                        if token[x-1] not in functionNames:
                            print("REJECT")
                            exit(0)

                    cz = 0
                    m = 0
                    for duplicates in vars: #check for duplicate declared variables
                        if v in token[x-1]:
                            if functioName not in varsScope[m] and "global" not in varsScope[m]:
                                cz = 1
                            if functionName in varsScope[m]:
                                cz = 0
                        m += 1
                    if token[x-1] not in vars and "(" not in token[x]:
                        print("REJECT")
                        exit(0)
                    if 1 in cz:
                        print("REJECT")
                        exit(0)

                    expression()

    elif "(" in token[x]:
        x += 1  # Accepts (
        expressionPrime()
        if ")" in token[x]:
            x += 1  # Accepts )
            termPrime()
            addExpressionPrime()
            if comparisonSymbols in token[x]:
                comparisonOperation()
                addExpression()
            elif addSubtractSymbols in token[x]:
                addExpressionPrime()
                if comparisonSymbols in token[x]:
                    comparisonOperation()
                    addExpression()
            elif comparisonSymbols in token[x]:
                comparisonOperation()
                addExpression()
            else:
                return
        else:
            print("REJECT")
            exit(0)
    elif z is True:
        x += 1  # Accepts NUM/FLOAT
        if 1 in parameter:
            if "." in token[x-1]:
                parameterMatch = parameterMatch + " float"
            elif "E" in token[x-1]:
                parameterMatch = parameterMatch + "float"
            else:
                parameterMatch = parameterMatch + " int"

            cz = 0
            if "." in token[x-1]:
                cz = 1
            if "E" in token[x-1]:
                cz = 1

            if 1 in exceptionReturn and 1 in cz:
                if "float" not in expressionType:
                    print("REJECT")
                    exit(0)
            if 1 in exceptionReturn and 0 in cz:
                if "int" not in expressionType:
                    print("REJECT")
                    exit(0)
            if 1 in exception1 and "E" in token[x-1]:
                print("REJECT")
                exit(0)
            if 1 in exception1 and "." in token[x-1]:
                print("REJECT")
                exit(0)

            if 1 in exception0:
                if 1 is not cz and "float" in expressionType:
                    if "." not in token[x-1] and "E" not in token[x+1]:
                        print("REJECT")
                        exit(0)
        termPrime()
        addExpressionPrime()
        if comparisonSymbols in token[x]:
            comparisonOperation()
            addExpression()
        elif addSubtractSymbols in token[x]:
            addExpressionPrime()
            if comparisonSymbols in token[x]:
                comparisonOperation()
                addExpression()
        elif comparisonSymbols in token[x]:
                comparisonOperation()
                addExpression()
        else:
            return
    else:
        print("REJECT")
        exit(0)



def variable(): #Rule 29
    global x
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
    else:
        return
    variablePrime()

def variablePrime(): #Rule 30
    if "[" in token[x]:
        x += 1  # Accepts [
        expressionPrime()
        if "]" in token[x]:
            x += 1  # Accepts ]
        else:
            print("REJECT")
            exit(0)
    else:
        return


def simpleExpression(): #Rule 31
    addExpression()
    simpleExpressionPrime()


def simpleExpressionPrime(): #Rule 32
    if comparisonSymbols in token[x]:
        comparisonOperation()
        addExpression()
    else:
        return


def comparisonOperation(): #Rule 33
    global x
    if comparisonSymbols in token[x]:
        x += 1  # Accepts <=, <, >, >=, ==, or !=
    else:
        return


def addExpression(): #Rule 34
    term()
    addExpressionPrime()


def addExpressionPrime(): #Rule 35
    if addSubtractSymbols in token[x]:
        addOperation()
        term()
        addExpressionPrime()
    else:
        return


def addOperation(): #Rule 36
    global x
    if addSubtractSymbols in token[x]:
        x += 1  # Accepts +, -
    else:
        return


def term(): #Rule 37
    factor()
    termPrime()


def termPrime(): #Rule 38
    if multiplyDivideSymbols in token[x]:
        multiplyOperation()
        factor()
        termPrime()
    else:
        return


def multiplyOperation(): #Rule 39
    global x
    if multiplyDivideSymbols in token[x]:
        x += 1  # Accepts *, /
    else:
        return


def factor(): #Rule 40
    global x
    global exceptionReturn
    global exception0
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID

        if 1 in exceptionReturn:
            q = 0
            cz = 0
            for duplicates in vars: #get the type of the var for operand/operator checking
                if token[x-1] in v:
                    if "global" not in varsScope[q] and functionName not in varsScope[q]:
                        cz = 1
                    if functionName in varsScope[q]:
                        cz = 0
                        check = variableType[q]
                        break
                    check = variableType[q]
                q += 1
            if check not in expressionType:
                print("REJECT")
                exit(0)
            if 1 in cz:
                print("REJECT")
                exit(0)

        if 1 in exceptionReturn:
            q = 0
            for duplicates in vars: #get the type of the var for operand/operator checking
                if token[i-1] in duplicates:
                    check = variableType[q]
                q += 1
            if check not in expressionType:
                print("REJECT")
                exit(0)

        if "[" in token[x]:
            x += 1  # Accepts [
            expressionPrime()
            if "]" in token[x]:
                x += 1  # Accepts ]
            else:
                return
        elif "(" in token[x]:
            x += 1  # Accepts (
            arguments()
            if ")" in token[x]:
                x += 1  # Accepts )
            else:
                return
        else:
            return
    elif z is True:
        x += 1  # Accepts NUM/FLOAT
    elif "(" in token[x]:
        x += 1  # Accepts (
        expressionPrime()
        if ")" in token[x]:
            x += 1  # Accepts )
        else:
            return
    else:
        print("REJECT")
        exit(0)


def factorPrime(): #Rule 41
    global x
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
        if "(" in token[x]:
            x += 1  # Accepts (
            arguments()
            if ")" in token[x]:
                x += 1  # Accepts )
            else:
                print("REJECT")
                exit(0)
        else:
            print("REJECT")
            exit(0)
    else:
        return

    variablePrime()


def arguments(): #Rule 42
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


def argumentsList(): #Rule 43
    global parameter
    global parameterMatch
    parameterMatch = ""
    parmeter = 1
    expressionPrime()
    argumentslistPrime()


def argumentslistPrime(): #Rule 44
    global x
    if "," in token[x]:
        x += 1  # Accepts ,
        expressionPrime()
        argumentslistPrime()
    elif ")" in token[x]:
        return
    else:
        return


                        # ----- end of parser ------ #


programDeclaration() #Starts parsing the

print(variableDeclaration)
print(functionDeclaration)

if checkMain == 1 and checkLastMain == 1: #check if contains 1 main function
    print("ACCEPT")
else:
    print("REJECT")