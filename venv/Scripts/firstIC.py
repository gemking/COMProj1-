import sys
import re


f = open(sys.argv[1], "r")  # open file and read contents into a list (without "\n")
filelines = f.read().splitlines()
f.close()


keywordchecklist = ["else", "if", "int", "return", "void", "while", "float"]  # list of all keywords

# our regular expressions for the lexical analyzer
wordsRegex = "[a-z]+"  # gets all words/ID's
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

q = 1  # Counter for quadruples list
t = 0  # counter for our temps in the quadruples

currentfunc = 0  # what the function we are currently in is
incurrentfunc = 0  # checks for scope inside a function
inexp = 0

iflistq = []
iflistqnum = 0
iflistfront = []
iflistback = []
iniflistq = 0
ifbr = 0
elsebr = 0

doublecheck = 0
whileendbr = 0
whilefirstbr = 0
lastw = 0
whilelistq = []   # list of quadruples done until end of while loop
wlistqnum = 0
inwlistq = 0
whilelistfront = []  # first half of the paramteres for while loop
whilelistback = []  # second half of the parameters for while loop

# --------------------------- print line for code generation ----------------------------- #
print("----------------------------------------------------")
# ---------------------------------- parsing functions ----------------------------------- #


def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def program():  # 1
    dl()
    if token[i] == "$":
        done = 1
        # print "ACCEPT"
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
    global i, q, currentfunc
    types()
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        funcparm = []
        if token[i-1] == "main":
            print(str(q).ljust(4) + "\tfunc \t\t" + token[i-1] + "\t\tvoid\t\t0")
            q += 1
            currentfunc = token[i-1]

        else:
            if token[i-2] == "void":
                if token[i+1] == "void":
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[i-1].ljust(4) + "\t\tvoid\t\t0")
                    q += 1
                    currentfunc = token[i-1]
                else:
                    f = i + 1
                    paramcount = 0
                    qch = q + 1
                    while token[f] != ")":
                        if token[f] == "int" or token[f] == "float":
                            paramcount += 1
                            funcparm.append(str(qch).ljust(4) + "\tparam\t\t4   \t\t\t\t\t" + token[f+1])
                            qch += 1
                            f += 2
                            if token[f] == ",":
                                f += 1
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[i-1].ljust(4) + "\t\t" + token[i-2].ljust(4) + "\t\t" + str(paramcount))
                    q = qch
                    for v in funcparm:
                        print(v)
                    currentfunc = token[i-1]

            else:
                if token[i+1] == "void":
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[i-1].ljust(4) + "\t\t" + token[i-2].ljust(4) + "\t\t0")
                    q += 1
                    currentfunc = token[i-1]
                else:
                    f = i + 1
                    paramcount = 0
                    qch = q + 1
                    while token[f] != ")":
                        if token[f] == "int" or token[f] == "float":
                            paramcount += 1
                            funcparm.append(str(qch).ljust(4) + "\tparam\t\t4   \t\t\t\t\t" + token[f+1])
                            qch += 1
                            f += 2
                            if token[f] == ",":
                                f += 1
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[i-1].ljust(4) + "\t\t" + token[i-2].ljust(4) + "\t\t" + str(paramcount))
                    q = qch
                    for v in funcparm:
                        print(v)
                    currentfunc = token[i-1]

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
    global i, q
    types()

    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID

        if token[i] != "[":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[i-1])
                q += 1
            elif iniflistq == 1:
                iflistq.append(str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[i-1])
                q += 1
            else:
                print(str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[i-1])
                q += 1

    else:
        print("REJECT")
        sys.exit(0)

    if token[i] == ";":
        i += 1  # Accept ;
    elif token[i] == "[":
        i += 1  # Accept [

        alloc = int(token[i]) * int(4)

        if inwlistq == 1:
            whilelistq.append(str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[i-2])
            q += 1
        elif iniflistq == 1:
            iflistq.append(str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[i-2])
            q += 1
        else:
            print(str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[i-2])
            q += 1

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
    if token[i] == "int" or token[i] == "float" or token[i] == "void":
        paramslist()
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
        if token[i] == "[":
            i += 1  # Accept [
            if token[i] == "]":
                i += 1  # Accept ]
                return
            else:
                print("REJECT")
                sys.exit(0)
    else:
        if token[i-1] == "void":
            return
        else:
            print("REJECT")
            sys.exit(0)


