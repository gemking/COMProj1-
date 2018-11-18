import sys
import re

with open(sys.argv[1], "r") as file:  # opens file
    filelines = file.read().splitlines()  # reads file and splits lines
    file.close()  # closes file

insideComment = 0

keywordchecklist = ["if", "else", "while", "int", "float", "void", "return"]  # denotes all keywords
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
            if word[0] in keywordchecklist:
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
    if token[x] == "$":
        done = 1
        # print "ACCEPT"
    else:
        print("REJECT")


def dl():  # 2
    declaration()
    dlprime()


def dlprime():  # 3
    if token[x] == "int" or token[x] == "void" or token[x] == "float":
        declaration()
        dlprime()
    elif token[x] == "$":
        return
    else:
        return


def declaration():  # 4
    global x
    global q
    global currentfunc
    types()
    w = token[x].isalpha()
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID
        funcparm = []
        if token[x-1] == "main":
            print(str(q).ljust(4) + "\tfunc \t\t" + token[x-1] + "\t\tvoid\t\t0")
            q += 1
            currentfunc = token[x-1]

        else:
            if token[x-2] == "void":
                if token[x+1] == "void":
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[x-1].ljust(4) + "\t\tvoid\t\t0")
                    q += 1
                    currentfunc = token[x-1]
                else:
                    f = x + 1
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
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[x-1].ljust(4) + "\t\t" + token[x-2].ljust(4) + "\t\t" + str(paramcount))
                    q = qch
                    for v in funcparm:
                        print(v)
                    currentfunc = token[x-1]

            else:
                if token[i+1] == "void":
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[x-1].ljust(4) + "\t\t" + token[x-2].ljust(4) + "\t\t0")
                    q += 1
                    currentfunc = token[x-1]
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
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[x-1].ljust(4) + "\t\t" + token[x-2].ljust(4) + "\t\t" + str(paramcount))
                    q = qch
                    for v in funcparm:
                        print(v)
                    currentfunc = token[x-1]

        if token[x] == ";":
            x += 1  # Accept ;
        elif token[x] == "[":
            x += 1  # Accept [
            y = hasnum(token[x])
            if y is True:
                x += 1  # Accept NUM/FLOAT
                if token[i] == "]":
                    x += 1  # Accept ]
                    if token[i] == ";":
                        x += 1  # Accept ;
                    else:
                        print("REJECT")
                        sys.exit(0)
                else:
                    print("REJECT")
                    sys.exit(0)
            else:
                print("REJECT")
                sys.exit(0)
        elif token[x] == "(":
            x += 1  # Accept (
            params()
            if token[x] == ")":
                x += 1  # Accept )
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
    global x
    global q
    types()

    w = token[x].isalpha()
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID

        if token[x] != "[":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[x-1])
                q += 1
            elif iniflistq == 1:
                iflistq.append(str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[x-1])
                q += 1
            else:
                print(str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[x-1])
                q += 1

    else:
        print("REJECT")
        sys.exit(0)

    if token[x] == ";":
        x += 1  # Accept ;
    elif token[i] == "[":
        x += 1  # Accept [

        alloc = int(token[i]) * int(4)

        if inwlistq == 1:
            whilelistq.append(str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[x-2])
            q += 1
        elif iniflistq == 1:
            iflistq.append(str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[x-2])
            q += 1
        else:
            print(str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[x-2])
            q += 1

        w = hasnum(token[x])
        if w is True:
            x += 1  # Accept NUM/FLOAT
            if token[x] == "]":
                x += 1  # Accept ]
                if token[x] == ";":
                    x += 1  # Accept ;
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
    global x
    if token[x] == "int" or token[x] == "void" or token[x] == "float":
        x += 1  # Accept int/void/float
    else:
        return


def fd():  # 7
    global x
    types()

    w = token[x].isalpha()
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID
    else:
        return

    if token[x] == "(":
        x += 1  # Accept (
    else:
        print("REJECT")
        sys.exit(0)

    params()

    if token[x] == ")":
        x += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    compoundstmt()


