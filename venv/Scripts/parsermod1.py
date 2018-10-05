import sys
import re

f = open(sys.argv[1], "r")  # open file and read contents into a list (without "\n")
filelines = f.read().splitlines()
f.close()

keywordchecklist = ["else", "if", "int", "return", "void", "while", "float"]  # list of all keywords

# our regular expressions for the lexical analyzer
wordsRegex = "[a-z]+"  # gets all words/ID's
#comparisonSymbols = "<=|<|>=|>|==|!=" #for comparision
comparisonSymbols = "<" or "<=" or  ">" or ">=" or "==" or"!="
addSubtractSymbols = "+" or "-"
multiplyDivideSymbols = "*" or "/"
#numberVoidSymbols = "int" or "void" or "float"
numbersRegex = "[0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?"  # gets all NUM's/float numbers
symRegex = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"  # gets all special symbols
errorRegex = "\S"

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

    regex = "(%s)|(%s)|(%s)|(%s)" % (wordsRegex, numbersRegex, symRegex, errorRegex)
    '([a-z]+)|([0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?)|'
    '("\/\*|\*\/|\+|-|\*|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]|//")|(\S)'

    for t in re.findall(regex, fline):
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
        elif t[5]:
            if t[5] == "/*":
                incomment = incomment + 1
            elif t[5] == "*/" and incomment > 0:
                incomment = incomment - 1
            elif t[5] == "//" and incomment == 0:
                break
            elif incomment == 0:
                if t[5] == "*/":
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
                    token.append(t[5])
        elif t[6] and incomment == 0:
            # print "ERROR:", t[6]
            token.append(t[6])
# ------------ end of for loop for the file and getting tokens --------------------------- #

token.append("$")  # add to end to check if done parsing

# ---------------------------------- parsing functions ----------------------------------- #


def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def program():  # 1
    dl()
    if "$" in token[i]:
        print("ACCEPT")
    else:
        print ("REJECT")


def dl():  # 2
    declaration()
    dlprime()


def dlprime():  # 3
    if "int" in token[i] or "void" in token[i] or "float" in token[i]:
        declaration()
        dlprime()
    elif "$" in token[i]:
        return
    else:
        return


def declaration():  # 4
    global i
    types()
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
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
            params()

            if ")" in token[i]:
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


def fd():  # 7
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

    params()

    if ")" in token[i]:
        i += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    compoundstmt()


def params():  # 8
    global i
    if "int" in token[i] or "float" in token[i]:
        paramslist()
    elif "void" in token[i]:
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
    if "," in token[i]:
        i += 1  # Accept ,
        param()
        paramslistprime()
    elif  ")" in token[i]:
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


def compoundstmt():  # 12
    global i
    if "{" in token[i]:
        i += 1  # Accept {
    else:
        return

    localdeclarations()
    statementlist()

    if "}" in token[i]:
        i += 1  # Accept }
    else:
        print("REJECT")
        sys.exit(0)


def localdeclarations():  # 13
    localdeclarationsprime()


def localdeclarationsprime():  # 14
    if "int" in token[i] or "void" in token[i] or "float" in token[i]:
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
    elif "(" in token[i] or ";" in token[i] or "{" in token[i] or "if" in token[i] or "while" in token[i] or "return" in token[i]:
        statement()
        statementlistprime()
    elif "}" in token[i]:
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
    elif "(" in token[i] or ";" in token[i]:
        expstmt()
    elif "{" in token[i]:
        compoundstmt()
    elif "if" in token[i]:
        selectionstmt()
    elif "while" in token[i]:
        itstmt()
    elif "return" in token[i]:
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
        if ";" in token[i]:
            i += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif y is True:
        exp()
        if ";" in token[i]:
            i += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif "(" in token[i]:
        exp()
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


def selectionstmt():  # 19
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

    exp()

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


def itstmt():  # 20
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

    exp()

    if ")" in token[i]:
        i += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    statement()


def retstmt():  # 21
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
    elif token[i] not in keywordchecklist and x is True:
        exp()
        if ";" in token[i]:
            i += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif y is True:
        exp()
        if ";" in token[i]:
            i += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif "(" in token[i]:
        exp()
        if ";" in token[i]:
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
    elif "(" in token[i]:
        i += 1  # Accept (
        exp()
        if ")" in token[i]:
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
            print("REJECT")
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
    if "=" in token[i]:
        i += 1  # Accept =
        exp()
    elif "[" in token[i]:
        i += 1  # Accept [
        exp()
        if "[" in token[i-1]:
            print("REJECT")
            sys.exit(0)
        if "]" in token[i]:
            i += 1  # Accept ]
            if "=" in token[i]:
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
    elif "(" in token[i]:
        i += 1  # Accept (
        args()
        if ")" in token[i]:
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
        # error begins
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
    if "[" in token[i]:
        i += 1  # Accept [
        exp()
        if "]" in token[i]:
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
        if "[" in token[i]:
            i += 1  # Accept [
            exp()
            if "]" in token[i]:
                i += 1  # Accept ]
            else:
                return
        elif "(" in token[i]:
            i += 1  # Accept (
            args()
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
        exp()
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
            args()
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


def args():  # 34
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        arglist()
    elif y is True:
        arglist()
    elif "(" in token[i]:
        arglist()
    elif ")" in token[i]:
        return
    else:
        return


def arglist():  # 35
    exp()
    arglistprime()


def arglistprime():  # 36
    global i
    if "," in token[i]:
        i += 1  # Accept ,
        exp()
        arglistprime()
    elif ")" in token[i]:
        return
    else:
        return


# ----------------------------- end of parsing functions --------------------------------- #

# begin parsing
program()