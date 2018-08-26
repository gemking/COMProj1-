import re

class Lexer(object):


    def __init__(self, source_code):
        self.source_code = source_code
    def tokenize(self):
        keywords = ["if", "else", "while", "int", "float", "void", "return"]
        symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"
        #symbols = ['+', '!', '-', '/', '*', '<', '>', ">=", "<=", "==", "=", "!=", ";", ",", "(", ")", "[", "]", "{", "}"]
        characters = "[a-zA-Z]+" #gets all words/ID's
        digits =  "[0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?" #gets all int/float values

        #regex = "(%s)|(%s)|(%s)|(%s)" % (keywords, symbols, characters, digits)
        #'([a-zA-Z]+)|([0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?)|'
        #'("\/\*|\*\/|\+|-|\*|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]|//")|(\S)'

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

            # This will recognize operators and create an OPERATOR token for it
            elif re.match(symbols, word):
                tokens.append([word])

            elif re.match(characters, word):
                if word in keywords:
                    tokens.append(['KEYWORD', word])
                else:
                    tokens.append(['ID', word])
                # if word[len(word) - 1] == ")":
                # tokens.append(['ID', word[0:len(word) - 1]])


            #This will recognize an integer and create an INTEGER token for it
            elif re.match(digits, word):
                #if word[len(word) -1] == ";":
                    #tokens.append(['INTEGER', word[0:len(word) - 1]])
                #else:
                tokens.append(['INTEGER', word])





            #If a STATEMENT_END (;) is found at the last character in a word add a STATEMENT_END token
            #if word[len(word) - 1] == ")":
                #tokens.append(['End Statement', ')'])

           
           
            #elif word not in keywords or symbols or characters or digits:
                #tokens.append(['ERROR', word])
            
            
            
            #Increase word index after checking it
            source_index += 1

        print(str(tokens))

        #Return created tokens
        return tokens

