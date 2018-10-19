import sys
import re

f = open(sys.argv[1], "r")  # open file and read contents into a list (without "\n")
filelines = f.read().splitlines()
f.close()

keywordchecklist = ["if", "else", "while", "int", "float", "void", "return"] #denotes all keywords
comparisonSymbols = "<" or "<=" or  ">" or ">=" or "==" or"!=" #holds relational operations
addSubtractSymbols = "+" or "-" #holds addition and subtraction operations
multiplyDivideSymbols = "*" or "/" #holds multiplication and division operations
# our regular expressions for the lexical analyzer
characters = "[a-zA-Z]+"  # gets all words/ID's
digits = "[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?" #gets all decimal values, including integer values 0-9
#digits = "[0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?"  # gets all NUM's/float numbers
symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"  # gets all special symbols
errors = "\S"

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

    list = "(%s)|(%s)|(%s)|(%s)" % (characters, digits, symbols, errors)


    for t in re.findall(list, fline):
        if t[0] and incomment == 0:
            if t[0] in keywordchecklist:
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
        elif t[4]:
            if "/*" in t[4]:
                incomment = incomment + 1
            elif "*/" in t[4] and incomment > 0:
                incomment = incomment - 1
            elif "//" in t[4] and incomment == 0:
                break
            elif incomment == 0:
                if "*/" in t[4]:
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
                    token.append(t[4])
        elif t[3] and incomment == 0:
            # print "ERROR:", t[6]
            token.append(t[3])
# ------------ end of for loop for the file and getting tokens --------------------------- #

token.append("$")  # add to end to check if done parsing

# ---------------------------------- parsing functions ----------------------------------- #


def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def program():  # 1
    dl()
    if token[i] == "$":
        print("ACCEPT")
    else:
        print("REJECT")


def dl():  # 2
    declaration()
    dlprime()


def dlprime():  # 3
    if token[i] == "int" or token[i] == "void" or token[i] == "float":
        declaration()
        dlprime()
    elif token[i] == "$":
        return
    else:
        return


def declaration():  # 4
    global i
    types()
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        if token[i] == ";":
            i += 1  # Accept ;
        elif token[i] == "[":
            i += 1  # Accept [
            y = hasnum(token[i])
            if y is True:
                i += 1  # Accept NUM/FLOAT
                if token[i] == "]":
                    i += 1  # Accept ]
                    if token[i] == ";":
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
        elif token[i] == "(":
            i += 1  # Accept (
            params()
            if token[i] == ")":
                i += 1  # Accept )
                compoundstmt()
            else:
                print("REJECT")
                sys.exit(0)
        else:
            print("REJECT")
            sys.exit(0)
    else:
        print("REJECT")
        sys.exit(0)


def vd():  # 5
    global i
    types()

    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
    else:
        print("REJECT")
        sys.exit(0)

    if token[i] == ";":
        i += 1  # Accept ;
    elif token[i] == "[":
        i += 1  # Accept [
        x = hasnum(token[i])
        if x is True:
            i += 1  # Accept NUM/FLOAT
            if token[i] == "]":
                i += 1  # Accept ]
                if token[i] == ";":
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


def types():  # 6
    global i
    if token[i] == "int" or token[i] == "void" or token[i] == "float":
        i += 1  # Accept int/void/float
    else:
        return


def fd():  # 7
    global i
    types()

    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
    else:
        return

    if token[i] == "(":
        i += 1  # Accept (
    else:
        print("REJECT")
        sys.exit(0)

    params()

    if token[i] == ")":
        i += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    compoundstmt()


def params():  # 8
    global i
    if token[i] == "int" or token[i] == "float":
        paramslist()
    elif token[i] == "void":
        i += 1  # Accept void
        return
    else:
        print("REJECT")
        sys.exit(0)


def paramslist():  # 9
    param()
    paramslistprime()


def paramslistprime():  # 10
    global i
    if token[i] == ",":
        i += 1  # Accept ,
        param()
        paramslistprime()
    elif token[i] == ")":
        return
    else:
        return


