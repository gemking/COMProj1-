import sys
import re

with open(sys.argv[1], "r") as file:  # opens file
    filelines = file.read().splitlines()  # reads file and splits lines
    file.close()  # closes file

insideComment = 0

keywords = ["if", "else", "while", "int", "float", "void", "return"]  # denotes all keywords
symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"  # denotes symbols used
comparisionSymbols = ["==", "<=", ">=", "!=", "<", ">"]
additionSubtractionSymbols = ["-", "+"]
multiplicationDivisionSymbols = ["/", "*"]
intFloatKeywords = ["int", "float"]
decimalExponentKeywords = [".", "E"]
leftParenthesesSemicolon = ["(", ";"]
miniKeywords = ["void", "int", "float"]
miniKeywordsTwo = ["while", "if", "return", "(", ";", "{"]
characters = "[a-zA-Z]+"  # obtains all words for the IDs
digits = "[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?"  # gets all decimal values, including integer values 0-9
errors = "\S"  # reports errors
token = []  # creates a list that holds all of the tokens
x = 0  # value that holds the token counter for the parser

for importantLines in filelines:  # receiving importantlines from filelines
    importantLine = importantLines  # sets importantLine to importantLines

    if not importantLine:
        continue  # if not an important line, it continues through the file

    list = "(%s)|(%s)|(%s)|(%s)" % (characters, digits, symbols, errors)  # puts entire library into a list of strings

    for word in re.findall(list, importantLine):  # finds list
        if re.match(characters, word[0]) and insideComment == 0:  # matches characters and makes sure insideComment is 0
            if word[0] in keywords:
                token.append(word[0])  # keyword is constructed out of characters a-zA-Z
            else:
                token.append(word[0])  # appends character values that are not keywords




        elif re.match(digits, word[1]) and insideComment == 0:  # matches digits and makes sure inside comment is 0
            if "." in word[1]:
                token.append(word[1])  # checks if value is a decimal value and appends
            elif "E" in word[1]:
                token.append(word[1])  # checks if value is an expontential value and appends
            else:
                token.append(word[1])  # appends integer value
        elif re.match(symbols, word[4]):  # matches symbols
            if "/*" in word[4]:  # Checks when word approaches /*
                insideComment = insideComment + 1  # increments insideComment if inside
            elif "*/" in word[4] and insideComment > 0:  # Checks when word approaches */
                insideComment = insideComment - 1  # decrements insideComment if outside
            elif "//" in word[4] and insideComment == 0:  # If neither
                break
            elif insideComment == 0:  # when inside counter is 0
                if "*/" in word[4]:  # when it reaches terminal */
                    if "*/*" in importantLine:  # when it's still sorting through comments
                        token.append("*")
                        insideComment += 1
                        continue  # skips comments and continue through the program
                    else:
                        token.append("*")  # appends multiplication symbol
                        token.append("/")  # appends division symbol
                else:
                    token.append(word[4])  # appends rest of symbols
        elif word[3] and insideComment == 0:  # matches errors and makes sure insideComment is 0
            token.append(word[3])  # appends error

            # ----- end of lexer ----- #

token.append("$")  # add to end to check if done parsing
leftExpression = 0
rightExpression = 0
expressionReturn = 0
theParameter = 0
matchParameter = 0
checkMain = 0  # checks if there is 1 main function
checkFinalMain = 0  # checks if the last function is main
isCompleted = 0

variableType = []  # holds type of variables
variableDeclaration = []  # holds declared variables, scope, and type
variableOperation = []  # checks for operation agreement
vars = []  # holds all declared variables
varsScope = []  # holds variable scope
varsScopeBlock = []  # holds block number of variable scope

functionType = 0  # holds function type and determine if it needs a return
functionTypes = []  # holds function types
functionName = 0  # holds function name for scoping purposes
functionNames = []  # holds function names
functionDeclaration = []  # list to hold decfunctionTypes = []  #holds function typeslared functions with parameters and arguments
functionIndex = 0  # index that keeps track of the parameters and arguments of a function
functionCall = []  # the functions that are called
functionCallArguments = []  # holds argument types in a function's parameters
currentScope = 0  # current scope
functionReturn = 0  # checks if the function is an int/float and if it has a return


# ----- beginning of semantic analyzing parser ----- #

