from colorama import init, Fore, Style
from .lex import lex, LexError
from .parse import parse, ParseError
from .ident_table import IdentTable
from .dot import to_dot
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
                if len(sys.argv) == 2 and sys.argv[1] == '-dot':
                    print(to_dot(node))
                else:
                    res = node.eval(table)
                    res_s = ''
                    if type(res) == bool:
                        res_s = str(res)
                    else:
                        res_s = str(round(res, 3))

                    print(Fore.GREEN + res_s)
            except RuntimeError as e:
                sys.stderr.write((Fore.RED + "Runtime error: ") +
                        (Style.RESET_ALL + str(e)) + "\n")
        except ParseError as e:
            sys.stderr.write((Fore.RED + "Parse error: ") + (Style.RESET_ALL +
                e.message) + "\n")
        except LexError as e:
            sys.stderr.write((Fore.RED + "Lex error: ") + (Style.RESET_ALL +
                e.message) + "\n")

