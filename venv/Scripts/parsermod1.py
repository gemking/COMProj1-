import sys
import re

f = open(sys.argv[1], "r")  # open file and read contents into a list (without "\n")
filelines = f.read().splitlines()
f.close()

keywords = ["if", "else", "while", "int", "float", "void", "return"] #denotes all keywords
symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]" #denotes symbols used
# our regular expressions for the lexical analyzer
characters = "[a-z]+"  # gets all words/ID's
#comparisonSymbols = "<=|<|>=|>|==|!=" #for comparision
comparisonSymbols = "<" or "<=" or  ">" or ">=" or "==" or"!="
addSubtractSymbols = "+" or "-"
multiplyDivideSymbols = "*" or "/"
#numberVoidSymbols = "int" or "void" or "float"

characters = "[a-zA-Z]+" #obtains all words for the IDs
digits = "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" #gets all decimal values, including integer values 0-9
errors = "\S" #reports errors

incomment = 0  # check to see if in comment
token = []  # create List to hold all tokens
i = 0  # token counter for parser

# ------------------Begin going through the file and getting tokens----------------------- #
for flines in filelines:
    fline = flines

    if not fline:
        continue
    # print  # extra line to separate input lines
    # if fline:
        # print "INPUT: " + fline  # print the input line, while also getting rid of blank lines

    list = "(%s)|(%s)|(%s)|(%s)" % (characters, digits, symbols, errors)  # puts entire library into a list of strings

    for t in re.findall(list, fline):
        if t[0] and incomment == 0:
            if t[0] in keywords:
                token.append(t[0])
                # print "keyword:", t[0]
            else:
                # print "ID:", t[0]
                token.append(t[0])
        elif t[1] and incomment == 0:
            if "." in t[1]:
                # print "FLOAT:", t[1]
                token.append(t[1])
            elif "E" in t[1]:
                # print "FLOAT:", t[1]
                token.append(t[1])
            else:
                # print "NUM:", t[1]
                token.append(t[1])
        elif t[3]:
            if t[3] == "/*":
                incomment = incomment + 1
            elif t[3] == "*/" and incomment > 0:
                incomment = incomment - 1
            elif t[3] == "//" and incomment == 0:
                break
            elif incomment == 0:
                if t[3] == "*/":
                    if "*/*" in fline:
                        # print "*"
                        token.append("*")
                        incomment += 1
                        continue
                    else:
                        # print "*"
                        token.append("*")
                        # print "/"
                        token.append("/")
                else:
                    # print t[5]
                    token.append(t[3])
        elif t[4] and incomment == 0:
            # print "ERROR:", t[6]
            token.append(t[4])
# ------------ end of for loop for the file and getting tokens --------------------------- #

token.append("$")  # add to end to check if done parsing

# ---------------------------------- parsing functions ----------------------------------- #


def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def program():  # 1
    dollarOne()
    if "$" in token[i]:
        print("ACCEPT")
    else:
        print ("REJECT")


def dollarOne():  # 2
    declaration()
    dollarOnePrime()


def dollarOnePrime():  # 3
    if "int" in token[i] or "void" in token[i] or "float" in token[i]:
        declaration()
        dollarOnePrime()
    elif "$" in token[i]:
        return
    else:
        return


def declaration():  # 4
    global i
    types()
    x = token[i].isalpha()
    if token[i] not in keywords and x is True:
        i += 1  # Accept ID
        if ";" in token[i]:
            i += 1  # Accept ;
        elif "[" in token[i]:
            i += 1  # Accept [
            y = hasnum(token[i])
            if y is True:
                i += 1  # Accept NUM/FLOAT
                if "]" in token[i]:
                    i += 1  # Accept ]
                    if ";" in token[i]:
                        i += 1  # Accept ;
                    else:
                        print("REJECT")
                        sys.exit(0)
                else:
                    print("REJECT")
                    sys.exit(0)
            else:
                print("REJECT")
                sys.exit(0)
        elif "(" in token[i]:
            i += 1  # Accept (
            parameters()

            if ")" in token[i]:
                i += 1  # Accept )
                compoundStatement()
            else:
                print("REJECT")
                sys.exit(0)
        else:
            print("REJECT")
            sys.exit(0)
    else:
        print("REJECT")
        sys.exit(0)