def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def programDeclaration():  # runs the program(Rule 1)
    global isCompleted
    declarationList()
    if "$" in token[x]:
        isCompleted = 1  # continues
    else:
        print("REJECT")


def declarationList():  # Rule 2
    declaration()
    declarationListPrime()


def declarationListPrime():  # Rule 3
    if token[x] in miniKeywords:
        declaration()
        declarationListPrime()
    elif "$" in token[x]:
        return
    else:
        return


def declaration():  # Rule 4
    global x
    global checkMain
    global functionName
    global currentScope
    global functionType
    global functionReturn
    global checkFinalMain
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        if "main" in token[x]:
            checkMain += 1
            checkFinalMain = 1
            if "void" not in token[x - 1]:
                print("REJECT")
                exit(0)
        else:
            checkFinalMain = 0

        x += 1  # Accepts ID
        if ";" in token[x]:
            x += 1  # Accepts ;
            duplicateVariableCheck()
            variableAppend()
        elif "[" in token[x]:
            x += 1  # Accepts [
            duplicateVariableCheck()
            variableAppend()

            z = hasnum(token[x])
            if z is True:
                x += 1  # Accepts NUM/FLOAT
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

        elif "(" in token[x]:
            declarationPrime()


def declarationPrime():  # Rule 5
    global x
    global functionType
    global functionReturn
    typeSpecifier()

    if "(" in token[x]:
        x += 1  # Accepts (
        duplicateFunctionCheck()

        if ")" in token[x]:
            x += 1  # Accepts )
            compoundStatement()

            if functionReturn == 0 and functionType in intFloatKeywords:  # check if not funtype in "int"
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


def theVariableDeclaration():  # Rule 6
    global x
    global checkMain
    typeSpecifier()

    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
        s = 0
        for l in vars:  # checks for duplicates of declared variables
            if token[x - 1] in l:
                if varsScope[s] in functionName:
                    if currentScope <= varsScopeBlock[s]:
                        print("REJECT")
                        exit(0)
            s += 1

        variableFunctionScopeAppend()

        if "void" in token[x - 2]:  # checks if the ID is of type void
            print("REJECT")
            exit(0)
    else:
        print("REJECT")
        exit(0)

    variableDeclarationPrime()


def variableDeclarationPrime():  # Rule 7
    global x
    if ";" in token[x]:
        x += 1  # Accepts ;
    elif "[" in token[x]:
        x += 1  # Accepts [
        w = hasnum(token[x])
        if w is True:
            x += 1  # Accepts NUM/FLOAT
            if token[x - 1] in intFloatKeywords:
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


def typeSpecifier():  # Rule 8
    global x
    if token[x] in miniKeywords:
        x += 1  # Accepts int/void/float
    else:
        return


def parameter():  # Rule 9
    global x
    global checkMain
    typeSpecifier()

    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        if "main" in token[x]:
            checkMain += 1
        x += 1  # Accepts ID
    else:
        return

    if "(" in token[x]:
        x += 1  # Accepts (
    else:
        print("REJECT")
        exit(0)

    parameters()

    if ")" in token[x]:
        x += 1  # Accepts )
    else:
        print("REJECT")
        exit(0)

    compoundStatement()


def parameterPrime():  # Rule 10
    global x
    global currentScope
    global functionName
    typeSpecifier()
    functionDeclaration[functionIndex] = functionDeclaration[functionIndex] + " " + token[x - 1]
    functionCallArguments.append("")
    functionCallArguments[functionIndex] = functionCallArguments[functionIndex] + " " + token[x - 1]
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
        functionDeclaration[functionIndex] = functionDeclaration[functionIndex] + " " + token[x - 1]

        s = 0
        g = 0
        gh = 0
        dn = 0
        for l in vars:  # checks if there are duplicates of declared variables and their potential scope
            if token[x - 1] in l:
                if "global" not in varsScope[s] and varsScope[s] not in functionName:
                    dn = 1
                    continue
                if "global" in varsScope[s]:
                    g = s
                    gh = 1
                    break
            s += 1

        currentScope = 1
        if not varsScope:
            dn = 1
        if dn == 0 and "global" in varsScope[g] and gh == 1:
            variableAppendTwo()

        else:


            variableFunctionScopeAppend()

        currentScope = 0

        if "[" in token[x]:
            x += 1  # Accept [
            if "]" in token[x]:
                x += 1  # Accepts ]
                return
            else:
                print("REJECT")
                exit(0)
        else:
            return
    else:
        if "void" in token[x - 1]:
            return
        else:
            print("REJECT")
            exit(0)


