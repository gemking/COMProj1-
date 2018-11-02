import sys
import re
with open(sys.argv[1], "r") as file: #opens file
    filelines = file.read().splitlines() # reads file and splits lines
    file.close() #closes file


insideComment = 0


keywords = ["if", "else", "while", "int", "float", "void", "return"] #denotes all keywords
symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]" #denotes symbols used
comparisionSymbols = ["==","<=",">=","!=","<",">"]
additionSubtractionSymbols = ["-","+"]
multiplicationDivisionSymbols = ["/", "*"]
miniKeywords = ["void", "int", "float"]
miniKeywordsTwo = ["while", "if", "return", "(", ";", "{"]
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

token.append("$")  # add to end to check if done parsing
ismain = 0  # check for 1 main function
lastmain = 0  # check if main is last function
done = 0
exc0 = 0
exc1 = 0
excret = 0
parammatch = 0
parm = 0

vardec = []  # list to hold declared variables, type, and scope
vartype = []  # list of type of variables
varop = []  # check for operand and operator agreement, i.e. int x; x = "hi"
vars = []  # list to hold all declared variables
varscope = []  # list of all variable scopes, as in what functions they are in
varscopen = []  # list of all variable scopes, as in block number

fundec = []  # list to hold declared functions with parms/args
fundeci = 0  # index to keep track of parameters/args for a function
funcall = []  # functions called
funcallargs = []  # list of argument types in a function's parameters
funnames = []  # list of all function names
funtypes = []  # list of all function types
funname = 0  # function name, for scope
funtype = 0  # function type, determine if it needs return
curscope = 0  # current scope
funret = 0  # does function have a return
funret = 0  # check if int/float function has return

# ---------------------------------- parsing functions ----------------------------------- #


def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def programDeclaration(): #runs program(Rule 1)
    global done
    declarationList()
    if "$" in token[x]:
        done = 1 #continues outside
    else:
        print ("REJECT") #if not, Reject


def declarationList(): #Rule 2
    declaration()
    declarationListPrime()


def declarationListPrime(): #Rule 3
    if token[x] in miniKeywords:
        declaration()
        declarationListPrime()
    elif "$" in token[x]:
        return
    else:
        return


def declaration():  # 4
    global x, ismain, funname, curscope, funtype, funret, lastmain
    types()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        if "main" in token[x]:
            ismain += 1
            lastmain = 1
            if token[x-1] != "void":
                print("REJECT")
                sys.exit(0)
        else:
            lastmain = 0

        x += 1  # Accept ID
        if ";" in token[x]:
            x += 1  # Accept ;
            k = 0
            for v in vars:  # check for duplicate declared variables
                if token[x-2] == v:
                    if vartype[k] == token[x-3]:
                        print("REJECT")
                        sys.exit(0)
                k += 1

            vardec.append(token[x-3] + " " + token[x-2] + " global 0")
            vars.append(token[x-2])
            vartype.append(token[x-3])
            varscope.append("global")
            varscopen.append(0)

            if token[x-3] == "void":
                print("REJECT")
                sys.exit(0)

        elif token[x] == "[":
            x += 1  # Accept [
            k = 0
            for v in vars:  # check for duplicate declared variables
                if token[x-2] == v:
                    if vartype[k] == token[x-3]:
                        print("REJECT")
                        sys.exit(0)
                k += 1

            vardec.append(token[x-3] + " " + token[x-2] + " global 0")
            vars.append(token[x-2])
            vartype.append(token[x-3])
            varscope.append("global")
            varscopen.append(0)

            if token[x-3] == "void":
                print("REJECT")
                sys.exit(0)

            z = hasnum(token[x])
            if z is True:
                x += 1  # Accept NUM/FLOAT
                if token[x] == "]":
                    x += 1  # Accept ]
                    if token[x] == ";":
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
            for v in fundec:  # check for duplicate declared functions
                if token[x-2] in v:
                    print("REJECT")
                    sys.exit(0)
            fundec.append(token[x-3] + " " + token[x-2])
            funname = token[x-2]
            funnames.append(token[x-2])
            funtypes.append(token[x-3])
            funtype = token[x-3]
            funret = 0
            curscope = 0

            params()

            if token[x] == ")":
                x += 1  # Accept )
                compoundstmt()

                if funret == 0 and funtype == "int":
                    print("REJECT")
                    sys.exit(0)
                elif funret == 0 and funtype == "float":
                    print("REJECT")
                    sys.exit(0)
                else:
                    funret = 0

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
    global x, ismain
    types()

    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        k = 0
        for v in vars:  # check for duplicate declared variables
            if token[x-1] == v:
                if varscope[k] == funname:
                    if varscopen[k] >= curscope:
                        print("REJECT")
                        sys.exit(0)
            k += 1
        vardec.append(token[x-2] + " " + token[x-1] + " " + str(funname) + " " + str(curscope))
        vars.append(token[x-1])
        vartype.append(token[x-2])
        varscope.append(funname)
        varscopen.append(curscope)

        if token[x-2] == "void":  # check if ID is type void
            print("REJECT")
            sys.exit(0)
    else:
        print("REJECT")
        sys.exit(0)

    if token[x] == ";":
        x += 1  # Accept ;
    elif token[x] == "[":
        x += 1  # Accept [
        w = hasnum(token[x])
        if w is True:
            x += 1  # Accept NUM/FLOAT
            if "." in token[x-1]:  # check for float in array declaration
                print("REJECT")
                sys.exit(0)
            if "E" in token[x-1]:  # check for float in array declaration
                print("REJECT")
                sys.exit(0)
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
    if token[x] in miniKeywords:
        x += 1  # Accept int/void/float
    else:
        return