def param():  # 11
    global i
    types()
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
    else:
        return
    if token[i] == "[":
        i += 1  # Accept [
        if token[i] == "]":
            i += 1  # Accept ]
            return
        else:
            print("REJECT")
            sys.exit(0)
    else:
        return


def compoundstmt():  # 12
    global i
    if token[i] == "{":
        i += 1  # Accept {
    else:
        return

    localdeclarations()
    statementlist()

    if token[i] == "}":
        i += 1  # Accept }
    else:
        print("REJECT")
        sys.exit(0)


def localdeclarations():  # 13
    localdeclarationsprime()


def localdeclarationsprime():  # 14
    if token[i] == "int" or token[i] == "void" or token[i] == "float":
        vd()
        localdeclarationsprime()
    else:
        return


def statementlist():  # 15
    statementlistprime()


def statementlistprime():  # 16
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        statement()
        statementlistprime()
    elif y is True:
        statement()
        statementlistprime()
    elif token[i] == "(" or token[i] == ";" or token[i] == "{" or token[i] == "if" or\
                     token[i] == "while" or token[i] == "return":
        statement()
        statementlistprime()
    elif token[i] == "}":
        return
    else:
        return


def statement():  # 17
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        expstmt()
    elif y is True:
        expstmt()
    elif token[i] == "(" or token[i] == ";":
        expstmt()
    elif token[i] == "{":
        compoundstmt()
    elif token[i] == "if":
        selectionstmt()
    elif token[i] == "while":
        itstmt()
    elif token[i] == "return":
        retstmt()
    else:
        print("REJECT")
        sys.exit(0)


def expstmt():  # 18
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif y is True:
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif token[i] == "(":
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif token[i] == ";":
        i += 1  # Accept ;
    else:
        print("REJECT")
        sys.exit(0)


def selectionstmt():  # 19
    global i
    if token[i] == "if":
        i += 1  # Accept if
    else:
        return

    if token[i] == "(":
        i += 1  # Accept (
    else:
        print("REJECT")
        sys.exit(0)

    exp()

    if token[i] == ")":
        i += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    statement()

    if token[i] == "else":
        i += 1  # Accept else
        statement()
    else:
        return


def itstmt():  # 20
    global i
    if token[i] == "while":
        i += 1  # Accept while
    else:
        return

    if token[i] == "(":
        i += 1  # Accept (
    else:
        print("REJECT")
        sys.exit(0)

    exp()

    if token[i] == ")":
        i += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    statement()


def retstmt():  # 21
    global i
    if token[i] == "return":
        i += 1  # Accept return
    else:
        return

    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] == ";":
        i += 1  # Accept ;
        return
    elif token[i] not in keywordchecklist and x is True:
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif y is True:
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif token[i] == "(":
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    else:
        print("REJECT")
        sys.exit(0)


def exp():  # 22
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        ex()
    elif token[i] == "(":
        i += 1  # Accept (
        exp()
        if token[i] == ")":
            i += 1  # Accept )
            termprime()
            addexpprime()
            if comparisonSymbols in token[i]:
                relop()
                addexp()
            elif addSubtractSymbols in token[i]:
                addexpprime()
                if comparisonSymbols in token[i]:
                    relop()
                    addexp()
            elif comparisonSymbols in token[i]:
                relop()
                addexp()
            else:
                return
        else:
            print ("REJECT")
            sys.exit(0)
    elif y is True:
        i += 1  # Accept NUM/FLOAT
        termprime()
        addexpprime()
        if comparisonSymbols in token[i]:
            relop()
            addexp()
        elif addSubtractSymbols in token[i]:
            addexpprime()
            if comparisonSymbols in token[i]:
                relop()
                addexp()
        elif comparisonSymbols in token[i]:
                relop()
                addexp()
        else:
            return
    else:
        print("REJECT")
        sys.exit(0)


