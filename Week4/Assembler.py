import sys
from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable


def assemble(filename):
    parser = Parser(filename)
    symbols = SymbolTable()

    rom_address = 0

    while parser.hasMoreCommands():
        parser.advance()

        if parser.commandType() == "L_COMMAND":
            symbol = parser.symbol()
            if not symbols.contains(symbol):
                symbols.addEntry(symbol, rom_address)
        else:
            rom_address += 1

    parser = Parser(filename)
    next_variable = 16
    output = []

    while parser.hasMoreCommands():
        parser.advance()

        command_type = parser.commandType()

        if command_type == "L_COMMAND":
            continue

        if command_type == "A_COMMAND":
            symbol = parser.symbol()

            if symbol.isdigit():
                address = int(symbol)
            else:
                if not symbols.contains(symbol):
                    symbols.addEntry(symbol, next_variable)
                    next_variable += 1
                address = symbols.getAddress(symbol)

            output.append(format(address, "016b"))

        else:
            dest = Code.dest(parser.dest())
            comp = Code.comp(parser.comp())
            jump = Code.jump(parser.jump())

            output.append("111" + comp + dest + jump)

    with open(filename.rsplit(".", 1)[0] + ".hack", "w") as f:
        f.write("\n".join(output))


if __name__ == "__main__":
    assemble(sys.argv[1])