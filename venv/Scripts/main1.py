import lexer
import sys
def main():
    content = ""
    with open(sys.argv[1], 'r') as file:
        content = file.read()
        lex = lexer.Lexer(content)
    tokens = lex.tokenize()
main()