def ex():  # 22X
    global i
    if token[i] == "=":
        i += 1  # Accept =
        exp()
    elif token[i] == "[":
        i += 1  # Accept [
        exp()
        if token[i-1] == "[":
            print("REJECT")
            sys.exit(0)
        if token[i] == "]":
            i += 1  # Accept ]
            if token[i] == "=":
                i += 1  # Accept =
                exp()
            elif multiplyDivideSymbols in token[i]:
                termprime()
                addexpprime()
                if comparisonSymbols in token[i]:
                    relop()
                    addexp()
                else:
                    return
            elif addSubtractSymbols in token[i]:
                addexpprime()
                if comparisonSymbols in token[i]:
                    relop()
                    addexp()
            elif comparisonSymbols in token[i]:
                relop()
                addexp()
            else:
                return
        else:
            print("REJECT")
            sys.exit(0)
    elif token[i] == "(":
        i += 1  # Accept (
        args()
        if token[i] == ")":
            i += 1  # Accept )
            if multiplyDivideSymbols in token[i]:
                termprime()
                addexpprime()
                if comparisonSymbols in token[i]:
                    relop()
                    addexp()
                else:
                    return
            elif addSubtractSymbols in token[i]:
                addexpprime()
                if comparisonSymbols in token[i]:
                    relop()
                    addexp()
            elif comparisonSymbols in token[i]:
                relop()
                addexp()
            else:
                return
        else:
            print("REJECT")
            sys.exit(0)
    elif multiplyDivideSymbols in token[i]:
        termprime()
        addexpprime()
        if comparisonSymbols in token[i]:
            relop()
            addexp()
        else:
            return
    elif addSubtractSymbols in token[i]:
        addexpprime()
        if comparisonSymbols in token[i]:
            relop()
            addexp()
        else:
            return
    elif comparisonSymbols in token[i]:
        relop()
        addexp()
    else:
        return


def var():  # 23
    global i
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
    else:
        return
    if token[i] == "[":
        i += 1  # Accept [
        exp()
        if token[i] == "]":
            i += 1  # Accept ]
        else:
            print("REJECT")
            sys.exit(0)
    else:
        return


def simexp():  # 24
    addexp()
    if comparisonSymbols in token[i]:
        relop()
        addexp()
    else:
        return


def relop():  # 25
    global i
    if comparisonSymbols in token[i]:
        i += 1  # Accept <=, <, >, >=, ==, or !=
    else:
        return


def addexp():  # 26
    term()
    addexpprime()


def addexpprime():  # 27
    if addSubtractSymbols in token[i]:
        addop()
        term()
        addexpprime()
    else:
        return


def addop():  # 28
    global i
    if addSubtractSymbols in token[i]:
        i += 1  # Accept +, -
    else:
        return


def term():  # 29
    factor()
    termprime()


def termprime():  # 30
    if multiplyDivideSymbols in token[i]:
        mulop()
        factor()
        termprime()
    else:
        return


def mulop():  # 31
    global i
    if multiplyDivideSymbols in token[i]:
        i += 1  # Accept *, /
    else:
        return


def factor():  # 32
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        if token[i] == "[":
            i += 1  # Accept [
            exp()
            if token[i] == "]":
                i += 1  # Accept ]
            else:
                return
        elif token[i] == "(":
            i += 1  # Accept (
            args()
            if token[i] == ")":
                i += 1  # Accept )
            else:
                return
        else:
            return
    elif y is True:
        i += 1  # Accept NUM/FLOAT
    elif token[i] == "(":
        i += 1  # Accept (
        exp()
        if token[i] == ")":
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
        if token[i] == "(":
            i += 1  # Accept (
            args()
            if token[i] == ")":
                i += 1  # Accept )
            else:
                print("REJECT")
                sys.exit(0)
        else:
            print("REJECT")
            sys.exit(0)
    else:
        return


def args():  # 34
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        arglist()
    elif y is True:
        arglist()
    elif token[i] == "(":
        arglist()
    elif token[i] == ")":
        return
    else:
        return


def arglist():  # 35
    exp()
    arglistprime()


def arglistprime():  # 36
    global i
    if token[i] == ",":
        i += 1  # Accept ,
        exp()
        arglistprime()
    elif token[i] == ")":
        return
    else:
        return


# ----------------------------- end of parsing functions --------------------------------- #

# begin parsing
program()