def parameters():  # Rule 11
    global x
    global functionIndex
    if token[x] in intFloatKeywords:
        parameterPrime()
        parametersListPrime()
        functionIndex += 1
    elif "void" in token[x]:
        parametersPrime()
        functionIndex += 1
    else:
        print("REJECT")
        exit(0)


def parametersPrime():  # Rule 12
    global x
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        parameterPrime()
        parametersListPrime()
    else:
        return


def parametersList():  # Rule 13
    parameterPrime()
    parametersListPrime()


def parametersListPrime():  # Rule 14
    global x
    if "," in token[x]:
        x += 1  # Accepts ,
        parameterPrime()
        parametersListPrime()
    elif ")" in token[x]:
        return
    else:
        return


def compoundStatement():  # Rule 15
    global x
    global currentScope
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


def localDeclarations():  # Rule 16
    localDeclarationsPrime()


def localDeclarationsPrime():  # Rule 17
    if token[x] in miniKeywords:
        theVariableDeclaration()
        localDeclarationsPrime()
    else:
        return


def statementList():  # Rule 18
    statementListPrime()


def statementListPrime():  # Rule 19
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True or z is True or token[x] in miniKeywordsTwo:
        statement()
        statementListPrime()
    elif "}" in token[x]:
        return
    else:
        return


def statement():  # Rule 20
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True or z is True or token[x] in leftParenthesesSemicolon:
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


def expressionStatement():  # Rule 21
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True or z is True or "(" in token[x]:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accepts ;
        else:
            print("REJECT")
            exit(0)


def selectionStatement():  # Rule 22
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


def selectionStatementPrime():  # Rule 23
    global x
    if "else" in token[x]:
        x += 1  # Accepts else
        statement()
    else:
        return


def iterationStatement():  # Rule 24
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


def returnStatement():  # Rule 25
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


def returnStatementPrime():  # Rule 26
    global x
    global functionReturn
    global expressionReturn
    global expressionType
    w = token[x].isalpha()
    z = hasnum(token[x])
    if ";" in token[x]:
        x += 1  # Accepts ;
        if "void" not in functionType:  # checks if the int or float function does not return a value
            print("REJECT")
            exit(0)
        return
    elif token[x] not in keywords and w is True or z is True:
        checkVoidIntFloatInFunctionType()
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


def expression():  # Rule 27
    global x
    global expressionType
    global leftExpression
    global rightExpression
    global theParameter
    global matchParameter
    if "=" in token[x]:
        x += 1  # Accepts =
        s = 0
        for l in vars:  # finds the type of the first ID for the expression
            if l in token[x - 2]:
                expressionType = variableType[s]
                leftExpression = 1
            s += 1
        expressionPrime()
        leftExpression = 0
    elif "[" in token[x]:
        x += 1  # Accepts [
        expressionType = "int"
        rightExpression = 1
        expressionPrime()
        rightExpression = 0
        if "[" in token[x - 1]:
            print("REJECT")
            exit(0)
        if "]" in token[x]:
            x += 1  # Accepts ]
            if "=" in token[x]:
                x += 1  # Accepts =
                expressionPrime()
            elif token[x] in multiplicationDivisionSymbols:
                termPrime()
                addExpressionPrime()
            elif token[x] in additionSubtractionSymbols:
                addExpressionPrime()
            elif token[x] in comparisionSymbols:
                simpleExpressionPrime()
        else:
            print("REJECT")
            exit(0)
    elif "(" in token[x]:
        x += 1  # Accepts (
        s = 0
        for l in functionNames:
            if l in token[x - 2]:
                break
            s += 1
        arguments()
        theParameter = 0
        p = 0
        if not matchParameter:
            p = 1
        if p == 0 and functionCallArguments[s] != matchParameter:
            print("REJECT")
            exit(0)

        if ")" in token[x]:
            x += 1  # Accepts )
            if token[x] in multiplicationDivisionSymbols:
                termPrime()
                addExpressionPrime()
            elif token[x] in additionSubtractionSymbols:
                addExpressionPrime()
            elif token[x] in comparisionSymbols:
                simpleExpressionPrime()
        else:
            print("REJECT")
            exit(0)
    elif token[x] in multiplicationDivisionSymbols:
        termPrime()
        addExpressionPrime()
    elif token[x] in additionSubtractionSymbols:
        addExpressionPrime()
    elif token[x] in comparisionSymbols:
        simpleExpressionPrime()


