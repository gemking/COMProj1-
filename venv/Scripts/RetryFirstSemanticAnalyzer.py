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
                    # print t[5]
                    token.append(word[4])  # appends rest of symbols
        elif word[3] and insideComment == 0:  # matches errors and makes sure insideComment is 0
            # print "ERROR:", t[6]
            token.append(word[3])  # appends error

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


def programDeclaration():  # runs program(Rule 1)
    global isCompleted
    declarationList()
    if "$" in token[x]:
        isCompleted = 1  # continues outside
    else:
        print("REJECT")  # if not, Reject


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

        x += 1  # Accept ID
        if ";" in token[x]:
            x += 1  # Accept ;
            s = 0
            for l in vars:  # check for duplicate declared variables
                if token[x - 2] in l:
                    if variableType[s] in token[x - 3]:
                        print("REJECT")
                        exit(0)
                s += 1

            variableDeclaration.append(token[x - 3] + " " + token[x - 2] + " global 0")
            vars.append(token[x - 2])
            variableType.append(token[x - 3])
            varsScope.append("global")
            varsScopeBlock.append(0)

            if "void" in token[x - 3]:
                print("REJECT")
                exit(0)

        elif "[" in token[x]:
            x += 1  # Accept [
            s = 0
            for l in vars:  # check for duplicate declared variables
                if token[x - 2] in l:
                    if variableType[s] in token[x - 3]:
                        print("REJECT")
                        exit(0)
                s += 1

            variableDeclaration.append(token[x - 3] + " " + token[x - 2] + " global 0")
            vars.append(token[x - 2])
            variableType.append(token[x - 3])
            varsScope.append("global")
            varsScopeBlock.append(0)

            if "void" in token[x - 3]:
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
            for l in functionDeclaration:  # check for duplicate declared functions
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

            if ")" in token[x]:
                x += 1  # Accept )
                compoundStatement()

                if functionReturn == 0 and "int" in functionType:  # check if not funtype in "int"
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


def theVariableDeclaration():  # Rule 5
    global x
    global checkMain
    typeSpecifier()

    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        s = 0
        for l in vars:  # check for duplicate declared variables
            if token[x - 1] in l:
                if varsScope[s] in functionName:
                    if varsScopeBlock[s] >= currentScope:
                        print("REJECT")
                        exit(0)
            s += 1
        variableDeclaration.append(
            token[x - 2] + " " + token[x - 1] + " " + str(functionName) + " " + str(currentScope))
        vars.append(token[x - 1])
        variableType.append(token[x - 2])
        varsScope.append(functionName)
        varsScopeBlock.append(currentScope)

        if "void" in token[x - 2]:  # check if ID is type void
            print("REJECT")
            exit(0)
    else:
        print("REJECT")
        exit(0)

    variableDeclarationPrime()


def variableDeclarationPrime():  # Rule 6
    global x
    if ";" in token[x]:
        x += 1  # Accept ;
    elif "[" in token[x]:
        x += 1  # Accept [
        w = hasnum(token[x])
        if w is True:
            x += 1  # Accept NUM/FLOAT
            if "." in token[x - 1]:  # check for float in array declaration
                print("REJECT")
                exit(0)
            if "E" in token[x - 1]:  # check for float in array declaration
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


def typeSpecifier():  # Rule 7
    global x
    if token[x] in miniKeywords:
        x += 1  # Accept int/void/float
    else:
        return


def parameter():  # Rule 8
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


def parameterPrime():  # Rule 9
    global x, functionName, currentScope
    typeSpecifier()
    functionDeclaration[functionIndex] = functionDeclaration[functionIndex] + " " + token[x - 1]
    functionCallArguments.append("")
    functionCallArguments[functionIndex] = functionCallArguments[functionIndex] + " " + token[x - 1]
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        functionDeclaration[functionIndex] = functionDeclaration[functionIndex] + " " + token[x - 1]

        s = 0
        g = 0
        gh = 0
        dn = 0
        for l in vars:  # check for duplicate declared variables and with scope
            if token[x - 1] in l:
                if "global" not in varsScope[s] and varsScope[s] not in functionName:  # may not work
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
            variableDeclaration.append(token[x - 2] + " " + token[x - 1] + " global 0")
            vars.append(token[x - 1])
            variableType.append(token[x - 2])
            varsScope.append("global")
            varsScopeBlock.append(0)

        else:
            variableDeclaration.append(
                token[x - 2] + " " + token[x - 1] + " " + str(functionName) + " " + str(currentScope))
            vars.append(token[x - 1])
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
        if "void" in token[x - 1]:
            return
        else:
            print("REJECT")
            exit(0)


def parameters():  # Rule 10
    global x
    global functionIndex
    if "int" in token[x] or "float" in token[x]:
        parameterPrime()
        parametersListPrime()
        functionIndex += 1
    elif "void" in token[x]:
        parametersPrime()
        functionIndex += 1
    else:
        print("REJECT")
        exit(0)


def parametersPrime():  # Rule 11
    global x
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        parameterPrime()
        parametersListPrime()
    else:
        return


def parametersList():  # Rule 12
    parameterPrime()
    parametersListPrime()


def parametersListPrime():  # Rule 13
    global x
    if "," in token[x]:
        x += 1  # Accept ,
        parameterPrime()
        parametersListPrime()
    elif ")" in token[x]:
        return
    else:
        return


def compoundStatement():  # Rule 14
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


def localDeclarations():  # Rule 15
    localDeclarationsPrime()


def localDeclarationsPrime():  # Rule 16
    if token[x] in miniKeywords:
        theVariableDeclaration()
        localDeclarationsPrime()
    else:
        return