def variableDeclaration():  # 5
    global i
    types()

    x = token[i].isalpha()
    if token[i] not in keywords and x is True:
        i += 1  # Accept ID
    else:
        print("REJECT")
        sys.exit(0)

    if ";" in token[i]:
        i += 1  # Accept ;
    elif "[" in token[i]:
        i += 1  # Accept [
        x = hasnum(token[i])
        if x is True:
            i += 1  # Accept NUM/FLOAT
            if "]" in token[i]:
                i += 1  # Accept ]
                if ";" in token[i]:
                    i += 1  # Accept ;
                    return
                else:
                    print("REJECT")
                    sys.exit(0)
            else:
                print("REJECT")
                sys.exit(0)
        else:
            print("REJECT")
            sys.exit(0)
    else:
        print("REJECT")
        sys.exit(0)

# checking if in keywords messes up program process
def types():  # 6
    global i
    if "int" in token[i] or "void" in token[i] or "float" in token[i]:
        i += 1  # Accept int/void/float
    else:
        return


def functionDeclaration():  # 7
    global i
    types()

    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
    else:
        return

    if "(" in token[i]:
        i += 1  # Accept (
    else:
        print()
        sys.exit(0)

    parameters()

    if ")" in token[i]:
        i += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    compoundStatement()

def parameter():
    global i
    types()
    x = token[i].isalpha()
    if token[i] not in keywords and x is True:
        i += 1  # Accept ID
    else:
        return
    if "[" in token[i]:
        i += 1  # Accept [
        if "]" in token[i]:
            i += 1  # Accept ]
            return
        else:
            print("REJECT")
            sys.exit(0)
    else:
        return

def parameters():  # 8
    global i
    if "int" in token[i] or "float" in token[i]:
        parametersList()
    elif "void" in token[i]:
        i += 1  # Accept void
        return
    else:
        print("REJECT")
        sys.exit(0)


def parametersList():  # 9
    parameter()
    parametersListPrime()


def parametersListPrime():  # 10
    global i
    if "," in token[i]:
        i += 1  # Accept ,
        parameter()
        parametersListPrime()
    elif  ")" in token[i]:
        return
    else:
        return





def compoundStatement():  # 12
    global i
    if "{" in token[i]:
        i += 1  # Accept {
    else:
        return

    localDeclarations()
    statementList()

    if "}" in token[i]:
        i += 1  # Accept }
    else:
        print("REJECT")
        sys.exit(0)


def localDeclarations():  # 13
    localDeclarationsPrime()


def localDeclarationsPrime():  # 14
    if "int" in token[i] or "void" in token[i] or "float" in token[i]:
        variableDeclaration()
        localDeclarationsPrime()
    else:
        return


def statementList():  # 15
    statementListPrime()


def statementListPrime():  # 16
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywords and x is True:
        statement()
        statementListPrime()
    elif y is True:
        statement()
        statementListPrime()
    elif "(" in token[i] or ";" in token[i] or "{" in token[i] or "if" in token[i] or "while" in token[i] or "return" in token[i]:
        statement()
        statementListPrime()
    elif "}" in token[i]:
        return
    else:
        return


def statement():  # 17
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywords and x is True:
        expressionStatement()
    elif y is True:
        expressionStatement()
    elif "(" in token[i] or ";" in token[i]:
        expressionStatement()
    elif "{" in token[i]:
        compoundStatement()
    elif "if" in token[i]:
        selectionStatement()
    elif "while" in token[i]:
        itStatement()
    elif "return" in token[i]:
        returnStatement()
    else:
        print("REJECT")
        sys.exit(0)


