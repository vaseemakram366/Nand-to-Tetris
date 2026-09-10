import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file(parser, writer):
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

        elif command_type == "C_LABEL":
            writer.writeLabel(parser.arg1())

        elif command_type == "C_GOTO":
            writer.writeGoto(parser.arg1())

        elif command_type == "C_IF":
            writer.writeIf(parser.arg1())

        elif command_type == "C_FUNCTION":
            writer.writeFunction(
                parser.arg1(),
                parser.arg2()
            )

        elif command_type == "C_CALL":
            writer.writeCall(
                parser.arg1(),
                parser.arg2()
            )

        elif command_type == "C_RETURN":
            writer.writeReturn()


def main():
    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        folder_name = os.path.basename(
            os.path.normpath(input_path)
        )

        output_path = os.path.join(
            input_path,
            folder_name + ".asm"
        )

        vm_files = [
            os.path.join(input_path, file)
            for file in os.listdir(input_path)
            if file.endswith(".vm")
        ]

        writer = CodeWriter(output_path)
        writer.writeInit()

        for vm_file in vm_files:
            writer.setFileName(
                os.path.basename(vm_file)
            )

            parser = Parser(vm_file)
            translate_file(parser, writer)

        writer.close()

    else:
        output_path = os.path.splitext(input_path)[0] + ".asm"

        writer = CodeWriter(output_path)
        writer.setFileName(
            os.path.basename(input_path)
        )

        parser = Parser(input_path)
        translate_file(parser, writer)

        writer.close()


if __name__ == "__main__":
    main()