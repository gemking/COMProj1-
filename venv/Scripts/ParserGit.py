import re
import sys

with open(sys.argv[1], "r") as file: #opens file
    filelines = file.read().splitlines() # reads file and splits lines
    file.close() #closes file


insideComment = 0
keywords = ["if", "else", "while", "int", "float", "void", "return"] #denotes all keywords
symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]" #denotes symbols used
comparisonSymbols = "<=|<|>=|>|==|!=" #for comparision
characters = "[a-zA-Z]+" #obtains all words for the IDs
digits = "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" #gets all decimal values, including integer values 0-9
errors = "\S" #reports errors
tokens = [] #creates a list that holds all of the tokens
x = 0 #value that holds the token counter for the parser

for importantLines in filelines: #receiving importantlines from filelines
    importantLine = importantLines #sets importantLine to importantLines




    list = "(%s)|(%s)|(%s)|(%s)" % (characters, digits, symbols, errors) #puts entire library into a list of strings

    for word in re.findall(list, importantLine): #finds list
        if re.match(characters, word[0]) and insideComment == 0: #matches digits and makes sure insideComment is 0
            if word[0] in keywords:
                tokens.append("KEYWORD: " + word[0]) #keyword is constructed out of characters a-zA-Z
            else:
                tokens.append("ID: " + word[0]) # appends character values that are not keywords

        elif re.match(digits, word[1]) and insideComment == 0: #matches characters and makes sure insideComment is 0
            if "." in word[1]:
                tokens.append("FLOAT: " + word[1]) #checks if value is a decimal value and appends
            elif "E" in word[1]:
                tokens.append("FLOAT: " + word[1]) #checks if value is an expontential value and appends
            else:
                tokens.append("INTEGER: " + word[1])  #appends integer value


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
                        tokens.append("*")
                        insideComment += 1
                        continue #skips comments and continues through the program
                    else:
                        tokens.append("*") #appends multiplication symbol
                        tokens.append("/") #appends division symbol
                else:
                    tokens.append(word[3]) #appends rest of symbols
        elif word[4] and insideComment == 0: #matches errors and makes sure insideComment is 0
            tokens.append("ERROR: " + word[4]) #appends error

#end of lexical analyzer
tokens.append("$") #end result for parsing

#parser

def containsNumber(inputstring):
    return any(char.isdigit() for char in inputstring)

def program(): #1
    d1()
    if "$" in tokens[x]:
        print("ACCEPT")
    else:
        print("REJECT")

def d1(): #2
    declaration()
    d1prime()

def d1prime(): #3
    if "int" in tokens[x] or "void" in tokens[x] or "float" in tokens[x]:
        declaration()
        d1prime()
    elif "$" in tokens[x]:
        return
    else:
        return
def declaration(): #4
    global x
    types()
    w = tokens[x].isalpha()
    if tokens[x] not in keywords and w is True:
        x += 1  #Identifier Accepted
        if ";" in tokens[x]:
            x += 1 # ';' Accepted
        elif "[" in tokens[x]:
            x += 1 # '[' Accepted
            z = containsNumber(tokens[x])
            if z is True:
                x += 1 #Number and Float Accepted
                if "]" in tokens[x]:
                    x += 1 # ']' Accepted
                    if ";" in tokens[x]:
                        x += 1 # ';' Accepted
                    else:
                        print("REJECT")
                        sys.exit(0)
                else:
                    print("REJECT")
                    sys.exit(0)
            else:
                print("REJECT")
                sys.exit(0)
        elif "(" in tokens[x]:
            x += 1 # '(' Accepted
            params()
            if ")" in tokens[x]:
                x += 1 # ')' Accepted
                compoundstmt() #come back later
            else:
                print("REJECT")
                sys.exit(0) #see if there is another commaand
        else:
            print("REJECT")
            sys.exit(0)
    else:
        print("REJECT")
        sys.exit(0)

def vd(): #5
    global x
    types()

    w = tokens[x].isalpha()
    if tokens[x] not in keywords and w is True:
        x += 1  #ID Accepted
    else:
        print("REJECT")
        sys.exit(0)

    if ";" in tokens[x]:
        x += 1 # ';' Accepted
    elif "[" in tokens[x]:
        x += 1 # '[' Accepted
        w = containsNumber([tokens[x]])
        if w is True:
            x +=1 #NUM/FLOAT Accepted
            if "]" in tokens[x]:
                x += 1 # ']' Accepted
                if ";" in tokens[x]:
                    x += 1 # ';' Accepted
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
def types(): #6
    global x
    if "int" in tokens[x] or "void" in tokens[x] or "float" in tokens[x]:
        x += 1 #integer, void, and float values are accepted
    else:
        return

