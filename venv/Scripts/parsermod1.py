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
digits = "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" #gets all decimal values, including integer values 0-9
errors = "\S" #reports errors
token = []  # creates a list that holds all of the tokens
x = 0  #value that holds the token counter for the parser

for importantLines in filelines: #receiving importantlines from filelines
    importantLine = importantLines #sets importantLine to importantLines


    if not importantLine:
        continue

    list = "(%s)|(%s)|(%s)|(%s)" % (characters, digits, symbols, errors)  # puts entire library into a list of strings

    for word in re.findall(list, importantLine): #finds list
        if re.match(characters, word[0]) and insideComment == 0: #matches digits and makes sure insideComment is 0
            if word[0] in keywords:
                token.append(word[0]) #keyword is constructed out of characters a-zA-Z
            else:
                token.append(word[0]) #appends character values that are not keywords




        elif re.match(digits,word[1]) and insideComment == 0:
            if "." in word[1]:
                token.append(word[1]) #checks if value is a decimal value and appends
            elif "E" in word[1]:
                token.append(word[1]) #checks if value is an expontential value and appends
            else:
                token.append(word[1]) #appends integer value
        elif re.match(symbols, word[3]):  # matches symbols
            if "/*" in word[3]:  # Checks when word approaches /*
                insideComment += 1  # increments insideComment if inside
            elif "*/" in word[3] and insideComment > 0:  # Checks when word approaches */
                insideComment -= 1  # decrements insideComment if outside
            elif "//" in word[3] and insideComment > 0:  # If neither
                break
            elif insideComment == 0:  # when inside counter is 0
                if "*/" in word[3]:  # when it reaches terminal */
                    if "*/*" in word:  # when it's still sorting through comments
                        token.append("*")
                        insideComment += 1
                        continue  # skips comments and continues through the program
                    else:
                        token.append("*")  # appends multiplication symbol
                        token.append("/")  # appends division symbol
                else:
                    token.append(word[3])  # appends rest of symbols
        elif word[4] and insideComment == 0:  # matches errors and makes sure insideComment is 0
            token.append(word[4])  # appends error
# ------------ end of for loop for the file and getting tokens --------------------------- #

token.append("$")  # add to end to check if done parsing

# ---------------------------------- parsing functions ----------------------------------- #


def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def program():  # 1
    dollarOne()
    if "$" in token[x]:
        print("ACCEPT")
    else:
        print ("REJECT")


def dollarOne():  # 2
    declaration()
    dollarOnePrime()


def dollarOnePrime():  # 3
    if "int" in token[x] or "void" in token[x] or "float" in token[x]:
        declaration()
        dollarOnePrime()
    elif "$" in token[x]:
        return
    else:
        return


def declaration():  # 4
    global x
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        if ";" in token[x]:
            x += 1  # Accept ;
        elif "[" in token[x]:
            x += 1  # Accept [
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
            parameters()

            if ")" in token[x]:
                x += 1  # Accept )
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

def declarationPrime():  # 5
    global x
    types()
    #variableDeclaration()
    w = token[x].isalpha()
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID
    else:
        return

    if "(" in token[x]:
        x += 1  # Accept (
    else:
        print()
        exit(0)

    parameters()

    if ")" in token[x]:
        x += 1  # Accept )
    else:
        print("REJECT")
        exit(0)

    compoundStatement()

def variableDeclaration():  # 5
    global x
    typeSpecifier()

    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
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

# checking if in keywords messes up program process
def typeSpecifier():  # 6
    global x
    if "int" in token[x] or "void" in token[x] or "float" in token[x]:
        x += 1  # Accept int/void/float
    else:
        return



def parameter():
    global x
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
    else:
        return
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

def parameters():  # 8
    global x
    if "int" in token[x] or "float" in token[x]:
        parametersList()
    elif "void" in token[x]:
        x += 1  # Accept void
        return
    else:
        print("REJECT")
        exit(0)


def parametersList():  # 9
    parameter()
    parametersListPrime()


def parametersListPrime():  # 10
    global x
    if "," in token[x]:
        x += 1  # Accept ,
        parameter()
        parametersListPrime()
    elif  ")" in token[x]:
        return
    else:
        return





def compoundStatement():  # 12
    global x
    if "{" in token[x]:
        x += 1  # Accept {
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
    if "int" in token[x] or "void" in token[x] or "float" in token[x]:
        variableDeclaration()
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
    elif "(" in token[x] or ";" in token[x] or "{" in token[x] or "if" in token[x] or "while" in token[x] or "return" in token[x]:
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
        expression()
        if ";" in token[x]:
            x += 1  # Accept ;
        else:
            print("REJECT")
            exit(0)
    elif z is True:
        expression()
        if ";" in token[x]:
            x += 1  # Accept ;
        else:
            print("REJECT")
            exit(0)
    elif "(" in token[x]:
        expression()
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

    expression()

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

    expression()

    if ")" in token[x]:
        x += 1  # Accept )
    else:
        print("REJECT")
        exit(0)

    statement()


