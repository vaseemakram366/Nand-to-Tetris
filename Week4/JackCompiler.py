import sys
import os

from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter
from CompilationEngine import CompilationEngine


def compile_file(input_file):
    output_file = os.path.splitext(input_file)[0] + ".vm"

    tokenizer = JackTokenizer(input_file)
    symbol_table = SymbolTable()
    vm_writer = VMWriter(output_file)

    if not tokenizer.hasMoreTokens():
        vm_writer.close()
        return

    tokenizer.advance()

    engine = CompilationEngine(
        tokenizer,
        vm_writer,
        symbol_table
    )

    engine.compileClass()
    vm_writer.close()


def main():
    if len(sys.argv) != 2:
        print("Usage: python JackCompiler.py <file.jack>")
        return

    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        jack_files = [
            os.path.join(input_path, file)
            for file in os.listdir(input_path)
            if file.endswith(".jack")
        ]

        for jack_file in jack_files:
            compile_file(jack_file)

    elif input_path.endswith(".jack"):
        compile_file(input_path)

    else:
        print("Please provide a .jack file or directory.")


if __name__ == "__main__":
    main()