def fd(): #7
    global x
    types()

    w = tokens[x].isalpha()
    if tokens[x] not in keywords and x is True:
        x += 1 #Accept ID
    else:
        return

    if "(" in tokens[x]:
        x += 1 # '(' Accepted
    else:
        print()
        sys.exit(0)

    params()

    if ")" in tokens[x]:
        x += 1 # ')' Accepted
    else:
        print("REJECT")
        sys.exit(0)

    compoundstmt()

def params(): #8
    global x
    if "int" in tokens[x] or "float" in tokens[x]:
        paramslist()
    elif "void" in tokens[x]:
        x += 1 #Void Accepted
        return
    else:
        print("REJECT")
        sys.exit(0)

def paramslist(): #9
    param()
    paramsListPrime()

def paramsListPrime(): #10
    global x
    if "," in tokens[x]:
        x += 1 #Accept ,
        param()
        paramsListPrime()
    elif ")" in tokens[x]:
        return
    else:
        return

def param(): #11
    global x
    types()
    w = tokens[x].isalpha()
    if tokens[x] not in keywords and w is True:
        x += 1 #Accept ID
    else:
        return
    if "[" in tokens[x]:
        x += 1 # '[' Accepted
        if "]" in tokens[x]:
            x += 1 # ']' Accepted
            return
        else:
            print("REJECT")
            sys.exit(0)
    else:
        return

def compoundstmt(): #12
    global x
    if "{" in tokens[x]:
        x += 1 # '{' Accepted
    else :
        return

    localdeclarations()
    statementlist()

    if "}" in tokens[x]:
        x += 1 # '}' Accepted
    else:
        print("REJECT")
        sys.exit(0)

def localdeclarations(): # 13
    localdeclarationsprime()

def localdeclarationsprime(): #14
    if "int" in tokens[x] or "void" in tokens[x] or "float" in tokens[x]:
        vd()
        localdeclarationsprime()
    else:
        return

def statementlist(): #15
    statementlistprime()

def statementlistprime(): # 16
    w = tokens[x].isalpha()
    z = containsNumber(tokens[x])
    if tokens[x] not in keywords and w is True:
        statement()
        statementlistprime()
    elif z is True:
        statement()
        statementlistprime()
    elif "(" in tokens[x] or ";" in tokens[x] or "{" in tokens[x] or "if" in tokens[x] or "while" in tokens[x] or "return" in tokens[x]:
        statement()
        statementlistprime()
    elif "}" in tokens[x]:
        return
    else:
        return

def statement(): # 17
    w = tokens[x].isalpha()
    z = containsNumber(tokens[x])
    if tokens[x] not in keywords and w is True:
        expstmt()
    elif z is True:
        expstmt()
    elif "(" in tokens[x] or ";" in tokens[x]:
        expstmt()
    elif "{" in tokens[x]:
        compoundstmt()
    elif "if" in tokens[x]:
        selectionstmt()
    elif "while" in tokens[x]:
        itstmt()
    elif "return" in tokens[x]:
        retstmt()
    else
        print("REJECT")
        sys.exit(0)

def expstmt(): #18
    global x
    w = tokens[x].isalpha()
    z = containsNumber(tokens[x])
    if tokens[x] not in keywords and w is True:
        exp()
        if ";" in tokens[x]:
            x += 1 # ";" is accepted
        else:
            print("REJECT")
            sys.exit(0)
    elif z is True:
        exp()
        if ";" in tokens[x]:
            x += 1 # ";" is accepted
        else:
            print("REJECT")
            sys.exit(0)
    elif "(" in tokens[x]:
        exp()
        if ";" in tokens[x]:
            x += 1 # ";" is accepted
        else:
            print("REJECT")
            sys.exit(0)
    elif ";" in tokens[x]:
        x += 1 # ";" is accepted
    else:
        print("REJECT")
        sys.exit(0)