def params():  # 8
    global x
    if token[x] == "int" or token[x] == "float" or token[x] == "void":
        paramslist()
    else:
        print("REJECT")
        sys.exit(0)


def paramslist():  # 9
    param()
    paramslistprime()


def paramslistprime():  # 10
    global x
    if token[x] == ",":
        x += 1  # Accept ,
        param()
        paramslistprime()
    elif token[x] == ")":
        return
    else:
        return


def param():  # 11
    global x
    types()
    w = token[x].isalpha()
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID
        if token[x] == "[":
            x += 1  # Accept [
            if token[i] == "]":
                x += 1  # Accept ]
                return
            else:
                print("REJECT")
                sys.exit(0)
    else:
        if token[x-1] == "void":
            return
        else:
            print("REJECT")
            sys.exit(0)


def compoundstmt():  # 12
    global x
    global currentfunc
    global q
    global incurrentfunc
    if token[x] == "{":
        x += 1  # Accept {
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

    if token[x] == "}":
        x += 1  # Accept }

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
    if token[x] == "int" or token[x] == "void" or token[x] == "float":
        vd()
        localdeclarationsprime()
    else:
        return


def statementlist():  # 15
    statementlistprime()


def statementlistprime():  # 16
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywordchecklist and w is True:
        statement()
        statementlistprime()
    elif z is True:
        statement()
        statementlistprime()
    elif token[x] == "(" or token[x] == ";" or token[x] == "{" or token[x] == "if" or\
                     token[x] == "while" or token[x] == "return":
        statement()
        statementlistprime()
    elif token[x] == "}":
        return
    else:
        return


def statement():  # 17
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywordchecklist and w is True:
        expstmt()
    elif z is True:
        expstmt()
    elif token[x] == "(" or token[x] == ";":
        expstmt()
    elif token[x] == "{":
        compoundstmt()
    elif token[x] == "if":
        selectionstmt()
    elif token[x] == "while":
        itstmt()
    elif token[x] == "return":
        retstmt()
    else:
        print("REJECT")
        sys.exit(0)


def expstmt():  # 18
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywordchecklist and w is True:
        exp()
        if token[x] == ";":
            x += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif z is True:
        exp()
        if token[x] == ";":
            x += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif token[x] == "(":
        exp()
        if token[x] == ";":
            x += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif token[x] == ";":
        x += 1  # Accept ;
    else:
        print("REJECT")
        sys.exit(0)


def selectionstmt():  # 19
    global x
    global ifbr
    global q
    global t
    global iniflistq
    if token[x] == "if":
        x += 1  # Accept if
    else:
        return

    if token[x] == "(":
        x += 1  # Accept (

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

    if token[x] == ")":
        x += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    iniflistq = 1

    statement()

    if token[x] == "else":
        iflistq[iflistqnum] = iflistq[iflistqnum] + str(q+1)
    else:
        iflistq[iflistqnum] = iflistq[iflistqnum] + str(q)
    elsech = 0

    for v in iflistq:
        print(v)
    iniflistq = 0

    if token[x] == "else":
        x += 1  # Accept else

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
    global x
    global lastw
    global t
    global q
    global inwlistq
    global doublecheck
    global wlistqnum
    if token[x] == "while":
        x += 1  # Accept while
    else:
        return

    if token[x] == "(":
        x += 1  # Accept (

        whileendbr = q  # get start of while loop line for last quadruple in the block

        f = x
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

    if token[x] == ")":
        x += 1  # Accept )
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
    global x
    global q
    global t
    if token[x] == "return":
        x += 1  # Accept return
    else:
        return

    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] == ";":
        x += 1  # Accept ;

        print(str(q).ljust(4) + "\treturn\t\t    \t\t    ")
        q += 1
        return

    elif token[x] not in keywordchecklist and w is True:

        if token[x+1] == "[":
            f = x
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
            print(str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + token[x])
            q += 1

        exp()

        if token[x] == ";":
            x += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)

    elif z is True:

        print(str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + token[x])
        q += 1

        exp()

        if token[x] == ";":
            x += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif token[x] == "(":

        f = x + 1
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

        if token[x] == ";":
            x += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    else:
        print("REJECT")
        sys.exit(0)


