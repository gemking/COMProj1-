import lexer
import sys

#content = ""
#with open(sys.argv[1], "r") as file:
   #content = file.read()
def main():
    content = ""
    with open(sys.argv[1], 'r') as file:
         #file.read().splitlines()

    #file = open(sys.argv[1], 'r')
    #filelines = file.read().splitlines()
    #file.close()

    #for line in filelines:
        #fline = filelines

       #if not fline:
           #continue
        #print

        #if fline:
            #print("INPUT: " + str(fline))
    #filename = "test.txt"
    #file = open(filename, "r")
    #for line in file:
       #print(line)

        content = file.read()

    # lexer
    # call the lexicalAnalyzer class and initialize it with the source code
        lex = lexer.Lexer(content)
    # we now call the tokenize method
    tokens = lex.tokenize()


main()