def fd():  # 7
    global x, ismain
    types()

    w = token[x].isalpha()
    if token[x] not in keywordchecklist and w is True:
        if token[x] == "main":
            ismain += 1
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
    global x, fundeci
    if token[x] in miniKeywords:
        paramslist()
        fundeci += 1
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
    global x, funname, curscope
    types()
    fundec[fundeci] = fundec[fundeci] + " " + token[x-1]
    funcallargs.append("")
    funcallargs[fundeci] = funcallargs[fundeci] + " " + token[x-1]
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        fundec[fundeci] = fundec[fundeci] + " " + token[x-1]

        k = 0
        m = 0
        mc = 0
        ch = 0
        for v in vars:  # check for duplicate declared variables and with scope
            if token[x-1] == v:
                if varscope[k] != "global" and varscope[k] != funname:
                    ch = 1
                    continue
                if varscope[k] == "global":
                    m = k
                    mc = 1
                    break
            k += 1

        curscope = 1
        if not varscope:
            ch = 1
        if ch == 0 and varscope[m] == "global" and mc == 1:
            vardec.append(token[x-2] + " " + token[x-1] + " global 0")
            vars.append(token[x-1])
            vartype.append(token[x-2])
            varscope.append("global")
            varscopen.append(0)

        else:
            vardec.append(token[x-2] + " " + token[x-1] + " " + str(funname) + " " + str(curscope))
            vars.append(token[x-1])
            vartype.append(token[x-2])
            varscope.append(funname)
            varscopen.append(curscope)

        curscope = 0

        if token[x] == "[":
            x += 1  # Accept [
            if token[x] == "]":
                x += 1  # Accept ]
                return
            else:
                print("REJECT")
                sys.exit(0)
        else:
            return
    else:
        if token[x-1] == "void":
            return
        else:
            print("REJECT")
            sys.exit(0)


def compoundstmt():  # 12
    global x, curscope
    if token[x] == "{":
        x += 1  # Accept {
        curscope += 1
    else:
        return

    localdeclarations()
    statementlist()

    if token[x] == "}":
        x += 1  # Accept }
    else:
        print("REJECT")
        sys.exit(0)


def localdeclarations():  # 13
    localdeclarationsprime()


