import re
import sys

with open(sys.argv[1], "r") as file: #opens file
    filelines = file.read().splitlines() # reads file and splits lines
    file.close() #closes file


insideComment = 0
keywordchecklist = ["else", "if", "int", "return", "void", "while", "float"]  # list of all keywords
#keywords = ["if", "else", "while", "int", "float", "void", "return"] #denotes all keywords
symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]" #denotes symbols used
comparisonSymbols = "<" or "<=" or  ">" or ">=" or "==" or"!="
addSubtractSymbols = "+" or "-"
multiplyDivideSymbols = "*" or "/"
characters = "[a-zA-Z]+" #obtains all words for the IDs
digits = "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" #gets all decimal values, including integer values 0-9
errors = "\S" #reports errors
token = [] #creates a list that holds all of the tokens
i = 0 #value that holds the token counter for the parser

for importantLines in filelines: #receiving importantlines from filelines
    importantLine = importantLines #sets importantLine to importantLines




    list = "(%s)|(%s)|(%s)|(%s)" % (characters, digits, symbols, errors) #puts entire library into a list of strings

    for word in re.findall(list, importantLine): #finds list
        if re.match(characters, word[0]) and insideComment == 0: #matches digits and makes sure insideComment is 0
            if word[0] in keywordchecklist:
                token.append("KEYWORD: " + word[0]) #keyword is constructed out of characters a-zA-Z
            else:
                token.append("ID: " + word[0]) # appends character values that are not keywords

        elif re.match(digits, word[1]) and insideComment == 0: #matches characters and makes sure insideComment is 0
            if "." in word[1]:
                token.append("FLOAT: " + word[1]) #checks if value is a decimal value and appends
            elif "E" in word[1]:
                token.append("FLOAT: " + word[1]) #checks if value is an expontential value and appends
            else:
                token.append("INTEGER: " + word[1])  #appends integer value


        elif re.match(symbols, word[3]): #matches symbols
            if "/*" in word[3]: #Checks when word approaches /*
                insideComment += 1 #increments insideComment if inside
            elif "*/" in word[3] and insideComment > 0: #Checks when word approaches */
                insideComment -= 1 #decrements insideComment if outside
            elif "//" in word[3] and insideComment > 0: #If neither
                break
            elif insideComment == 0: #when inside counter is 0
                if "*/" in word[3]: #when it reaches terminal */
                    if "*/*" in word: #when it's still sorting through comments
                        token.append("*")
                        insideComment += 1
                        continue #skips comments and continues through the program
                    else:
                        token.append("*") #appends multiplication symbol
                        token.append("/") #appends division symbol
                else:
                    token.append(word[3]) #appends rest of symbols
        elif word[4] and insideComment == 0: #matches errors and makes sure insideComment is 0
            token.append("ERROR: " + word[4]) #appends error

#end of lexical analyzer
token.append("$") #end result for parsing

#parser

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