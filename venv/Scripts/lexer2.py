import re
import sys


def __init__(self, source_code):
    self.source_code = source_code
file = open(sys.argv[1], "r")
filelines = file.read().splitlines()
file.close()

keywords = ["if", "else", "while", "int", "float", "void", "return"]
symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"
characters = "[a-zA-Z]+" #gets all words/ID's"
digits =  "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" #gets all int/float values
errors = "\S"
insideComment = 0



for lines in filelines:
    fline = lines
    if not fline:
        continue
    print

    if fline:
        print("INPUT: " + fline)
def tokenize(self):
    tokens = []
    source_code = self.source_code.split()
    source_index = 0
    while source_index < len(source_code):
        word = source_code[source_index]
    list = "(%s)|(%s)|(%s)|(%s)" % (characters, digits, symbols, errors)

    for word in re.findall(list, fline):
        if re.match(characters, word[0]):
            if word[0] and insideComment == 0:
                if word[0] in keywords:
                    tokens.append("KEYWORD:", word[0])
                else:
                     tokens.append("ID:", word[0])

        elif word[1] and insideComment == 0:
            if re.match(digits, word[1]):
                if "." in word[1]:
                    print("FLOAT:", word[1])
                elif "E" in word[1]:
                    print("FLOAT:", word[1])
                else:
                    print("INTEGER:", word[1])

        elif re.match(characters, word[2]):
            if word[2] and insideComment == 0:
             print("ID:", word[2])

        elif re.match(symbols, word[3]):
            if word[3]:
                if word[3] == "/*":
                    insideComment = insideComment + 1
                elif word[3] == "*/" and insideComment > 0:
                    insideComment = insideComment - 1
                elif word[3] == "//" and insideComment == 0:
                    break
                elif insideComment == 0:
                    if word[3] == "*/":
                        if "*/*" in word:
                            print(["*"])
                            insideComment += 1
                            continue
                        else:
                            print("*")
                            print("/")
                    else:
                        print(word[3])
        elif word[4] and insideComment == 0:
            print("ERROR:", word[4])

        for token in tokens:
            print(str(token))