def localdeclarationsprime():  # 14
    if token[x] in miniKeywords:
        vd()
        localdeclarationsprime()
    else:
        return


def statementlist():  # 15
    statementlistprime()


def statementlistprime():  # 16
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        statement()
        statementlistprime()
    elif z is True:
        statement()
        statementlistprime()
    elif token[x] in miniKeywordsTwo:
        statement()
        statementlistprime()
    elif token[x] == "}":
        return
    else:
        return


def statement():  # 17
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
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
    if token[x] not in keywords and w is True:
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
    if token[x] == "if":
        x += 1  # Accept if
    else:
        return

    if token[x] == "(":
        x += 1  # Accept (
    else:
        print("REJECT")
        sys.exit(0)

    exp()
    if token[x] == ")":
        x += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)
    statement()
    if token[x] == "else":
        x += 1  # Accept else
        statement()
    else:
        return


def itstmt():  # 20
    global x
    if token[x] == "while":
        x += 1  # Accept while
    else:
        return

    if token[x] == "(":
        x += 1  # Accept (
    else:
        print("REJECT")
        sys.exit(0)

    exp()

    if token[x] == ")":
        x += 1  # Accept )
    else:
        print("REJECT")
        sys.exit(0)

    statement()


def retstmt():  # 21
    global x, excret, exptype, funret
    if token[x] == "return":
        x += 1  # Accept return
        if funtype == "int":
            funret = 1
        else:
            funret = 1
    else:
        return
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] == ";":
        x += 1  # Accept ;
        if funtype != "void":  # check if int or float function does not return a value
            print("REJECT")
            sys.exit(0)
        return
    elif token[x] not in keywords and w is True:
        if funtype == "void":  # check if void has return with value
            print("REJECT")
            sys.exit(0)

        if funtype == "int":
            exptype = "int"
        else:
            exptype = "float"
        excret = 1
        exp()
        excret = 0

        if token[x] == ";":
            x += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif z is True:
        if funtype == "void":  # check if void has return with value
            print("REJECT")
            sys.exit(0)

        if funtype == "int":
            exptype = "int"
        else:
            exptype = "float"
        excret = 1

        exp()
        excret = 0
        if token[x] == ";":
            x += 1  # Accept ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif token[x] == "(":
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
    global x, exptype, exc1, exc0, excret, parammatch, parm
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        if parm == 1:
            o = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v == token[x-1]:
                    check = vartype[o]
                o += 1
            parammatch = parammatch + " " + check

        if exc0 == 1 and parm == 0:
            if "(" in token[x]:
                o = 0
                check = 0
                for v in funnames:  # get the type of the function for operand/operator checking
                    if v == token[x-1]:
                        check = funtypes[o]
                    o += 1
                if exptype != check:
                    print("REJECT")
                    sys.exit(0)

            else:
                o = 0
                ch = 0
                check = 0
                for v in vars:  # check variable before checking if operator/operand agree
                    if v == token[x-1]:
                        if varscope[o] != "global" and varscope[o] != funname:
                            ch = 1
                        if varscope[o] == funname:
                            ch = 0
                            check = vartype[o]
                            break
                        check = vartype[o]
                    o += 1
                if ch == 1:
                    print("REJECT")
                    sys.exit(0)
                if exptype != check:
                    print("REJECT")
                    sys.exit(0)

        if exc1 == 1:
            o = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v == token[x-1]:
                    check = vartype[o]
                o += 1
            if exptype != check:
                print("REJECT")
                sys.exit(0)

        if excret == 1:
            o = 0
            check = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v == token[x-1]:
                    check = vartype[o]
                o += 1
            if exptype != check:
                print("REJECT")
                sys.exit(0)

        if "(" in token[x] and exc0 == 0 and parm == 0:
            if token[x-1] not in funnames:
                print("REJECT")
                sys.exit(0)

        ch = 0
        k = 0
        for v in vars:  # check for duplicate declared variables
            if token[x-1] == v:
                if varscope[k] != funname and varscope[k] != "global":
                    ch = 1
                if varscope[k] == funname:
                    ch = 0
            k += 1

        if token[x-1] not in vars and token[x] != "(":
            print("REJECT")
            sys.exit(0)

        if ch == 1:
            print("REJECT")
            sys.exit(0)

        ex()

    elif token[x] == "(":
        x += 1  # Accept (
        exp()
        if token[x] == ")":
            x += 1  # Accept )
            termprime()
            addexpprime()
            if token[x] in comparisionSymbols:
                simexpprime()
            elif token[x] in additionSubtractionSymbols:
                addexpprime()
                if token[x] in comparisionSymbols:
                    simexpprime()
            elif token[x] in comparisionSymbols:
                simexpprime()
        else:
            print("REJECT")
            sys.exit(0)
    elif z is True:
        x += 1  # Accept NUM/FLOAT
        if parm == 1:
            if "." in token[x-1]:
                parammatch = parammatch + " float"
            elif "E" in token[x-1]:
                parammatch = parammatch + " float"
            else:
                parammatch = parammatch + " int"

        ch = 0
        if "." in token[x-1]:
            ch = 1
        if "E" in token[x-1]:
            ch = 1

        if excret == 1 and ch == 1:
            if exptype != "float":
                print("REJECT")
                sys.exit(0)

        if excret == 1 and ch == 0:
            if exptype != "int":
                print("REJECT")
                sys.exit(0)

        if exc1 == 1 and "E" in token[x-1]:
            print("REJECT")
            sys.exit(0)
        if exc1 == 1 and "." in token[x-1]:
            print("REJECT")
            sys.exit(0)

        if exc0 == 1:
            if ch != 1 and exptype == "float":
                if "." not in token[x+1] and "E" not in token[x+1]:
                    print("REJECT")
                    sys.exit(0)

        termprime()
        addexpprime()
        if token[x] in comparisionSymbols:
            simexpprime()
        elif token[x] in additionSubtractionSymbols:
            addexpprime()
            if token[x] in comparisionSymbols:
                simexpprime()
        elif token[x] in comparisionSymbols:
                simexpprime()
    else:
        print("REJECT")
        sys.exit(0)


