import re
import sys

with open(sys.argv[1], "r") as file: #opens file
    filelines = file.read().splitlines() # reads file and splits lines
    file.close() #closes file


insideComment = 0
keywords = ["if", "else", "while", "int", "float", "void", "return"] #denotes all keywords
symbols = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]" #denotes symbols used
characters = "[a-zA-Z]+" #obtains all words for the IDs
digits =  "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" #gets all decimal values, including integer values 0-9
errors = "\S" #reports errors
tokens = [] #creates a list that holds all of the tokens


for importantLines in filelines: #receiving importantlines from filelines
    importantLine = importantLines #sets importantLine to importantLines
    if importantLine: #needs to be an importantLine
        tokens.append("INPUT: " + importantLines.strip()) #appends input and strips blank space



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

for token in tokens:
    print(str(token)) #prints tokens


 #this is the end of the program











            