def expressionPrime():  # Rule 28
    global x
    global expressionType
    global rightExpression
    global leftExpression
    global expressionReturn
    global matchParameter
    global theParameter
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        if theParameter == 1:
            q = 0
            for l in vars:  # gets the type of the var for operation agreement
                if l in token[x - 1]:
                    check = variableType[q]
                q += 1
            matchParameter = matchParameter + " " + check

        if leftExpression == 1 and theParameter == 0:
            if "(" in token[x]:
                q = 0
                check = 0
                for l in functionNames:  # gets the type of the function for operation agreement
                    if l in token[x - 1]:
                        check = functionTypes[q]
                    q += 1
                if check != expressionType:
                    print("REJECT")
                    exit(0)

            else:
                q = 0
                dn = 0
                check = 0
                for l in vars:  # checks variable before checking for operation agreement
                    if l in token[x - 1]:
                        if "global" not in varsScope[q] and varsScope[q] not in functionName:
                            dn = 1
                        if varsScope[q] in functionName:
                            dn = 0
                            check = variableType[q]
                            break
                        check = variableType[q]
                    q += 1
                if dn == 1:
                    print("REJECT")
                    exit(0)
                if expressionType != check:
                    print("REJECT")
                    exit(0)

        if rightExpression == 1:
            getVar()

        if expressionReturn == 1:
            check = 0
            getVar()

        if "(" in token[x] and leftExpression == 0 and theParameter == 0:
            if token[x - 1] not in functionNames:
                print("REJECT")
                exit(0)

        dn = 0
        s = 0
        for l in vars:  # checks for duplicates of declared variables
            if l in token[x - 1]:
                if functionName not in varsScope[s] and "global" not in varsScope[s]:
                    dn = 1
                if functionName in varsScope[s]:
                    dn = 0
            s += 1

        if token[x - 1] not in vars and "(" not in token[x]:
            print("REJECT")
            exit(0)

        if dn == 1:
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
            if token[x] in comparisionSymbols:
                simpleExpressionPrime()
            elif token[x] in additionSubtractionSymbols:
                addExpressionPrime()
        else:
            print("REJECT")
            exit(0)
    elif z is True:
        x += 1  # Accepts NUM/FLOAT
        if theParameter == 1:
            if "." in token[x - 1] or "E" in token[x - 1]:
                matchParameter = matchParameter + " float"
            else:
                matchParameter = matchParameter + " int"

        dn = 0
        if token[x - 1] in decimalExponentKeywords:
            dn = 1

        if expressionReturn == 1 and dn == 1:
            if "float" not in expressionType:
                print("REJECT")
                exit(0)

        if expressionReturn == 1 and dn == 0:
            if "int" not in expressionType:
                print("REJECT")
                exit(0)

        if rightExpression == 1 and token[x - 1] in decimalExponentKeywords:
            print("REJECT")
            exit(0)

        if leftExpression == 1:
            if dn != 1 and "float" in expressionType:
                if token[x + 1] not in decimalExponentKeywords:
                    print("REJECT")
                    exit(0)

        termPrime()
        addExpressionPrime()
        if token[x] in comparisionSymbols:
            simpleExpressionPrime()
        elif token[x] in additionSubtractionSymbols:
            addExpressionPrime()
    else:
        print("REJECT")
        exit(0)


def variable():  # Rule 29
    global x
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
    else:
        return
    variablePrime()


def variablePrime():  # Rule 30
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


def simpleExpression():  # Rule 31
    addExpression()
    simpleExpressionPrime()


def simpleExpressionPrime():  # Rule 32
    if token[x] in comparisionSymbols:
        comparisonOperation()
        addExpression()
    else:
        return


def comparisonOperation():  # Rule 33
    global x
    if token[x] in comparisionSymbols:
        x += 1  # Accepts <=, <, >, >=, ==, or !=
    else:
        return


def addExpression():  # Rule 34
    term()
    addExpressionPrime()


def addExpressionPrime():  # Rule 35
    if token[x] in additionSubtractionSymbols:
        additiveOperation()
        term()
        addExpressionPrime()
    else:
        return


def additiveOperation():  # Rule 36
    global x
    if token[x] in additionSubtractionSymbols:
        x += 1  # Accepts +, -
    else:
        return