def ex():  # 22X
    global x, exptype, exc1, exc0, parm, parammatch
    if token[x] == "=":
        x += 1  # Accept =
        k = 0
        for v in vars:  # find the type of the first ID for the exp
            if token[x-2] == v:
                exptype = vartype[k]
                exc0 = 1
            k += 1
        exp()
        exc0 = 0
    elif token[x] == "[":
        x += 1  # Accept [
        exptype = "int"
        exc1 = 1
        exp()
        exc1 = 0
        if token[x-1] == "[":
            print("REJECT")
            sys.exit(0)
        if token[x] == "]":
            x += 1  # Accept ]
            if token[x] == "=":
                x += 1  # Accept =
                exp()
            elif token[x] in multiplicationDivisionSymbols:
                termprime()
                addexpprime()
                if token[x] in comparisionSymbols:
                    simexpprime()
            elif token[x] in additionSubtractionSymbols:
                addexpprime()
                if token[x] in comparisionSymbols:
                   simexpprime()
            elif token[x] in comparisionSymbols:
                simexpprime()
        else:
            print("REJECT")
            sys.exit(0)
    elif "(" in token[x]:
        x += 1  # Accept (
        k = 0
        for v in funnames:
            if v == token[x-2]:
                break
            k += 1
        args()
        parm = 0
        u = 0
        if not parammatch:
            u = 1
        if u == 0 and funcallargs[k] != parammatch:
            print("REJECT")
            sys.exit(0)

        if ")" in token[x]:
            x += 1  # Accept )
            if token[x] in multiplicationDivisionSymbols:
                termprime()
                addexpprime()
                if token[x] in comparisionSymbols:
                    simexpprime()
            elif token[x] in additionSubtractionSymbols:
                addexpprime()
                if token[x] in comparisionSymbols:
                    simexpprime()
            elif token[x] in comparisionSymbols:
                simexpprime()
        else:
            print("REJECT")
            sys.exit(0)
    elif token[x] in multiplicationDivisionSymbols:
        termprime()
        addexpprime()
        if token[x] in comparisionSymbols:
             simexpprime()
    elif token[x] in additionSubtractionSymbols:
        addexpprime()
        if token[x] in comparisionSymbols:
            simexpprime()
    elif token[x] in comparisionSymbols:
            simexpprime()