def expressionStatement():  # 18
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywords and x is True:
        expression()
        if ";" in token[i]:
            i += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif y is True:
        expression()
        if ";" in token[i]:
            i += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif "(" in token[i]:
        expression()
        if ";" in token[i]:
            i += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif ";" in token[i]:
        i += 1  # Accept ;
    else:
        print("REJECT")
        sys.exit(0)


def selectionStatement():  # 19
    global i
    if "if" in token[i]:
        i += 1  # Accept if
    else:
        return

    if "(" in token[i]:
        i += 1  # Accept (
    else:
        print("REJECT")
        sys.exit(0)

    expression()

    if ")" in token[i]:
        i += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    statement()

    if "else" in token[i]:
        i += 1  # Accept else
        statement()
    else:
        return


def iterationStatement():  # 20
    global i
    if "while" in token[i]:
        i += 1  # Accept while
    else:
        return

    if "(" in token[i]:
        i += 1  # Accept (
    else:
        print("REJECT")
        sys.exit(0)

    expression()

    if ")" in token[i]:
        i += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    statement()


def returnStatement():  # 21
    global i
    if "return" in token[i]:
        i += 1  # Accept return
    else:
        return

    x = token[i].isalpha()
    y = hasnum(token[i])
    if ";" in token[i]:
        i += 1  # Accept ;
        return
    elif token[i] not in keywords and x is True:
        expression()
        if ";" in token[i]:
            i += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif y is True:
        expression()
        if ";" in token[i]:
            i += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif "(" in token[i]:
        expression()
        if ";" in token[i]:
            i += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    else:
        print("REJECT")
        sys.exit(0)


def expression():  # 22
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywords and x is True:
        i += 1  # Accept ID
        moreExpressions()
    elif "(" in token[i]:
        i += 1  # Accept (
        expression()
        if ")" in token[i]:
            i += 1  # Accept )
            termPrime()
            addExpressionPrime()
            if comparisonSymbols in token[i]:
                comparisonOperation()
                addExpression()
            elif addSubtractSymbols in token[i]:
                addExpressionPrime()
                if comparisonSymbols in token[i]:
                    comparisonOperation()
                    addExpression()
            elif comparisonSymbols in token[i]:
                comparisonOperation()
                addExpression()
            else:
                return
        else:
            print("REJECT")
            sys.exit(0)
    elif y is True:
        i += 1  # Accept NUM/FLOAT
        termPrime()
        addExpressionPrime()
        if comparisonSymbols in token[i]:
            comparisonOperation()
            addExpression()
        elif addSubtractSymbols in token[i]:
            addExpressionPrime()
            if comparisonSymbols in token[i]:
                comparisonOperation()
                addExpression()
        elif comparisonSymbols in token[i]:
                comparisonOperation()
                addExpression()
        else:
            return
    else:
        print("REJECT")
        sys.exit(0)