def compoundstmt():  # 12
    global i, currentfunc, q, incurrentfunc
    if token[i] == "{":
        i += 1  # Accept {
        incurrentfunc += 1

        if incurrentfunc > 1:
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tblock\t\t    \t\t    ")
                q += 1
            elif iniflistq == 1:
                iflistq.append(str(q).ljust(4) + "\tblock\t\t    \t\t    ")
                q += 1
            else:
                print(str(q).ljust(4) + "\tblock\t\t    \t\t    ")
                q += 1

    else:
        return

    localdeclarations()
    statementlist()

    if token[i] == "}":
        i += 1  # Accept }

        incurrentfunc -= 1
        if incurrentfunc > 0:
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tend  \t\tblock\t\t")
                q += 1
            elif iniflistq == 1:
                iflistq.append(str(q).ljust(4) + "\tend  \t\tblock\t\t")
                q += 1
            else:
                print(str(q).ljust(4) + "\tend  \t\tblock\t\t")
                q += 1

        if incurrentfunc == 0:
            print(str(q).ljust(4) + "\tend  \t\tfunc\t\t" + currentfunc)
            q += 1

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
    global i, ifbr, q, t, iniflistq
    if token[i] == "if":
        i += 1  # Accept if
    else:
        return

    if token[i] == "(":
        i += 1  # Accept (

        f = i
        iflistfront = ""
        comparison = 0
        bch = 0
        while token[f] != "<" and token[f] != "<=" and token[f] != ">" and token[f] != ">=" and token[f] != "==" and token[f] != "!=":
            if token[f] == "[" or bch == 1:
                iflistfront = iflistfront + token[f]
                bch = 1
                if token[f] == "]":
                    bch = 0
            else:
                iflistfront = iflistfront + " " + token[f]
            f += 1


        comparison = token[f]
        iflistfront = infixToPostfix(iflistfront)
        lastif = postfixEval(iflistfront)

        f += 1
        bch = 0
        iflistback = ""
        while token[f] != ")":
            if token[f] == "[" or bch == 1:
                iflistback = iflistback + token[f]
                bch = 1
                if token[f] == "]":
                    bch = 0
            else:
                iflistback = iflistback + " " + token[f]
            f += 1

        iflistback = infixToPostfix(iflistback)
        lastif1 = postfixEval(iflistback)

        print(str(q).ljust(4) + "\tcomp \t\t" + lastif.ljust(4) + "\t\t" + lastif1.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1

        if comparison == ">":
            print(str(q).ljust(4) + "\tBGT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == ">=":
            print(str(q).ljust(4) + "\tBGET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "<":
            print(str(q).ljust(4) + "\tBLT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "<=":
            print(str(q).ljust(4) + "\tBLET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "==":
            print(str(q).ljust(4) + "\tBEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        else:  # comparison == "!="
            print(str(q).ljust(4) + "\tBNEQ \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1

        iflistq.append(str(q).ljust(4) + "\tBR   \t\t\t\t\t\t\t\t")
        q += 1


    else:
        print("REJECT")
        sys.exit(0)

    exp()

    if token[i] == ")":
        i += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    iniflistq = 1

    statement()

    if token[i] == "else":
        iflistq[iflistqnum] = iflistq[iflistqnum] + str(q+1)
    else:
        iflistq[iflistqnum] = iflistq[iflistqnum] + str(q)
    elsech = 0

    for v in iflistq:
        print(v)
    iniflistq = 0

    if token[i] == "else":
        i += 1  # Accept else

        iflistq.append(str(q).ljust(4) + "\tBR   \t\t\t\t\t\t\t\t")
        elsech = len(iflistq)
        q += 1
        iniflistq = 1

        statement()

        iflistq[elsech-1] = iflistq[elsech-1] + str(q)

        for v in range(elsech-1, len(iflistq)):
            print(iflistq[v])
        iniflistq = 0

    else:
        return


def itstmt():  # 20
    global i, lastw, t, q, inwlistq, doublecheck, wlistqnum
    if token[i] == "while":
        i += 1  # Accept while
    else:
        return

    if token[i] == "(":
        i += 1  # Accept (

        whileendbr = q  # get start of while loop line for last quadruple in the block

        f = i
        wlistfront = ""
        comparison = 0
        bch = 0
        while token[f] != "<" and token[f] != "<=" and token[f] != ">" and token[f] != ">=" and token[f] != "==" and token[f] != "!=":
            if token[f] == "[" or bch == 1:
                wlistfront = wlistfront + token[f]
                bch = 1
                if token[f] == "]":
                    bch = 0
            else:
                wlistfront = wlistfront + " " + token[f]
            f += 1


        comparison = token[f]
        wlistfront = infixToPostfix(wlistfront)
        lastw = postfixEval(wlistfront)

        f += 1
        bch = 0
        wlistback = ""
        while token[f] != ")":
            if token[f] == "[" or bch == 1:
                wlistback = wlistback + token[f]
                bch = 1
                if token[f] == "]":
                    bch = 0
            else:
                wlistback = wlistback + " " + token[f]
            f += 1

        wlistback = infixToPostfix(wlistback)
        lastw1 = postfixEval(wlistback)

        if inwlistq == 1:
            whilelistq.append(str(q).ljust(4) + "\tcomp \t\t" + lastw.ljust(4) + "\t\t" + lastw1.ljust(4) + "\t\tt" + str(t))
        else:
            print(str(q).ljust(4) + "\tcomp \t\t" + lastw.ljust(4) + "\t\t" + lastw1.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1

        if comparison == ">":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBGT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBGT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == ">=":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBGET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBGET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "<":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBLT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBLT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "<=":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBLET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBLET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "==":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        else:  # comparison == "!="
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBNEQ \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBNEQ \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1

        whilelistq.append(str(q).ljust(4) + "\tBR   \t\t\t\t\t\t\t\t")
        q += 1

    else:
        print("REJECT")
        sys.exit(0)

    exp()

    if token[i] == ")":
        i += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)


    inwlistq = 1
    doublecheck += 1

    statement()
    doublecheck -= 1


    whilelistq[wlistqnum] = whilelistq[wlistqnum] + str(q + 1)  +"h"
    inwlistq = 0

    if doublecheck == 0:
        for v in whilelistq:
            print(v)

    if inwlistq == 1:
        whilelistq.append(str(q).ljust(4) + "\tBR  \t\t\t\t\t\t\t\t" + str(whileendbr))
    else:
        print(str(q).ljust(4) + "\tBR  \t\t\t\t\t\t\t\t" + str(whileendbr))
    q += 1


def retstmt():  # 21
    global i, q, t
    if token[i] == "return":
        i += 1  # Accept return
    else:
        return

    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] == ";":
        i += 1  # Accept ;

        print(str(q).ljust(4) + "\treturn\t\t    \t\t    ")
        q += 1
        return

    elif token[i] not in keywordchecklist and x is True:

        if token[i+1] == "[":
            f = i
            retexp = ""
            while token[f] != ";":
                retexp = retexp + token[f]
                f += 1

            h1 = retexp.partition('[')
            h2 = retexp.partition('[')[-1].rpartition(']')[0]
            if h2.isdigit() == False:
                print(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                h2 = temp
            else:
                h2 = int(h2) * 4
            print(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
            q += 1
            temp = "t" + str(t)
            t += 1

            print(str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + temp)
            q += 1

        else:
            print(str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + token[i])
            q += 1

        exp()

        if token[i] == ";":
            i += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)

    elif y is True:

        print(str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + token[i])
        q += 1

        exp()

        if token[i] == ";":
            i += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif token[i] == "(":

        f = i + 1
        bch = 0
        expret = ""
        while token[f] != ")":
            if token[f] == "[" or bch == 1:
                expret = expret + token[f]
                bch = 1
                if token[f] == "]":
                    bch = 0
            else:
                expret = expret + " " + token[f]
            f += 1

        expret = infixToPostfix(expret)
        lastexpret = postfixEval(expret)

        print(str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + lastexpret)
        q += 1

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
    global i, q, t, inexp
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID

        if token[i] == "[" and inexp == 0:
            f = i - 1
            check = ""
            while token[f] != "=":
                check = check + token[f]
                f += 1
            i = f
            assign = check

            if inwlistq == 1:
                h1 = assign.partition('[')
                h2 = assign.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                assign = temp

            elif iniflistq == 1:
                h1 = assign.partition('[')
                h2 = assign.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    iflistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                iflistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                assign = temp

            else:
                h1 = assign.partition('[')
                h2 = assign.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    print(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                print(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                assign = temp

        else:
            assign = token[i-1]

        if token[i] == "(" and inexp == 0:
            f = i
            exquad = token[i-1]
            while token[f] != ";":
                exquad = exquad + token[f]
                f += 1

            if inwlistq == 1:
                parmcount = 0
                h1 = exquad.partition('(')[-1].rpartition(')')[0]
                h2 = exquad.partition('(')
                if ',' in h1:
                    h1 = h1.split(',')
                for v in h1:
                    parmcount += 1
                    whilelistq.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                    q += 1

                whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                q += 1
                t += 1

            elif iniflistq == 1:
                parmcount = 0
                h1 = exquad.partition('(')[-1].rpartition(')')[0]
                h2 = exquad.partition('(')
                if ',' in h1:
                    h1 = h1.split(',')
                for v in h1:
                    parmcount += 1
                    iflistq.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                    q += 1

                iflistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                q += 1
                t += 1

            else:
                parmcount = 0
                h1 = exquad.partition('(')[-1].rpartition(')')[0]
                h2 = exquad.partition('(')
                if ',' in h1:
                    h1 = h1.split(',')
                for v in h1:
                    parmcount += 1
                    print(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                    q += 1

                print(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                q += 1
                t += 1

        if token[i] == "=":
            f = i + 1
            exquad = ""
            bch = 0
            pch = 0
            while token[f] != ";":
                if token[f] == "[" or bch == 1:
                    exquad = exquad + token[f]
                    bch = 1
                    if token[f] == "]":
                        bch = 0
                elif token[f] == "(" or pch == 1:
                    if token[f-1] != "*" and token[f-1] != "/" and token[f-1] != "+" and token[f-1] != "-" and token[f-1] != "=":
                        exquad = exquad + token[f]
                        pch = 1
                        if token[f] == ")":
                            pch = 0
                    else:
                        exquad = exquad + " " + token[f]
                else:
                    exquad = exquad + " " + token[f]
                f += 1
            exquad = infixToPostfix(exquad)
            lastexp = postfixEval(exquad)

            if inwlistq == 1:
                if "(" in lastexp:
                    parmcount = 0
                    h1 = lastexp.partition('(')[-1].rpartition(')')[0]
                    h2 = lastexp.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whilelistq.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    whilelistq.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

                elif "[" in lastexp:
                    h1 = lastexp.partition('[')
                    h2 = lastexp.partition('[')[-1].rpartition(']')[0]
                    if h2.isdigit() == False:
                        whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                        q += 1
                        temp = "t" + str(t)
                        t += 1
                        h2 = temp
                    else:
                        h2 = int(h2) * 4
                    whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1

                    whilelistq.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

                else:
                    whilelistq.append(str(q).ljust(4) + "\tassgn\t\t" + lastexp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

            elif iniflistq == 1:
                if "(" in lastexp:
                    parmcount = 0
                    h1 = lastexp.partition('(')[-1].rpartition(')')[0]
                    h2 = lastexp.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        iflistq.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    iflistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    iflistq.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

                elif "[" in lastexp:
                    h1 = lastexp.partition('[')
                    h2 = lastexp.partition('[')[-1].rpartition(']')[0]
                    if h2.isdigit() == False:
                        iflistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                        q += 1
                        temp = "t" + str(t)
                        t += 1
                        h2 = temp
                    else:
                        h2 = int(h2) * 4
                    iflistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1

                    iflistq.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

                else:
                    iflistq.append(str(q).ljust(4) + "\tassgn\t\t" + lastexp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp =1

            else:
                if "(" in lastexp:
                    parmcount = 0
                    h1 = lastexp.partition('(')[-1].rpartition(')')[0]
                    h2 = lastexp.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        print(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    print(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    print(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp =1

                elif "[" in lastexp:
                    h1 = lastexp.partition('[')
                    h2 = lastexp.partition('[')[-1].rpartition(']')[0]
                    if h2.isdigit() == False:
                        print(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                        q += 1
                        temp = "t" + str(t)
                        t += 1
                        h2 = temp
                    else:
                        h2 = int(h2) * 4
                    print(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1

                    print(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

                else:
                    print(str(q).ljust(4) + "\tassgn\t\t" + lastexp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

        ex()
        inexp = 0

    elif token[i] == "(":
        i += 1  # Accept (
        exp()
        if token[i] == ")":
            i += 1  # Accept )
            termprime()
            addexpprime()
            if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                           token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
            elif token[i] == "+" or token[i] == "-":
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                             token[i] == ">=" or token[i] == "==" or token[i] == "!=":
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
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            addexp()
        elif token[i] == "+" or token[i] == "-":
            addexpprime()
            if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                           token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
        elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                         token[i] == ">=" or token[i] == "==" or token[i] == "!=":
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
            elif token[i] == "*" or token[i] == "/":
                termprime()
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
                else:
                    return
            elif token[i] == "+" or token[i] == "-":
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                             token[i] == ">=" or token[i] == "==" or token[i] == "!=":
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
            if token[i] == "*" or token[i] == "/":
                termprime()
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
                else:
                    return
            elif token[i] == "+" or token[i] == "-":
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                             token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
            else:
                return
        else:
            print("REJECT")
            sys.exit(0)
    elif token[i] == "*" or token[i] == "/":
        termprime()
        addexpprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            addexp()
        else:
            return
    elif token[i] == "+" or token[i] == "-":
        addexpprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            addexp()
        else:
            return
    elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                     token[i] == ">=" or token[i] == "==" or token[i] == "!=":
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
    if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                   token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        relop()
        addexp()
    else:
        return


def relop():  # 25
    global i
    if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                   token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        i += 1  # Accept <=, <, >, >=, ==, or !=
    else:
        return


def addexp():  # 26
    term()
    addexpprime()


def addexpprime():  # 27
    if token[i] == "+" or token[i] == "-":
        addop()
        term()
        addexpprime()
    else:
        return


def addop():  # 28
    global i
    if token[i] == "+" or token[i] == "-":
        i += 1  # Accept +, -
    else:
        return


def term():  # 29
    factor()
    termprime()


def termprime():  # 30
    if token[i] == "*" or token[i] == "/":
        mulop()
        factor()
        termprime()
    else:
        return


def mulop():  # 31
    global i
    if token[i] == "*" or token[i] == "/":
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
# ---------------------------- stack for infix to postfix -------------------------------- #

# turn infix to postfix
def infixToPostfix(infixexpr):  # turn infix to postfix
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token.isalnum() or "[" in token or ("(" in token and ")" in token) or (re.search('[a-z]', token) == True and "(" in token) or token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789" or token in "abcdefghijklmnopqrstuvwxyz":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)

# perform quadruples in postfix correct order
def postfixEval(postfixExpr):
    operandStack = Stack()
    tokenList = postfixExpr.split()

    for token in tokenList:
        if token.isalnum() or "[" in token or ("(" in token and ")" in token) or (re.search('[a-z]', token) == True and "(" in token) or token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789" or token in "abcdefghijklmnopqrstuvwxyz":
            operandStack.push(token)
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            result = doMath(token,operand1,operand2)
            operandStack.push(result)
    return operandStack.pop()

def doMath(op, op1, op2):
    global q, t

    if op == "*":
        if inwlistq == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whilelistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whilelistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        elif iniflistq == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        iflistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    iflistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        iflistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    iflistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    iflistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                iflistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    iflistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                iflistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            iflistq.append(str(q).ljust(4) + "\tmult \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        else:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        print(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    print(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        print(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    print(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    print(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                print(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    print(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                print(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            print(str(q).ljust(4) + "\tmult \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1
        return temp

    elif op == "/":
        if inwlistq == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whilelistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whilelistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            whilelistq.append(str(q).ljust(4) + "\tdiv  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        elif iniflistq == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        iflistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    iflistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        iflistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    iflistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    iflistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                iflistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    iflistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                iflistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            iflistq.append(str(q).ljust(4) + "\tdiv  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        else:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        print(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    print(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        print(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    print(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    print(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                print(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    print(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                print(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            print(str(q).ljust(4) + "\tdiv  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1
        return temp

    elif op == "+":
        if inwlistq == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whilelistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whilelistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp

            whilelistq.append(str(q).ljust(4) + "\tadd  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        elif iniflistq == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        iflistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    iflistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        iflistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    iflistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    iflistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                iflistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    iflistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                iflistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp

            iflistq.append(str(q).ljust(4) + "\tadd  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        else:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        print(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    print(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        print(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    print(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    print(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                print(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    print(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                print(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp

            print(str(q).ljust(4) + "\tadd  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1
        return temp

    else:  # if op == "-"
        if inwlistq == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whilelistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whilelistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            whilelistq.append(str(q).ljust(4) + "\tsub  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        elif iniflistq == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        iflistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    iflistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        iflistq.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    iflistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    iflistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                iflistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    iflistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                iflistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            iflistq.append(str(q).ljust(4) + "\tsub  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        else:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        print(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    print(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op1 = temp

            if "(" in op2:
                    parmcount = 0
                    h1 = op2.partition('(')[-1].rpartition(')')[0]
                    h2 = op2.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        print(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    print(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    print(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                print(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    print(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                print(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            print(str(q).ljust(4) + "\tsub  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1
        return temp


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

# ---------------------- end of our stack for infix to postfix --------------------------- #

# begin parsing
program()
print("----------------------------------------------------")