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
fourMathOperations = ["-", "+", "/", "*"]
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

q = 1  # Counter for quadruples list
t = 0  # counter for our temps in the quadruples

currentFunction = 0  # what the function we are currently in is
insideCurrentFunction = 0  # checks for scope inside a function
insideExpression = 0

ifListQuadruples = []
ifListNumberQuadruples = 0
ifListFront = []
ifListBack = []
insideIfListQuadruples = 0
ifBranch = 0
elseBranch = 0

doubleCheck = 0
whileEndBranch = 0
whileFirstBranch = 0
lastW = 0
whileListQuadruples = []   # list of quadruples done until end of while loop
wListQuadruplesNumbers = 0
insideWlistQuadruples = 0
whileListFront = []  # first half of the paramteres for while loop
whileListBack = []  # second half of the parameters for while loop

# --------------------------- print line for code generation ----------------------------- #
print("----------------------------------------------------")
# ---------------------------------- parsing functions ----------------------------------- #


def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def programDeclaration():  # runs program(Rule 1)
    global isCompleted
    declarationList()
    if "$" in token[x]:
        isCompleted = 1  #continues
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
    global q
    global currentFunction
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
        funcparm = []
        if "main" in token[x]:
            print(str(q).ljust(4) + "\tfunc \t\t" + token[x-1] + "\t\tvoid\t\t0")
            q += 1
            currentFunction = token[x - 1]

        else:
            if "void" in token[x-2]:
                if "void" in token[x+1]:
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[x-1].ljust(4) + "\t\tvoid\t\t0")
                    q += 1
                    currentFunction = token[x - 1]
                else:
                    f = x + 1
                    paramcount = 0
                    qch = q + 1
                    funcparm = []
                    while token[f] != ")":
                        if token[f] in intFloatKeywords:
                            paramcount += 1
                            funcparm.append(str(qch).ljust(4) + "\tparam\t\t4   \t\t\t\t\t" + token[f + 1])
                            qch += 1
                            f += 2
                            if token[f] == ",":
                                f += 1
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[x - 1].ljust(4) + "\t\t" + token[x - 2].ljust(4) + "\t\t" + str(paramcount))
                    q = qch
                    for v in funcparm:
                        print(v)
                    currentFunction = token[x - 1]
            else:
                if "void" in token[x+1]:
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[x-1].ljust(4) + "\t\t" + token[x-2].ljust(4) + "\t\t0")
                    q += 1
                    currentFunction = token[x - 1]
                else:
                    f = x + 1
                    paramcount = 0
                    qch = q + 1
                    funcparm = []
                    while token[f] != ")":
                        if token[f] in intFloatKeywords:
                            paramcount += 1
                            funcparm.append(str(qch).ljust(4) + "\tparam\t\t4   \t\t\t\t\t" + token[f + 1])
                            qch += 1
                            f += 2
                            if token[f] == ",":
                                f += 1
                    print(str(q).ljust(4) + "\tfunc \t\t" + token[x - 1].ljust(4) + "\t\t" + token[x - 2].ljust(
                        4) + "\t\t" + str(
                        paramcount))
                    q = qch
                    for v in funcparm:
                        print(v)
                    currentFunction = token[x - 1]

        if ";" in token[x]:
            x += 1  # Accepts ;
        elif "[" in token[x]:
            x += 1  # Accepts [
            y = hasnum(token[x])
            if y is True:
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
def declarationPrime(): #Rule 5 
        global x
        if "(" in token[x]:
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



def variableDeclaration():  # Rule 6
    global x
    global q
    typeSpecifier()

    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID

        if "[" not in token[x]:
            if insideWlistQuadruples == 1:
                whileListQuadruples.append(str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[x - 1])
                q += 1
            elif insideIfListQuadruples == 1:
                ifListQuadruples.append(str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[x - 1])
                q += 1
            else:
                print(str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[x-1])
                q += 1

    else:
        print("REJECT")
        exit(0)
    if ";" in token[x]:
        variableDeclarationPrime()

def variableDeclarationPrime(): # Rule 7
    global x
    global q
    if ";" in token[x]:
        x += 1  # Accepts ;
    elif "[" in token[x]:
        x += 1  # Accepts [

        alloc = int(token[x]) * int(4)

        if insideWlistQuadruples == 1:
            whileListQuadruples.append(str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[x - 2])
            q += 1
        elif insideIfListQuadruples == 1:
            ifListQuadruples.append(str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[x - 2])
            q += 1
        else:
            print(str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[x-2])
            q += 1

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