def returnStatement():  # 21
    global x
    if "return" in token[x]:
        x += 1  # Accept return
    else:
        return

    w = token[x].isalpha()
    z = hasnum(token[x])
    if ";" in token[x]:
        x += 1  # Accept ;
        return
    elif token[x] not in keywords and w is True:
        expression()
        if ";" in token[x]:
            x += 1  # Accept ;
            return
        else:
            print("REJECT")
            exit(0)
    elif z  is True:
        expression()
        if ";" in token[x]:
            x += 1  # Accept ;
            return
        else:
            print("REJECT")
            exit(0)
    elif "(" in token[x]:
        expression()
        if ";" in token[x]:
            x += 1  # Accept ;
            return
        else:
            print("REJECT")
            exit(0)
    else:
        print("REJECT")
        exit(0)


def expression():  # 22
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        moreExpressions()
    elif "(" in token[x]:
        x += 1  # Accept (
        expression()
        if ")" in token[x]:
            x += 1  # Accept )
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
        x += 1  # Accept NUM/FLOAT
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


def moreExpressions():  # 22X
    global x
    if "=" in token[x]:
        x += 1  # Accept =
        expression()
    elif "[" in token[x]:
        x += 1  # Accept [
        expression()
        if "[" in token[x-1]:
            print("REJECT")
            exit(0)
        if "]" in token[x]:
            x += 1  # Accept ]
            if "=" in token[x]:
                x += 1  # Accept =
                expression()
            elif multiplyDivideSymbols in token[x]:
                termPrime()
                addExpressionPrime()
                if comparisonSymbols in token[x]:
                    comparisonOperation()
                    addExpression()
                else:
                    return
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
        x += 1  # Accept (
        arguments()
        if ")" in token[x]:
            x += 1  # Accept )
            if multiplyDivideSymbols in token[x]:
                termPrime()
                addExpressionPrime()
                if comparisonSymbols in token[x]:
                    comparisonOperation()
                    addExpression()
                else:
                    return
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
        if comparisonSymbols in token[x]:
            comparisonOperation()
            addExpression()
        else:
            return
        # error begins
    elif addSubtractSymbols in token[x]:
        addExpressionPrime()
        if comparisonSymbols in token[x]:
            comparisonOperation()
            addExpression()
        else:
            return
    elif comparisonSymbols in token[x]:
        comparisonOperation()
        addExpression()
    else:
        return


def variable():  # 23
    global x
    w = token[x].isalpha()
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID
    else:
        return
    if "[" in token[x]:
        x += 1  # Accept [
        expression()
        if "]" in token[x]:
            x += 1  # Accept ]
        else:
            print("REJECT")
            exit(0)
    else:
        return


def simplifyExpression():  # 24
    addExpression()
    if comparisonSymbols in token[x]:
        comparisonOperation()
        addExpression()
    else:
        return


def comparisonOperation():  # 25
    global x
    if comparisonSymbols in token[x]:
        x += 1  # Accept <=, <, >, >=, ==, or !=
    else:
        return


def addExpression():  # 26
    term()
    addExpressionPrime()


def addExpressionPrime():  # 27
    if addSubtractSymbols in token[x]:
        addOperation()
        term()
        addExpressionPrime()
    else:
        return


def addOperation():  # 28
    global x
    if addSubtractSymbols in token[x]:
        x += 1  # Accept +, -
    else:
        return


def term():  # 29
    factor()
    termPrime()


def termPrime():  # 30
    if multiplyDivideSymbols in token[x]:
        multiplyOperation()
        factor()
        termPrime()
    else:
        return


def multiplyOperation():  # 31
    global x
    if multiplyDivideSymbols in token[x]:
        x += 1  # Accept *, /
    else:
        return


def factor():  # 32
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        if "[" in token[x]:
            x += 1  # Accept [
            expression()
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
        expression()
        if ")" in token[x]:
            x += 1  # Accept )
        else:
            return
    else:
        print("REJECT")
        exit(0)


def call():  # 33
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
    expression()
    argumentslistPrime()


def argumentslistPrime():  # 36
    global x
    if "," in token[x]:
        x += 1  # Accept ,
        expression()
        argumentslistPrime()
    elif ")" in token[x]:
        return
    else:
        return


# ----------------------------- end of parsing functions --------------------------------- #

# begin parsing
program()