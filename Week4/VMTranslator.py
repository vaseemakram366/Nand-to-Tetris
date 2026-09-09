import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter


def main():
    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        name = os.path.basename(os.path.normpath(input_path))
        output_path = os.path.join(input_path, name + ".asm")

        vm_files = [
            os.path.join(input_path, f)
            for f in os.listdir(input_path)
            if f.endswith(".vm")
        ]
    else:
        output_path = os.path.splitext(input_path)[0] + ".asm"
        vm_files = [input_path]

    writer = CodeWriter(output_path)

    for vm_file in vm_files:
        parser = Parser(vm_file)
        writer.setFileName(os.path.basename(vm_file))

        while parser.hasMoreCommands():
            parser.advance()
            command_type = parser.commandType()

            if command_type == "C_ARITHMETIC":
                writer.writeArithmetic(parser.arg1())

            elif command_type in ("C_PUSH", "C_POP"):
                writer.writePushPop(
                    command_type,
                    parser.arg1(),
                    parser.arg2()
                )

    writer.close()


if __name__ == "__main__":
    main()