def moreExpressions():  # 22X
    global i
    if "=" in token[i]:
        i += 1  # Accept =
        expression()
    elif "[" in token[i]:
        i += 1  # Accept [
        expression()
        if "[" in token[i-1]:
            print("REJECT")
            sys.exit(0)
        if "]" in token[i]:
            i += 1  # Accept ]
            if "=" in token[i]:
                i += 1  # Accept =
                expression()
            elif multiplyDivideSymbols in token[i]:
                termPrime()
                addExpressionPrime()
                if comparisonSymbols in token[i]:
                    comparisonOperation()
                    addExpression()
                else:
                    return
            elif addSubtractSymbols in token[i]:
                addExpressionPrime()
                if comparisonSymbols in token[i]:
                    comparisonOperation()
                    addExpression()
            elif comparisonSymbols in token[i]:
                comparisonOperation()
                addExpression()
            else:
                return
        else:
            print("REJECT")
            sys.exit(0)
    elif "(" in token[i]:
        i += 1  # Accept (
        arguments()
        if ")" in token[i]:
            i += 1  # Accept )
            if multiplyDivideSymbols in token[i]:
                termPrime()
                addExpressionPrime()
                if comparisonSymbols in token[i]:
                    comparisonOperation()
                    addExpression()
                else:
                    return
            elif addSubtractSymbols in token[i]:
                addExpressionPrime()
                if comparisonSymbols in token[i]:
                    comparisonOperation()
                    addExpression()
            elif comparisonSymbols in token[i]:
                comparisonOperation()
                addExpression()
            else:
                return
        else:
            print("REJECT")
            sys.exit(0)
    elif multiplyDivideSymbols in token[i]:
        termPrime()
        addExpressionPrime()
        if comparisonSymbols in token[i]:
            comparisonOperation()
            addExpression()
        else:
            return
        # error begins
    elif addSubtractSymbols in token[i]:
        addExpressionPrime()
        if comparisonSymbols in token[i]:
            comparisonOperation()
            addExpression()
        else:
            return
    elif comparisonSymbols in token[i]:
        comparisonOperation()
        addExpression()
    else:
        return


def variable():  # 23
    global i
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
    else:
        return
    if "[" in token[i]:
        i += 1  # Accept [
        expression()
        if "]" in token[i]:
            i += 1  # Accept ]
        else:
            print("REJECT")
            sys.exit(0)
    else:
        return


def simplifyExpression():  # 24
    addExpression()
    if comparisonSymbols in token[i]:
        comparisonOperation()
        addExpression()
    else:
        return


def comparisonOperation():  # 25
    global i
    if comparisonSymbols in token[i]:
        i += 1  # Accept <=, <, >, >=, ==, or !=
    else:
        return


def addExpression():  # 26
    term()
    addExpressionPrime()


def addExpressionPrime():  # 27
    if addSubtractSymbols in token[i]:
        addOperation()
        term()
        addExpressionPrime()
    else:
        return


def addOperation():  # 28
    global i
    if addSubtractSymbols in token[i]:
        i += 1  # Accept +, -
    else:
        return


def term():  # 29
    factor()
    termPrime()


def termPrime():  # 30
    if multiplyDivideSymbols in token[i]:
        multiplyOperation()
        factor()
        termPrime()
    else:
        return


def multiplyOperation():  # 31
    global i
    if multiplyDivideSymbols in token[i]:
        i += 1  # Accept *, /
    else:
        return


def factor():  # 32
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywords and x is True:
        i += 1  # Accept ID
        if "[" in token[i]:
            i += 1  # Accept [
            expression()
            if "]" in token[i]:
                i += 1  # Accept ]
            else:
                return
        elif "(" in token[i]:
            i += 1  # Accept (
            arguments()
            if ")" in token[i]:
                i += 1  # Accept )
            else:
                return
        else:
            return
    elif y is True:
        i += 1  # Accept NUM/FLOAT
    elif "(" in token[i]:
        i += 1  # Accept (
        expression()
        if ")" in token[i]:
            i += 1  # Accept )
        else:
            return
    else:
        print("REJECT")
        sys.exit(0)


def call():  # 33
    global i
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        if "(" in token[i]:
            i += 1  # Accept (
            arguments()
            if ")" in token[i]:
                i += 1  # Accept )
            else:
                print("REJECT")
                sys.exit(0)
        else:
            print("REJECT")
            sys.exit(0)
    else:
        return


def arguments():  # 34
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywords and x is True:
        argumentsList()
    elif y is True:
        argumentsList()
    elif "(" in token[i]:
        argumentsList()
    elif ")" in token[i]:
        return
    else:
        return


def argumentsList():  # 35
    expression()
    argumentslistPrime()


def argumentslistPrime():  # 36
    global i
    if "," in token[i]:
        i += 1  # Accept ,
        expression()
        argumentslistPrime()
    elif ")" in token[i]:
        return
    else:
        return


# ----------------------------- end of parsing functions --------------------------------- #

# begin parsing
program()