def exp():  # 22
    global x
    global q
    global t
    global inexp
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID

        if token[x] == "[" and inexp == 0:
            f = x - 1
            check = ""
            while token[f] != "=":
                check = check + token[f]
                f += 1
            x = f
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
            assign = token[x-1]

        if token[x] == "(" and inexp == 0:
            f = x
            exquad = token[x-1]
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

        if token[x] == "=":
            f = x + 1
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

    elif token[x] == "(":
        x += 1  # Accept (
        exp()
        if token[x] == ")":
            x += 1  # Accept )
            termprime()
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
            sys.exit(0)
    elif z is True:
        x += 1  # Accept NUM/FLOAT
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
        sys.exit(0)


def ex():  # 22X
    global x
    if token[x] == "=":
        x += 1  # Accept =
        exp()
    elif token[x] == "[":
        x += 1  # Accept [
        exp()
        if token[x-1] == "[":
            print("REJECT")
            sys.exit(0)
        if token[x] == "]":
            x += 1  # Accept ]
            if token[x] == "=":
                x += 1  # Accept =
                exp()
            elif token[x] in multiplicationDivisionSymbols:
                termPrime()
                addexpprime()
                if token[x] in comparisionSymbols:
                    simpleExpressionPrime()
            elif token[x] in additionSubtractionSymbols:
                addexpprime()
                if token[x] in comparisionSymbols:
                    simpleExpressionPrime()
            elif token[x] in comparisionSymbols:
                simpleExpressionPrime()
        else:
            print("REJECT")
            sys.exit(0)
    elif token[x] == "(":
        x += 1  # Accept (
        args()
        if token[x] == ")":
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
            sys.exit(0)
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


def var():  # 23
    global x
    w = token[x].isalpha()
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID
    else:
        return
    if token[x] == "[":
        x += 1  # Accept [
        exp()
        if token[x] == "]":
            x += 1  # Accept ]
        else:
            print("REJECT")
            sys.exit(0)
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

def term():  # 29
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


def factor():  # 32
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID
        if token[x] == "[":
            x += 1  # Accept [
            exp()
            if token[x] == "]":
                x += 1  # Accept ]
            else:
                return
        elif token[x] == "(":
            x += 1  # Accept (
            args()
            if token[x] == ")":
                x += 1  # Accept )
            else:
                return
        else:
            return
    elif z is True:
        x += 1  # Accept NUM/FLOAT
    elif token[x] == "(":
        x += 1  # Accept (
        exp()
        if token[x] == ")":
            x += 1  # Accept )
        else:
            return
    else:
        print("REJECT")
        sys.exit(0)


def call():  # 33
    global x
    w = token[x].isalpha()
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID
        if token[x] == "(":
            x += 1  # Accept (
            args()
            if token[x] == ")":
                x += 1  # Accept )
            else:
                print("REJECT")
                sys.exit(0)
        else:
            print("REJECT")
            sys.exit(0)
    else:
        return


def args():  # 34
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywordchecklist and w is True:
        arglist()
    elif z is True:
        arglist()
    elif token[x] == "(":
        arglist()
    elif token[x] == ")":
        return
    else:
        return


def arglist():  # 35
    exp()
    arglistprime()


def arglistprime():  # 36
    global x
    if token[x] == ",":
        x += 1  # Accept ,
        exp()
        arglistprime()
    elif token[x] == ")":
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
    global q
    global t

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