def typeSpecifier():  # Rule 8
    global x
    if token[x] in miniKeywords:
        x += 1  # Accepts int/void/float
    else:
        return


def parameter():  # Rule 9
    global x
    typeSpecifier()

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

def parameterPrime():  # Rule 10
    global x
    typeSpecifier()
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accepts ID
        if "[" in token[x]:
            x += 1  # Accepts [
            if "]" in token[x]:
                x += 1  # Accepts ]
                return
            else:
                print("REJECT")
                exit(0)
    else:
        if "void" in token[x-1]:
            return
        else:
            print("REJECT")
            exit(0)


def parameters():  # Rule 11
    global x
    if token[x] in intFloatKeywords:
        parameterPrime()
        parametersListPrime()
    elif "void" in token[x]:
        x += 1 #Accepts void
        parameterPrime()
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


def parametersList():  # Rule 13
    parameter()
    parametersListPrime()


def parametersListPrime():  # Rule 14
    global x
    if "," in token[x]:
        x += 1  # Accepts ,
        parameter()
        parametersListPrime()
    elif ")" in token[x]:
        return
    else:
        return





def compoundStatement():  # Rule 15
    global x
    global currentFunction
    global q
    global insideCurrentFunction
    if "{" in token[x]:
        x += 1  # Accepts {
        insideCurrentFunction += 1

        if insideCurrentFunction > 1:
            if insideWlistQuadruples == 1:
                whileListQuadruples.append(str(q).ljust(4) + "\tblock\t\t    \t\t    ")
                q += 1
            elif insideIfListQuadruples == 1:
                ifListQuadruples.append(str(q).ljust(4) + "\tblock\t\t    \t\t    ")
                q += 1
            else:
                print(str(q).ljust(4) + "\tblock\t\t    \t\t    ")
                q += 1

    else:
        return

    localDeclarations()
    statement()

    if "}" in token[x]:
        x += 1  # Accepts }

        insideCurrentFunction -= 1
        if insideCurrentFunction > 0:
            if insideWlistQuadruples == 1:
                whileListQuadruples.append(str(q).ljust(4) + "\tend  \t\tblock\t\t")
                q += 1
            elif insideIfListQuadruples == 1:
                ifListQuadruples.append(str(q).ljust(4) + "\tend  \t\tblock\t\t")
                q += 1
            else:
                print(str(q).ljust(4) + "\tend  \t\tblock\t\t")
                q += 1

        if insideCurrentFunction == 0:
            print(str(q).ljust(4) + "\tend  \t\tfunc\t\t" + currentFunction)
            q += 1

    else:
        print("REJECT")
        exit(0)


def localDeclarations():  # Rule 16
    localDeclarationsPrime()


def localDeclarationsPrime():  # Rule 17
    if token[x] in miniKeywords:
        variableDeclaration()
        localDeclarationsPrime()
    else:
        return


def statementList():  # Rule 18
    statementListPrime()


def statementListPrime():  # Rule 19
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


def statement():  # Rule 20
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        expressionStatement()
    elif z is True:
        expressionStatement()
    elif token[x] in leftParenthesesSemicolon:
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
    if token[x] not in keywords and w is True:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif z is True:
        expressionPrime()
        if ";" in token[x]:
            x += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif "(" in token[x]:
        if ";" in token[x]:
            x += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)
    elif ";" in token[x]:
        if ";" in token[x]:
            x += 1  # Accept ;
        else:
            print("REJECT")
            sys.exit(0)