def term():  # Rule 37
    factor()
    termPrime()


def termPrime():  # Rule 38
    if token[x] in multiplicationDivisionSymbols:
        multiplicativeOperation()
        factor()
        termPrime()
    else:
        return


def multiplicativeOperation():  # Rule 39
    global x
    if token[x] in multiplicationDivisionSymbols:
        x += 1  # Accepts *, /
    else:
        return


def factor():  # Rule 40
    global x
    global leftExpression
    global expressionReturn
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
        if leftExpression == 1:
            q = 0
            dn = 0
            check = variableType[q]
            for l in vars:  # get the type of the var for operation agreement
                if l in token[x - 1]:
                    if "global" not in varsScope[q] and functionName not in varsScope[q]:
                        dn = 1
                    if functionName in varsScope[q]:
                        dn = 0
                        check = variableType[q]
                        break
                    check = variableType[q]
                q += 1
            if expressionType not in check:
                print("REJECT")
                exit(0)
            if dn == 1:
                print("REJECT")
                exit(0)

        if expressionReturn == 1:
            q = 0
            check = variableType[q]
            for l in vars:  # gets the type of the var for operation agreement
                if l in token[x - 1]:
                    check = variableType[q]
                q += 1
            if expressionType not in check:
                print("REJECT")
                exit(0)

        if "[" in token[x]:
            x += 1  # Accepts [
            expressionPrime()
            if "]" in token[x]:
                x += 1  # Accept ]
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


def factorPrime():  # Rule 41
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


def arguments():  # Rule 42
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True or z is True or "(" in token[x]:
        argumentsList()
    elif ")" in token[x]:
        return
    else:
        return


def argumentsList():  # Rule 43
    global matchParameter
    global theParameter
    theParameter = 1
    matchParameter = ""
    expressionPrime()
    argumentsListPrime()


def argumentsListPrime():  # Rule 44
    global x
    if "," in token[x]:
        x += 1  # Accepts ,
        expressionPrime()
        argumentsListPrime()
    elif ")" in token[x]:
        return
    else:
        return


def duplicateFunctionCheck():
    global x
    global functionName
    global currentScope
    global functionType
    global functionReturn
    for l in functionDeclaration:  # checks if there are any dupllicates of declared functions
        if token[x - 2] in l:
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


def checkVoidIntFloatInFunctionType():
    global x
    global expressionReturn
    global expressionType
    if "void" in functionType:  # checks if void has a return with a value
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
        x += 1  # Accepts ;
        return
    else:
        print("REJECT")
        exit(0)


def duplicateVariableCheck():
    global x
    s = 0
    for l in vars:  # checks if there are any duplicates of declared variables
        if token[x - 2] in l:
            if variableType[s] in token[x - 3]:
                print("REJECT")
                exit(0)
        s += 1


def variableAppend():
    global x
    variableDeclaration.append(token[x - 3] + " " + token[x - 2] + " global 0")
    vars.append(token[x - 2])
    variableType.append(token[x - 3])
    varsScope.append("global")
    varsScopeBlock.append(0)
    if "void" in token[x - 3]:
        print("REJECT")
        exit(0)

def variableAppendTwo():
    global x
    variableDeclaration.append(token[x - 2] + " " + token[x - 1] + " global 0")
    vars.append(token[x - 1])
    variableType.append(token[x - 2])
    varsScope.append("global")
    varsScopeBlock.append(0)

def variableFunctionScopeAppend():
    global x
    variableDeclaration.append( token[x - 2] + " " + token[x - 1] + " " + str(functionName) + " " + str(currentScope))
    vars.append(token[x - 1])
    variableType.append(token[x - 2])
    varsScope.append(functionName)
    varsScopeBlock.append(currentScope)

def getVar():
    global x
    q = 0
    global expressionType
    check = variableType[q]
    for l in vars:  # gets the type of the var for operation agreement
        if l in token[x - 1]:
            check = variableType[q]
        q += 1
    if expressionType not in check:
        print("REJECT")
        exit(0)

        # ----- end of semantic analyzing parser ----- #


programDeclaration()  # runs the program

#print(variableDeclaration)
#print(functionDeclaration)

if checkFinalMain == 1 and checkMain == 1:  # check if contains 1 main function
    print("ACCEPT")
else:
    print("REJECT")