def statementList():  # Rule 17
    statementListPrime()


def statementListPrime():  # Rule 18
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


def statement():  # Rule 19
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


def expressionStatement():  # Rule 20
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


def selectionStatement():  # Rule 21
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
    selectionStatementPrime()


def selectionStatementPrime():  # Rule 22
    global x
    if "else" in token[x]:
        x += 1  # Accept else
        statement()
    else:
        return


def iterationStatement():  # Rule 23
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


def returnStatement():  # Rule 24
    global x
    global functionReturn
    if "return" in token[x]:
        x += 1  # Accept return
        if "int" in functionType:
            functionReturn = 1
        else:
            functionReturn = 1
    else:
        return
    returnStatementPrime()


def returnStatementPrime():  # Rule 25
    global x
    global functionReturn
    global expressionReturn
    global expressionType
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


def expression():  # Rule 26
    global x
    global expressionType
    global leftExpression
    global rightExpression
    global theParameter
    global matchParameter
    if "=" in token[x]:
        x += 1  # Accept =
        s = 0
        for l in vars:  # find the type of the first ID for the exp
            if token[x - 2] == l:
                expressionType = variableType[s]
                leftExpression = 1
            s += 1
        expressionPrime()
        leftExpression = 0
    elif "[" in token[x]:
        x += 1  # Accept [
        expressionType = "int"
        rightExpression = 1
        expressionPrime()
        rightExpression = 0
        if "[" in token[x - 1]:
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
        if p == 0 and matchParameter not in functionCallArguments[s]:
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


def expressionPrime():  # Rule 27
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
            for l in vars:  # get the type of the var for operand/operator checking
                if l in token[x - 1]:
                    check = variableType[q]
                q += 1
            matchParameter = matchParameter + " " + check

        if leftExpression == 1 and theParameter == 0:
            if "(" in token[x]:
                q = 0
                check = 0
                for l in functionNames:  # get the type of the function for operand/operator checking
                    if l in token[x - 1]:
                        check = functionTypes[q]
                    q += 1
                if expressionType != check:
                    print("REJECT")
                    exit(0)

            else:
                q = 0
                dn = 0
                check = 0
                for l in vars:  # check variable before checking if operator/operand agree
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
            q = 0
            for l in vars:  # get the type of the var for operand/operator checking
                if l in token[x - 1]:
                    check = variableType[q]
                q += 1
            if expressionType not in check:
                print("REJECT")
                exit(0)

        if expressionReturn == 1:
            q = 0
            check = 0
            for l in vars:  # get the type of the var for operand/operator checking
                if l in token[x - 1]:
                    check = variableType[q]
                q += 1
            if expressionType not in check:
                print("REJECT")
                exit(0)

        if "(" in token[x] and leftExpression == 0 and theParameter == 0:
            if token[x - 1] not in functionNames:
                print("REJECT")
                exit(0)

        dn = 0
        s = 0
        for l in vars:  # check for duplicate declared variables
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
            if "." in token[x - 1]:
                matchParameter = matchParameter + " float"
            elif "E" in token[x - 1]:
                matchParameter = matchParameter + " float"
            else:
                matchParameter = matchParameter + " int"

        dn = 0
        if "." in token[x - 1]:
            dn = 1
        if "E" in token[x - 1]:
            dn = 1

        if expressionReturn == 1 and dn == 1:
            if "float" not in expressionType:
                print("REJECT")
                exit(0)

        if expressionReturn == 1 and dn == 0:
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
            if dn != 1 and "float" in expressionType:
                if "." not in token[x + 1] and "E" not in token[x + 1]:
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


def variable():  # Rule 28
    global x
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
    else:
        return
    variablePrime()


def variablePrime():  # Rule 29
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


def simpleExpression():  # Rule 30
    addExpression()
    simpleExpressionPrime()


def simpleExpressionPrime():  # Rule 31
    if token[x] in comparisionSymbols:
        comparisonOperation()
        addExpression()
    else:
        return


def comparisonOperation():  # Rule 32
    global x
    if token[x] in comparisionSymbols:
        x += 1  # Accept <=, <, >, >=, ==, or !=
    else:
        return


def addExpression():  # Rule 33
    term()
    addExpressionPrime()


def addExpressionPrime():  # Rule 34
    if token[x] in additionSubtractionSymbols:
        additiveOperation()
        term()
        addExpressionPrime()
    else:
        return


def additiveOperation():  # Rule 35
    global x
    if token[x] in additionSubtractionSymbols:
        x += 1  # Accept +, -
    else:
        return


def term():  # Rule 36
    factor()
    termPrime()


def termPrime():  # Rule 37
    if token[x] in multiplicationDivisionSymbols:
        multiplicativeOperation()
        factor()
        termPrime()
    else:
        return


def multiplicativeOperation():  # Rule 38
    global x
    if token[x] in multiplicationDivisionSymbols:
        x += 1  # Accept *, /
    else:
        return


def factor():  # Rule 39
    global x
    leftExpression
    expressionReturn
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID

        if leftExpression == 1:
            q = 0
            dn = 0
            for l in vars:  # get the type of the var for operand/operator checking
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
            for l in vars:  # get the type of the var for operand/operator checking
                if l in token[x - 1]:
                    check = variableType[q]
                q += 1
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


def factorPrime():  # Rule 40
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


def arguments():  # Rule 41
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


def argumentsList():  # Rule 42
    global matchParameter
    global theParameter
    theParameter = 1
    matchParameter = ""
    expressionPrime()
    argumentsListPrime()


def argumentsListPrime():  # Rule 43
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