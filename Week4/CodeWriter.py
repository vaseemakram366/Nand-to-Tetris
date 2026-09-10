class CodeWriter:
    def __init__(self, output_file):
        self.file = open(output_file, "w")
        self.filename = ""
        self.label_count = 0
        self.call_count = 0
        self.current_function = ""

    def setFileName(self, filename):
        self.filename = filename

    def writeArithmetic(self, command):
        if command == "neg":
            self.file.write("@SP\nA=M-1\nM=-M\n")

        elif command == "not":
            self.file.write("@SP\nA=M-1\nM=!M\n")

        elif command in ("add", "sub", "and", "or"):
            operations = {
                "add": "M=M+D",
                "sub": "M=M-D",
                "and": "M=M&D",
                "or": "M=M|D"
            }

            self.file.write(
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                "A=A-1\n"
                + operations[command] + "\n"
            )

        elif command in ("eq", "gt", "lt"):
            jumps = {
                "eq": "JEQ",
                "gt": "JGT",
                "lt": "JLT"
            }

            true_label = f"TRUE{self.label_count}"
            end_label = f"END{self.label_count}"
            self.label_count += 1

            self.file.write(
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                "A=A-1\n"
                "D=M-D\n"
                f"@{true_label}\n"
                f"D;{jumps[command]}\n"
                "@SP\n"
                "A=M-1\n"
                "M=0\n"
                f"@{end_label}\n"
                "0;JMP\n"
                f"({true_label})\n"
                "@SP\n"
                "A=M-1\n"
                "M=-1\n"
                f"({end_label})\n"
            )

    def writePushPop(self, command, segment, index):
        if command == "C_PUSH":
            if segment == "constant":
                self.file.write(
                    f"@{index}\n"
                    "D=A\n"
                )

            elif segment in ("local", "argument", "this", "that"):
                base = {
                    "local": "LCL",
                    "argument": "ARG",
                    "this": "THIS",
                    "that": "THAT"
                }[segment]

                self.file.write(
                    f"@{index}\n"
                    "D=A\n"
                    f"@{base}\n"
                    "A=M+D\n"
                    "D=M\n"
                )

            elif segment == "temp":
                self.file.write(
                    f"@{5 + index}\n"
                    "D=M\n"
                )

            elif segment == "pointer":
                pointer = "THIS" if index == 0 else "THAT"
                self.file.write(
                    f"@{pointer}\n"
                    "D=M\n"
                )

            elif segment == "static":
                self.file.write(
                    f"@{self.filename}.{index}\n"
                    "D=M\n"
                )

            self.file.write(
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"
            )

        elif command == "C_POP":
            if segment in ("local", "argument", "this", "that"):
                base = {
                    "local": "LCL",
                    "argument": "ARG",
                    "this": "THIS",
                    "that": "THAT"
                }[segment]

                self.file.write(
                    f"@{base}\n"
                    "D=M\n"
                    f"@{index}\n"
                    "D=D+A\n"
                    "@R13\n"
                    "M=D\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "@R13\n"
                    "A=M\n"
                    "M=D\n"
                )

            elif segment == "temp":
                self.file.write(
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    f"@{5 + index}\n"
                    "M=D\n"
                )

            elif segment == "pointer":
                pointer = "THIS" if index == 0 else "THAT"

                self.file.write(
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    f"@{pointer}\n"
                    "M=D\n"
                )

            elif segment == "static":
                self.file.write(
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    f"@{self.filename}.{index}\n"
                    "M=D\n"
                )

    def writeLabel(self, label):
        self.file.write(f"({self.current_function}${label})\n")

    def writeGoto(self, label):
        self.file.write(
            f"@{self.current_function}${label}\n"
            "0;JMP\n"
        )

    def writeIf(self, label):
        self.file.write(
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            f"@{self.current_function}${label}\n"
            "D;JNE\n"
        )

    def writeFunction(self, function_name, num_locals):
        self.current_function = function_name

        self.file.write(f"({function_name})\n")

        for _ in range(num_locals):
            self.writePushPop("C_PUSH", "constant", 0)

    def writeCall(self, function_name, num_args):
        return_label = f"RETURN{self.call_count}"
        self.call_count += 1

        self.file.write(
            f"@{return_label}\n"
            "D=A\n"
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
        )

        for segment in ("LCL", "ARG", "THIS", "THAT"):
            self.file.write(
                f"@{segment}\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"
            )

        self.file.write(
            "@SP\n"
            "D=M\n"
            f"@{num_args}\n"
            "D=D-A\n"
            "@5\n"
            "D=D-A\n"
            "@ARG\n"
            "M=D\n"
            "@SP\n"
            "D=M\n"
            "@LCL\n"
            "M=D\n"
            f"@{function_name}\n"
            "0;JMP\n"
            f"({return_label})\n"
        )

    def writeReturn(self):
        self.file.write(
            "@LCL\n"
            "D=M\n"
            "@R13\n"
            "M=D\n"
            "@5\n"
            "A=D-A\n"
            "D=M\n"
            "@R14\n"
            "M=D\n"
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "@ARG\n"
            "A=M\n"
            "M=D\n"
            "@ARG\n"
            "D=M+1\n"
            "@SP\n"
            "M=D\n"
            "@R13\n"
            "AM=M-1\n"
            "D=M\n"
            "@THAT\n"
            "M=D\n"
            "@R13\n"
            "AM=M-1\n"
            "D=M\n"
            "@THIS\n"
            "M=D\n"
            "@R13\n"
            "AM=M-1\n"
            "D=M\n"
            "@ARG\n"
            "M=D\n"
            "@R13\n"
            "AM=M-1\n"
            "D=M\n"
            "@LCL\n"
            "M=D\n"
            "@R14\n"
            "A=M\n"
            "0;JMP\n"
        )

    def writeInit(self):
        self.file.write(
            "@256\n"
            "D=A\n"
            "@SP\n"
            "M=D\n"
        )
        self.writeCall("Sys.init", 0)

    def close(self):
        self.file.close()