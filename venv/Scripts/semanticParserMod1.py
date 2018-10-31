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


                 # ----- beginning of parser ----- #

def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def programDeclaration(): #runs program(Rule 1)
    declarationList()
    if "$" in token[x]:
        print("ACCEPT") #if $ can be applied in the token, proceed
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
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
        if ";" in token[x]:
            x += 1  # Accepts ;
        elif "[" in token[x]:
            x += 1  # Accepts [
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
            x += 1  # Accepts (
            parameters()

            if ")" in token[x]:
                x += 1  # Accepts )
                compoundStatement()
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

def variableDeclaration(): #Rule 6
    global x
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
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

def parameters(): #Rule 11
    global x
    if "int" in token[x] or "float" in token[x]:
        parametersList()
    elif "void" in token[x]:
        x += 1  # Accepts void
        parametersPrime()
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
    if "return" in token[x]:
        x += 1  # Accepts return
    else:
        return
    returnStatementPrime()


def returnStatementPrime(): #Rule 26
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if ";" in token[x]:
        x += 1  # Accepts ;
        return
    elif token[x] not in keywords and w is True:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accepts ;
            return
        else:
            print("REJECT")
            exit(0)
    elif z  is True:
        expressionPrime()
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
    if "=" in token[x]:
        x += 1  # Accepts =
        expressionPrime()
    elif "[" in token[x]:
        x += 1  # Accepts [
        expressionPrime()
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
        arguments()
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
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
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
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
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