def selectionStatement():  # Rule 22
    global x
    global ifBranch
    global q
    global t
    global insideIfListQuadruples
    if "if" in token[x]:
        x += 1  # Accept if
    else:
        return

    if "(" in token[x]:
        x += 1  # Accept (

        f = x
        ifListFront = ""
        comparison = 0
        bch = 0
        while token[f] not in comparisionSymbols:
            if "[" in token[f] or bch == 1:
                ifListFront = ifListFront + token[f]
                bch = 1
                if "]" in token[f]:
                    bch = 0
            else:
                ifListFront = ifListFront + " " + token[f]
            f += 1


        comparison = token[f]
        ifListFront = infixToPostfix(ifListFront)
        lastIf = postfixEval(ifListFront)

        f += 1
        bch = 0
        ifListBack = ""
        while ")" not in token[f]:
            if "[" in token[f] or bch == 1:
                ifListBack = ifListBack + token[f]
                bch = 1
                if "]" in token[f]:
                    bch = 0
            else:
                ifListBack = ifListBack + " " + token[f]
            f += 1

        ifListBack = infixToPostfix(ifListBack)
        lastIfL = postfixEval(ifListBack)

        print(str(q).ljust(4) + "\tcomp \t\t" + lastIf.ljust(4) + "\t\t" + lastIfL.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1

        if ">" in comparison:
            print(str(q).ljust(4) + "\tBGT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif ">=" in comparison:
            print(str(q).ljust(4) + "\tBGET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif "<" in comparison:
            print(str(q).ljust(4) + "\tBLT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif "<=" in comparison:
            print(str(q).ljust(4) + "\tBLET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif "==" in comparison:
            print(str(q).ljust(4) + "\tBEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif "!=" in comparison:
            print(str(q).ljust(4) + "\tBNEQ \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1

        ifListQuadruples.append(str(q).ljust(4) + "\tBR   \t\t\t\t\t\t\t\t")
        q += 1


    else:
        print("REJECT")
        exit(0)

    expressionPrime()

    if ")" in token[x]:
        x += 1  # Accept )
    else:
        print("REJECT")
        exit(0)

    insideIfListQuadruples = 1

    statement()
    selectionStatementPrime()

def selectionStatementPrime(): # Rule 23
    global x
    global ifBranch
    global q
    global t
    global insideIfListQuadruples
    if "else" in token[x]:
        ifListQuadruples[ifListNumberQuadruples] = ifListQuadruples[ifListNumberQuadruples] + str(q + 1)
    else:
        ifListQuadruples[ifListNumberQuadruples] = ifListQuadruples[ifListNumberQuadruples] + str(q)
    elsech = 0

    for v in ifListQuadruples:
        print(v)
    insideIfListQuadruples = 0

    if "else" in token[x]:
        x += 1  # Accepts else

        ifListQuadruples.append(str(q).ljust(4) + "\tBR   \t\t\t\t\t\t\t\t")
        elsech = len(ifListQuadruples)
        q += 1
        insideIfListQuadruples = 1

        statement()

        ifListQuadruples[elsech - 1] = ifListQuadruples[elsech - 1] + str(q)

        for v in range(elsech-1, len(ifListQuadruples)):
            print(ifListQuadruples[v])
        insideIfListQuadruples = 0

    else:
        return


def iterationStatement():  # Rule 24
    global x
    global lastW
    global t
    global q
    global insideWlistQuadruples
    global doubleCheck
    global wListQuadruplesNumbers
    if "while" in token[x]:
        x += 1  # Accepts while
    else:
        return

    if "(" in token[x]:
        x += 1  # Accepts (

        whileEndBranch = q  # get start of while loop line for last quadruple in the block

        f = x
        wListFront = ""
        comparison = 0
        bch = 0
        while token[f] not in comparisionSymbols:
            if "[" in token[f] or bch == 1:
                wListFront = wListFront + token[f]
                bch = 1
                if "]" in token[f]:
                    bch = 0
            else:
                wListFront = wListFront + " " + token[f]
            f += 1


        comparison = token[f]
        wListFront = infixToPostfix(wListFront)
        lastW = postfixEval(wListFront)

        f += 1
        bch = 0
        wListBack = ""
        while ")" not in token[f]:
            if "[" in token[f] or bch == 1:
                wListBack = wListBack + token[f]
                bch = 1
                if "]" in token[f]:
                    bch = 0
            else:
                wListBack = wListBack + " " + token[f]
            f += 1

        wListBack = infixToPostfix(wListBack)
        lastWL = postfixEval(wListBack)

        if insideWlistQuadruples == 1:
            whileListQuadruples.append(str(q).ljust(4) + "\tcomp \t\t" + lastW.ljust(4) + "\t\t" + lastWL.ljust(4) + "\t\tt" + str(t))
        else:
            print(str(q).ljust(4) + "\tcomp \t\t" + lastW.ljust(4) + "\t\t" + lastWL.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1

        if ">" in comparison:
            if insideWlistQuadruples == 1:
                whileListQuadruples.append(str(q).ljust(4) + "\tBGT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBGT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif ">=" in comparison:
            if insideWlistQuadruples == 1:
                whileListQuadruples.append(str(q).ljust(4) + "\tBGET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBGET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif "<" in comparison:
            if insideWlistQuadruples == 1:
                whileListQuadruples.append(str(q).ljust(4) + "\tBLT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBLT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif "<=" in comparison:
            if insideWlistQuadruples == 1:
                whileListQuadruples.append(str(q).ljust(4) + "\tBLET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBLET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif "==" in comparison:
            if insideWlistQuadruples == 1:
                whileListQuadruples.append(str(q).ljust(4) + "\tBEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif "!=" in comparison:
            if insideWlistQuadruples == 1:
                whileListQuadruples.append(str(q).ljust(4) + "\tBNEQ \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print(str(q).ljust(4) + "\tBNEQ \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1

        whileListQuadruples.append(str(q).ljust(4) + "\tBR   \t\t\t\t\t\t\t\t")
        q += 1

    else:
        print("REJECT")
        exit(0)

    expressionPrime()

    if ")" in token[x]:
        x += 1  # Accepts )
    else:
        print("REJECT")
        exit(0)


    insideWlistQuadruples = 1
    doubleCheck += 1

    statement()
    doubleCheck -= 1


    whileListQuadruples[wListQuadruplesNumbers] = whileListQuadruples[wListQuadruplesNumbers] + str(q + 1) + "h"
    insideWlistQuadruples = 0

    if doubleCheck == 0:
        for v in whileListQuadruples:
            print(v)

    if insideWlistQuadruples == 1:
        whileListQuadruples.append(str(q).ljust(4) + "\tBR  \t\t\t\t\t\t\t\t" + str(whileEndBranch))
    else:
        print(str(q).ljust(4) + "\tBR  \t\t\t\t\t\t\t\t" + str(whileEndBranch))
    q += 1


def returnStatement():  # Rule 25
    global x
    if "return" in token[x]:
        x += 1  # Accepts return
    else:
        return
    returnStatementPrime()

def returnStatementPrime(): # Rule 26
    global x
    global q
    global t

    w = token[x].isalpha()
    z = hasnum(token[x])
    if ";" in token[x]:
        x += 1  # Accept ;

        print(str(q).ljust(4) + "\treturn\t\t    \t\t    ")
        q += 1
        return

    elif token[x] not in keywords and w is True:

        if "[" in token[x+1]:
            f = x
            retexp = ""
            while ";" not in token[f]:
                retexp = retexp + token[f]
                f += 1

            h1 = retexp.partition('[')
            h2 = retexp.partition('[')[-1].rpartition(']')[0]
            if h2.isdigit() is False:
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

        expressionPrime()

        if ";" in token[x]:
            x += 1  # Accepts ;
            return
        else:
            print("REJECT")
            exit(0)

    elif z is True:

        print(str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + token[x])
        q += 1

        expressionPrime()

        if ";" in token[x]:
            x += 1  # Accepts ;
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif "(" in token[x]:

        f = x + 1
        bch = 0
        expret = ""
        while ")" not in token[f]:
            if "[" in token[f] or bch == 1:
                expret = expret + token[f]
                bch = 1
                if "]" in token[f]:
                    bch = 0
            else:
                expret = expret + " " + token[f]
            f += 1

        expret = infixToPostfix(expret)
        lastexpret = postfixEval(expret)

        print(str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + lastexpret)
        q += 1

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
    if "=" in token[x]:
        x += 1  # Accept =
        expressionPrime()
    elif "[" in token[x]:
        x += 1  # Accept [
        expressionPrime()
        if "[" in token[x-1]:
            print("REJECT")
            sys.exit(0)
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
            sys.exit(0)
    elif "(" in token[x]:
        x += 1  # Accept (
        arguments()
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


def expressionPrime():  # Rule 28
    global x
    global q
    global t
    global insideExpression
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID

        if "[" in token[x] and insideExpression == 0:
            f = x - 1
            check = ""
            while "=" not in token[f]:
                check = check + token[f]
                f += 1
            x = f
            assign = check

            if insideWlistQuadruples == 1:
                h1 = assign.partition('[')
                h2 = assign.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    whileListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whileListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                assign = temp

            elif insideIfListQuadruples == 1:
                h1 = assign.partition('[')
                h2 = assign.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    ifListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                ifListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                assign = temp

            else:
                h1 = assign.partition('[')
                h2 = assign.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
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

        if "(" in token[x] and insideExpression == 0:
            f = x
            exquad = token[x-1]
            while ";" not in token[f]:
                exquad = exquad + token[f]
                f += 1

            if insideWlistQuadruples == 1:
                parmcount = 0
                h1 = exquad.partition('(')[-1].rpartition(')')[0]
                h2 = exquad.partition('(')
                if ',' in h1:
                    h1 = h1.split(',')
                for v in h1:
                    parmcount += 1
                    whileListQuadruples.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                    q += 1

                whileListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                q += 1
                t += 1

            elif insideIfListQuadruples == 1:
                parmcount = 0
                h1 = exquad.partition('(')[-1].rpartition(')')[0]
                h2 = exquad.partition('(')
                if ',' in h1:
                    h1 = h1.split(',')
                for v in h1:
                    parmcount += 1
                    ifListQuadruples.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                    q += 1

                ifListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
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

        if "=" in token[x]:
            f = x + 1
            exquad = ""
            bch = 0
            pch = 0
            while ";" not in token[f]:
                if "[" in token[f] or bch == 1:
                    exquad = exquad + token[f]
                    bch = 1
                    if "]" in token[f]:
                        bch = 0
                elif "(" in token[f] or pch == 1:
                    if token[f-1] not in fourMathOperations:
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

            if insideWlistQuadruples == 1:
                if "(" in lastexp:
                    parmcount = 0
                    h1 = lastexp.partition('(')[-1].rpartition(')')[0]
                    h2 = lastexp.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whileListQuadruples.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whileListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    whileListQuadruples.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    insideExpression = 1

                elif "[" in lastexp:
                    h1 = lastexp.partition('[')
                    h2 = lastexp.partition('[')[-1].rpartition(']')[0]
                    if h2.isdigit() is False:
                        whileListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                        q += 1
                        temp = "t" + str(t)
                        t += 1
                        h2 = temp
                    else:
                        h2 = int(h2) * 4
                    whileListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1

                    whileListQuadruples.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    insideExpression = 1

                else:
                    whileListQuadruples.append(str(q).ljust(4) + "\tassgn\t\t" + lastexp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    insideExpression = 1

            elif insideIfListQuadruples == 1:
                if "(" in lastexp:
                    parmcount = 0
                    h1 = lastexp.partition('(')[-1].rpartition(')')[0]
                    h2 = lastexp.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        ifListQuadruples.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    ifListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    ifListQuadruples.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    insideExpression = 1

                elif "[" in lastexp:
                    h1 = lastexp.partition('[')
                    h2 = lastexp.partition('[')[-1].rpartition(']')[0]
                    if h2.isdigit() is False:
                        ifListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                        q += 1
                        temp = "t" + str(t)
                        t += 1
                        h2 = temp
                    else:
                        h2 = int(h2) * 4
                    ifListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1

                    ifListQuadruples.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    insideExpression = 1

                else:
                    ifListQuadruples.append(str(q).ljust(4) + "\tassgn\t\t" + lastexp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    insideExpression =1

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
                    insideExpression =1

                elif "[" in lastexp:
                    h1 = lastexp.partition('[')
                    h2 = lastexp.partition('[')[-1].rpartition(']')[0]
                    if h2.isdigit() is False:
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
                    insideExpression = 1

                else:
                    print(str(q).ljust(4) + "\tassgn\t\t" + lastexp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    insideExpression = 1

        expression()
        insideExpression = 0

    elif "(" in token[x]:
        x += 1  # Accepts (
        expressionPrime()
        if ")" in token[x] or z is True:
            x += 1  # Accepts )
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





def variable():  # Rule 29
    global x
    w = token[x].isalpha()
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
    else:
        return
    variablePrime()
def variablePrime(): # Rule 30
    if "[" in token[x]:
        x += 1  # Accepts [
        expressionPrime()
        if "]" in token[x]:
            x += 1  # Accept ]
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

def term():  # Rul3 37
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


def factor():  # 40
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True:
        x += 1  # Accept ID
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


def factorPrime():  # Rule 41
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


def arguments():  # Rule 42
    global x
    w = token[x].isalpha()
    z = hasnum(token[x])
    if token[x] not in keywords and w is True or z is True or "(" in token[x]:
        argumentsList()
    elif token[x] == ")":
        return
    else:
        return


def argumentsList():  # Rule 43
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
        if token.isalnum() or "[" in token or ("(" in token and ")" in token) or (re.search('[a-z]', token) is True and "(" in token) or token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789" or token in "abcdefghijklmnopqrstuvwxyz":
            postfixList.append(token)
        elif "(" in token:
            opStack.push(token)
        elif ")" in token :
            topToken = opStack.pop()
            while "(" not in topToken:
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and (prec[opStack.peek()] >= prec[token]):
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
        if token.isalnum() or "[" in token or ("(" in token and ")" in token) or (re.search('[a-z]', token) is True and "(" in token) or token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789" or token in "abcdefghijklmnopqrstuvwxyz":
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

    if "*" in op:
        if insideWlistQuadruples == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whileListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whileListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
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
                        whileListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whileListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    whileListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whileListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    whileListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whileListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            whileListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        elif insideIfListQuadruples == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        ifListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    ifListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
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
                        ifListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    ifListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    ifListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                ifListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    ifListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                ifListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            ifListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

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
                if h2.isdigit() is False:
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
                if h2.isdigit() is False:
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

    elif "/" in op:
        if insideWlistQuadruples == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whileListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whileListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
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
                        whileListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whileListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    whileListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whileListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    whileListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whileListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            whileListQuadruples.append(str(q).ljust(4) + "\tdiv  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        elif insideIfListQuadruples == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        ifListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    ifListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
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
                        ifListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    ifListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    ifListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                ifListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    ifListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                ifListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            ifListQuadruples.append(str(q).ljust(4) + "\tdiv  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

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

    elif "+" in op:
        if insideWlistQuadruples == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whileListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whileListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
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
                        whileListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whileListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    whileListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whileListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    whileListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whileListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp

            whileListQuadruples.append(str(q).ljust(4) + "\tadd  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        elif insideIfListQuadruples == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        ifListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    ifListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
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
                        ifListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    ifListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    ifListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                ifListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    ifListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                ifListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp

            ifListQuadruples.append(str(q).ljust(4) + "\tadd  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

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
                if h2.isdigit() is False:
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
                if h2.isdigit() is False:
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
        if insideWlistQuadruples == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whileListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whileListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
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
                        whileListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whileListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    whileListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whileListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    whileListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whileListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            whileListQuadruples.append(str(q).ljust(4) + "\tsub  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

        elif insideIfListQuadruples == 1:
            if "(" in op1:
                    parmcount = 0
                    h1 = op1.partition('(')[-1].rpartition(')')[0]
                    h2 = op1.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        ifListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    ifListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
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
                        ifListQuadruples.append(str(q).ljust(4) + "\targ \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    ifListQuadruples.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    op2 = temp

            if "[" in op1:
                h1 = op1.partition('[')
                h2 = op1.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    ifListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                ifListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op1 = temp

            if "[" in op2:
                h1 = op2.partition('[')
                h2 = op2.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() is False:
                    ifListQuadruples.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                ifListQuadruples.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                op2 = temp
            ifListQuadruples.append(str(q).ljust(4) + "\tsub  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))

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
                if h2.isdigit() is False:
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
                if h2.isdigit() is False:
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

def parameterCount():
    global x
    global q
    global currentFunction
    f = x + 1
    paramcount = 0
    qch = q + 1
    funcparm = []
    while ")" not in token[f]:
        if token[f] in intFloatKeywords:
            paramcount += 1
            funcparm.append(str(qch).ljust(4) + "\tparam\t\t4   \t\t\t\t\t" + token[f + 1])
            qch += 1
            f += 2
            if "," in token[f]:
                f += 1
    print(str(q).ljust(4) + "\tfunc \t\t" + token[x - 1].ljust(4) + "\t\t" + token[x - 2].ljust(4) + "\t\t" + str(
        paramcount))
    q = qch
    for v in funcparm:
        print(v)
    currentFunction = token[x - 1]
# ---------------------- end of our stack for infix to postfix --------------------------- #

# begin parsing
programDeclaration()