def selectionstmt(): #19
    global x
    if "if" in tokens[x]:
        x += 1 #  "if" is accepted
    else:
        return

    if "(" in tokens[x]:
        x += 1 # "(" is accepted
    else:
        print("REJECT")
        sys.exit(0)

    exp()

    if ")" in tokens[x]:
        x += 1 # ")" is accepted
    else:
        print("REJECT")
        sys.exit(0)

    statement()

    if "else" in tokens[x]:
        x += 1 # "else" is accepted
        statement()
    else:
        return

def itstmt(): #20
    global x
    if "while" in tokens[x]:
        x += 1 # "while" is accepted
    else:
        return

    if "(" in tokens[x]:
        x += 1 # "(" is accepted
    else:
        print("REJECT")
        sys.exit(0)

    exp()

    if ")" in tokens[x]:
        x += 1 # ")" is accepted
    else:
        print("REJECT")
        sys,exit(0)

    statement()

def retsmt(): #21
    global x
    if "return" in tokens[x]:
        x+= 1 # "return" is accepted
    else:
        return

    w = tokens[x].isalpha()
    z = containsNumber(tokens[x])
    if ";" in tokens[x]:
        x += 1 #";" is accepted
        return
    elif tokens[x] not in keywords and w is True:
        exp()
        if ";" in tokens[x]:
            x += 1 # ";" is accepted
            return
        else:
            print("REJECT")
            sys.exit(0)
    elif z is True:
        exp()
        if ";" in tokens[x]:
            x += 1 # ";" is accepted
            return
        else:
            print("REJECT")
            sys.exit(0)
    else:
        print("REJECT")
        sys.exit(0)

def exp(): #22
    global x
    w = tokens[x].isalpha()
    z = containsNumber(tokens[x])
    if tokens[x] not in keywords and w is True:
        x += 1 # "ID" is accepted
        ex()
    elif "(" in tokens[x]:
        x += 1 # ")" is accepted
        exp()
        if ")" in tokens[x]:
            termprime()
            addexpprime()
            if "<=" in tokens[x] or "<" in tokens[x] or ">" in tokens[x] or ">=" in tokens[x] or "==" in tokens[x] or "!=" in tokens[x]:
                relop()
                addexp()
            elif "+" in tokens[x] or "-" in tokens[x]:
                addexprime()
                if "<=" in tokens[x] or "<" in tokens[x] or ">" in tokens[x] or ">=" in tokens[x] or "==" in tokens[x] or "!=" in tokens[x]:
                relop()
                addexp()
            else:
                return
        else:
            print("REJECT")
            sys.exit(0)
    elif z is True:
        x += 1 # "NUM", "FLOAT" accepted
        termprime()
        addexpprime()
        if "<=" in tokens[x] or "<" in tokens[x] or ">" in tokens[x] or ">=" in tokens[x] or "==" in tokens[x] or "!=" in tokens[x]:
            relop()
            addexp()
        elif "+" in tokens[x] or "-" in tokens[x]:
            addexpprime()
            if "<=" in tokens[x] or "<" in tokens[x] or ">" in tokens[x] or ">=" in tokens[x] or "==" in tokens[x] or "!=" in tokens[x]:
                relop()
                addexp()
            elif "<=" in tokens[x] or "<" in tokens[x] or ">" in tokens[x] or ">=" in tokens[x] or "==" in tokens[x] or "!=" in tokens[x]:
                relop()
                addexp()
            else:
                return
        else:
            print("REJECT")
            sys.exit(0)

    def ex(): #22X
        global x
        if "=" in tokens[x]:
            x += 1 # "=" is accepted
            exp()
        elif "[" in tokens[x]:
            x += 1 # "[" is accepted
            exp()
            if "[" in tokens[x-1]:
                print("REJECT")
                sys.exit(0)
            if "]" in tokens[x]:
                x += 1 # "]" is accepted
                if "=" in tokens[x]:
                    x += 1 # "=" is accepted
                    exp()
                elif "*" in tokens[x] or "/" in tokens[x]:
                    termprime()
                    addexprime()
                    if comparisonSymbols in tokens[x]:
                        relop()
                        addexp()
                    else:
                        return
                elif "+" in tokens[x] or "-" in tokens[x]:
                    addexprime()
                    if comparisonSymbols in tokens[x]:
                        relop()
                        addexp()

