from colorama import init, Fore, Style
from .lex import lex, LexError
from .parse import parse, ParseError
from .ident_table import IdentTable
import sys

def repl():
    init()
    table = IdentTable()

    while True:
        sys.stderr.write(Fore.CYAN + 'rafmat> ' + Style.RESET_ALL)
        command = input()
        if command == "exit":
            break

        try:
            node = parse(lex(command))
            try:
                res = node.eval(table)
                print(Fore.GREEN + str(round(res, 3)))
            except RuntimeError as e:
                print((Fore.RED + "Runtime error: ") + (Style.RESET_ALL + str(e)))
        except ParseError as e:
            print((Fore.RED + "Parse error: ") + (Style.RESET_ALL + e.message))
        except LexError as e:
            print((Fore.RED + "Lex error: ") + (Style.RESET_ALL + e.message))