def var():  # 23
    global x
    w = token[x].isalpha()
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID
    else:
        return
    if "[" in token[x]:
        x += 1  # Accept [
        exp()
        if "]" in token[x]:
            x += 1  # Accept ]
        else:
            print("REJECT")
            sys.exit(0)
    else:
        return


def simexp():  # 24
    addexp()
    simexpprime()

def simexpprime():
    if token[x] in comparisionSymbols:
        relop()
        addexp()
    else:
        return


def relop():  # 25
    global x
    if token[x] in comparisionSymbols:
        x += 1  # Accept <=, <, >, >=, ==, or !=
    else:
        return


def addexp():  # 26
    term()
    addexpprime()


def addexpprime():  # 27
    if token[x] in additionSubtractionSymbols:
        addop()
        term()
        addexpprime()
    else:
        return


def addop():  # 28
    global x
    if token[x] in additionSubtractionSymbols:
        x += 1  # Accept +, -
    else:
        return


def term():  # 29
    factor()
    termprime()


def termprime():  # 30
    if token[x] in multiplicationDivisionSymbols:
        mulop()
        factor()
        termprime()
    else:
        return


def mulop():  # 31
    global x
    if token[x] in multiplicationDivisionSymbols:
        x += 1  # Accept *, /
    else:
        return


def factor():  # 32
    global x, exc0, excret
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID

        if exc0 == 1:
            o = 0
            ch = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v == token[x-1]:
                    if varscope[o] != "global" and varscope[o] != funname:
                        ch = 1
                    if varscope[o] == funname:
                        ch = 0
                        check = vartype[o]
                        break
                    check = vartype[o]
                o += 1
            if exptype != check:
                print("REJECT")
                sys.exit(0)
            if ch == 1:
                print("REJECT")
                sys.exit(0)

        if excret == 1:
            o = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v == token[x-1]:
                    check = vartype[o]
                o += 1
            if exptype != check:
                print("REJECT")
                sys.exit(0)


        if "[" in token[x]:
            x += 1  # Accept [
            exp()
            if "]" in token[x]:
                x += 1  # Accept ]
            else:
                return
        elif "(" in token[x]:
            x += 1  # Accept (
            args()
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
        exp()
        if ")" in token[x]:
            x += 1  # Accept )
        else:
            return
    else:
        print("REJECT")
        sys.exit(0)


def factorprime():  # 33
    global x
    w = token[x].isalpha()
    if token[x] not in keywordchecklist and w is True:
        x += 1  # Accept ID
        if "(" in token[x]:
            x += 1  # Accept (
            args()
            if ")" in token[x]:
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
    if token[x] not in keywords and w is True:
        arglist()
    elif z is True:
        arglist()
    elif "(" in token[x]:
        arglist()
    elif ")" in token[x]:
        return
    else:
        return


def arglist():  # 35
    global parammatch, parm
    parm = 1
    parammatch = ""
    exp()
    arglistprime()


def arglistprime():  # 36
    global x
    if "," in token[x]:
        x += 1  # Accept ,
        exp()
        arglistprime()
    elif ")" in token[x]:
        return
    else:
        return


# ----------------------------- end of parsing functions --------------------------------- #

# begin parsing
programDeclaration()

print(vardec)
print(fundec)

if ismain == 1 and lastmain == 1:  # check if contains 1 main function
    print("ACCEPT")
else:
    print("REJECT")