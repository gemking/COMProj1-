import re

i

keywords = ["if", "else", "while", "int", "float", "void", "return"]
symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"
# doubleSymbols = "<=|>=|==|!="
# symbols = ['+', '!', '-', '/', '*', '<', '>', ">=", "<=", "==", "=", "!=", ";", ",", "(", ")", "[", "]", "{", "}"]
characters = "[a-zA-Z]+|."  # gets all words/ID's
# digits = "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?"
# dPlaceholder = "[-+]?\d*\.\d+|\d+"
errorID = "(r'[a-zA-Z]+[.0-9][.0-9a-zA-Z]')"
errorInteger = "(r'[0-9]+[a-df-zA-DF-Z][.0-9a-zA-Z]')"
digits = "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?"  # gets all int/float values
errorSymbols = "[@|_|!]"
errors = "\S"
dot = "."
empty = "E"
# list = "(%s)|(%s)|(%s)|(%s)" % (characters, digits, symbols, errors)
'([a-zA-Z]+)|([0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?)|'
'("\/\*|\*\/|\+|-|\*|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]|//")|(\S)'

insideComment = 0
# insideComment = True/False


# This will recognize a variable  and create a token for it
# if word == "var": tokens.append(["VAR_DECLARATION", word])

# This will find all the characters in the file
# for word in re.findall(list, word):
# for word in re.findall("\s*(?:(\d+)|(\w+)|(E+)|(\S+)|(.))", word):
# for word in re.findall("\s*(\d+|\w+|.)", word):
for word in re.findall("\s*(?:([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)|(\w+)|(.))", word):

    if re.match(digits, word[0]):
        # if word[0] and insideComment == 0:
        if "." in word[0]:
            tokens.append(["FLOAT:", word[0]])
        elif "E" in word[0]:
            tokens.append(["FLOAT:", word[0]])
        else:
            tokens.append(["INTEGER:", word[0]])


    elif re.match(characters, word[2]):
        # if word[2] and insideComment == 0:
        if word[2] in keywords:
            tokens.append(["KEYWORD:", word[2]])
        else:
            # if word[2] in errorID:
            # tokens.append(["ERROR:", word[2]])
            if word[2] in errorSymbols:
                tokens.append(["ERROR:", word[2]])
            else:
                tokens.append(["ID:", word[2]])

    elif re.match(characters, word[3]):
        if word[3] in errorSymbols:
            tokens.append(["ERROR:", word[3]])
        else:
            # if word[3] == "=":
            # if len(word[3] + 1) in ["<", ">"]:
            # tokens.append("SYMBOL:", word[3])
            #:
            # tokens.append(["DOUBLESYMBOL", word[3][0:len(word[3] + 1)]])
            tokens.append(["SYMBOL:", word[3]])

    """elif word[3]:
        if word[3] == "/*":
            insideComment = insideComment + 1
        elif word[3] == "*/" and insideComment > 0:
            insideComment = insideComment - 1
        elif word[3] == "//" and insideComment == 0:
            break
        elif insideComment == 0:
            if word[3] == "*/":
                if "*/*" in word:
                    tokens.append(["*"])
                    insideComment += 1
                    continue
                else:
                    tokens.append(["*"])
                    tokens.append(["/"])
            else:
                    tokens.append(word[3]) """

    # else:
    # elif.re.match(symbols, word[3]):
    # if word[3] and insideComment == 0:
    # tokens.append("Symbols:", word[3])

    # elif re.match(errors,word[3]):
    # tokens.append(["ERROR:", word[3]])

    # elif re.match(not "\s*(\d+|\w+|.)", word):
    # tokens.append(["ERROR:", word])

# Increase word index after checking it
source_index += 1

for token in tokens:
    print(str(token))

# Return created tokens
return tokens