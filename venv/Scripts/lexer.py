import re

class Lexer(object):


    def __init__(self, source_code):
        self.source_code = source_code
    def tokenize(self):
        keywords = ["if", "else", "while", "int", "float", "void", "return"]
        symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"
        #symbols = ['+', '!', '-', '/', '*', '<', '>', ">=", "<=", "==", "=", "!=", ";", ",", "(", ")", "[", "]", "{", "}"]
        characters = "[a-zA-Z]+|." #gets all words/ID's
        digits =  "[0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?" #gets all int/float values
        errors = "\S"
        dot = "."
        empty = "E"
        list = "(%s)|(%s)|(%s)|(%s)" % (characters, digits, symbols, errors)
        '([a-zA-Z]+)|([0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?)|'
        '("\/\*|\*\/|\+|-|\*|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]|//")|(\S)'

        insideComment = 0 #counter for comments

        #Where all the tokens created by lexer will be stored
        tokens = []

        #Create a word list of the source code
        source_code = self.source_code.split()

        #Keep track of word inex we are at in source code
        source_index = 0

        #loop through each word in source code to generate tokens
        while source_index < len(source_code):

            word = source_code[source_index]

            #This will recognize a variable  and create a token for it
            if word == "var": tokens.append(["VAR_DECLARATION", word])

            # This will find all the characters in the file
            #for word in re.findall(list, word):
            # for word in re.findall("\s*(?:(\d+)|(\w+)|(E+)|(\S+)|(.))", word):
            # for word in re.findall("\s*(\d+|\w+|.)", word):
            for word in re.findall("\s*(?:(\d+)|(\w+)|(.))", word):


                if re.match(digits, word[0]):
                    if "." in word[0]:
                        tokens.append(["FLOAT:", word[0]])
                    elif "E" in word[0]:
                        tokens.append(["FLOAT:", word[0]])
                    else:
                        tokens.append(["INTEGER:", word[0]])


                elif re.match(characters, word[1]):
                    if word[1] in keywords:
                        tokens.append(["KEYWORD:", word[1]])
                    else:
                        tokens.append(["ID:", word[1]])

                elif re.match(symbols, word[2]):
                    tokens.append(["SYMBOLS:", word[2]])
                """else:
                    if word[2] == "/*":
                        insideComment = insideComment + 1
                    elif word[2] == "*/" and insideComment > 0:
                        insideComment = insideComment - 1
                    elif word[2] == "//" and insideComment == 0:
                        break
                    elif insideComment == 0:
                        if word[2] == "*/":
                            if "*/*" in words:
                                tokens.append(["*"])
                                insideComment += 1
                                continue
                            else:
                                tokens.append("*")
                                tokens.append("/")
                        else:
                            tokens.append(word[2]) """




                #elif re.match(errors,word[3]):
                    #tokens.append(["ERROR:", word[3]])






                #elif re.match(not "\s*(\d+|\w+|.)", word):
                    #tokens.append(["ERROR:", word])




                """if word[0]:
                    tokens.append(["SYMBOLS:", word[0]])
                elif word[1]:
                    tokens.append(["DIGITS:", word[1]])
                elif word[2]:
                    if word[2] in keywords:
                        tokens.append(["KEYWORD:", word[2]])
                    else:
                        tokens.append(["ID:", word[2]]) """""









                """ elif word:
                    if word == "/*":
                        insideComment = insideComment + 1
                    elif word == "*/" and insideComment > 0:
                        insideComment = insideComment - 1
                    elif word == "//" and insideComment == 0:
                        break
                    elif insideComment == 0:
                        if word == "*/":
                            if "*/*" in word:
                                tokens.append(["*"])
                                insideComment += 1
                                continue
                            else:
                                tokens.append(["*"])
                                tokens.append(["/"])
                        else:
                            tokens.append(["Symbols:", word]) """






            #If a STATEMENT_END (;) is found at the last character in a word add a STATEMENT_END token
            #if word[len(word) - 1] == ")":
                #tokens.append(['End Statement', ')'])

           
           
            #elif word not in keywords or symbols or characters or digits:
                #tokens.append(['ERROR', word])
            
            
            
            #Increase word index after checking it
            source_index += 1

        for token in tokens:
            print(str(token))

        #Return created tokens
        return tokens

