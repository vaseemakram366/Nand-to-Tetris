class CompilationEngine:
    def __init__(self, tokenizer, vm_writer, symbol_table):
        self.tokenizer = tokenizer
        self.vm_writer = vm_writer
        self.symbol_table = symbol_table
        self.class_name = ""
        self.label_count = 0

    def advance(self):
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    def current(self):
        return self.tokenizer.current

    def eat(self, value=None):
        if value is not None and self.current() != value:
            raise SyntaxError(
                f"Expected {value}, got {self.current()}"
            )
        self.advance()

    def compileClass(self):
        self.eat("class")

        self.class_name = self.current()
        self.eat()

        self.eat("{")

        while self.current() in ("static", "field"):
            self.compileClassVarDec()

        while self.current() in ("constructor", "function", "method"):
            self.compileSubroutine()

        self.eat("}")

    def compileClassVarDec(self):
        kind = self.current()
        self.eat()

        type_name = self.current()
        self.eat()

        while True:
            name = self.current()
            self.symbol_table.define(name, type_name, kind)
            self.eat()

            if self.current() != ",":
                break

            self.eat(",")

        self.eat(";")

    def compileSubroutine(self):
        subroutine_type = self.current()
        self.eat()

        self.eat()

        name = self.current()
        self.eat()

        self.symbol_table.startSubroutine()

        if subroutine_type == "method":
            self.symbol_table.define(
                "this",
                self.class_name,
                "argument"
            )

        self.eat("(")
        self.compileParameterList()
        self.eat(")")

        self.eat("{")

        while self.current() == "var":
            self.compileVarDec()

        n_locals = self.symbol_table.varCount("var")

        self.vm_writer.writeFunction(
            f"{self.class_name}.{name}",
            n_locals
        )

        if subroutine_type == "constructor":
            fields = self.symbol_table.varCount("field")
            self.vm_writer.writePush("constant", fields)
            self.vm_writer.writeCall("Memory.alloc", 1)
            self.vm_writer.writePop("pointer", 0)

        elif subroutine_type == "method":
            self.vm_writer.writePush("argument", 0)
            self.vm_writer.writePop("pointer", 0)

        self.compileStatements()
        self.eat("}")

    def compileParameterList(self):
        if self.current() == ")":
            return

        while True:
            type_name = self.current()
            self.eat()

            name = self.current()
            self.symbol_table.define(
                name,
                type_name,
                "argument"
            )
            self.eat()

            if self.current() != ",":
                break

            self.eat(",")

    def compileVarDec(self):
        self.eat("var")

        type_name = self.current()
        self.eat()

        while True:
            name = self.current()
            self.symbol_table.define(
                name,
                type_name,
                "var"
            )
            self.eat()

            if self.current() != ",":
                break

            self.eat(",")

        self.eat(";")

    def compileStatements(self):
        while self.current() in (
            "let",
            "if",
            "while",
            "do",
            "return"
        ):
            if self.current() == "let":
                self.compileLet()

            elif self.current() == "if":
                self.compileIf()

            elif self.current() == "while":
                self.compileWhile()

            elif self.current() == "do":
                self.compileDo()

            elif self.current() == "return":
                self.compileReturn()

    def compileLet(self):
        self.eat("let")

        name = self.current()
        self.eat()

        self.eat("=")

        self.compileExpression()

        kind = self.symbol_table.kindOf(name)
        index = self.symbol_table.indexOf(name)

        segment = self.kindToSegment(kind)

        self.vm_writer.writePop(segment, index)

        self.eat(";")

    def compileIf(self):
        self.eat("if")

        true_label = self.newLabel("IF_TRUE")
        false_label = self.newLabel("IF_FALSE")
        end_label = self.newLabel("IF_END")

        self.eat("(")
        self.compileExpression()
        self.eat(")")

        self.vm_writer.writeIf(true_label)
        self.vm_writer.writeGoto(false_label)
        self.vm_writer.writeLabel(true_label)

        self.eat("{")
        self.compileStatements()
        self.eat("}")

        if self.current == "else":
            self.vm_writer.writeGoto(end_label)
            self.vm_writer.writeLabel(false_label)

            self.eat("else")
            self.eat("{")
            self.compileStatements()
            self.eat("}")

            self.vm_writer.writeLabel(end_label)

        else:
            self.vm_writer.writeLabel(false_label)

    def compileWhile(self):
        self.eat("while")

        start_label = self.newLabel("WHILE_EXP")
        end_label = self.newLabel("WHILE_END")

        self.vm_writer.writeLabel(start_label)

        self.eat("(")
        self.compileExpression()
        self.eat(")")

        self.vm_writer.writeArithmetic("not")
        self.vm_writer.writeIf(end_label)

        self.eat("{")
        self.compileStatements()
        self.eat("}")

        self.vm_writer.writeGoto(start_label)
        self.vm_writer.writeLabel(end_label)

    def compileDo(self):
        self.eat("do")

        self.compileSubroutineCall()

        self.vm_writer.writePop("temp", 0)

        self.eat(";")

    def compileReturn(self):
        self.eat("return")

        if self.current == ";":
            self.vm_writer.writePush("constant", 0)
        else:
            self.compileExpression()

        self.vm_writer.writeReturn()

        self.eat(";")

    def compileExpression(self):
        self.compileTerm()

        operators = {
            "+": "add",
            "-": "sub",
            "*": "call Math.multiply 2",
            "/": "call Math.divide 2",
            "&": "and",
            "|": "or",
            "<": "lt",
            ">": "gt",
            "=": "eq"
        }

        while self.current in operators:
            op = self.current
            self.eat()

            self.compileTerm()

            command = operators[op]

            if command.startswith("call"):
                parts = command.split()
                self.vm_writer.writeCall(
                    parts[1],
                    int(parts[2])
                )
            else:
                self.vm_writer.writeArithmetic(command)

    def compileTerm(self):
        token_type = self.tokenizer.tokenType()

        if token_type == "INT_CONST":
            self.vm_writer.writePush(
                "constant",
                self.tokenizer.intVal()
            )
            self.eat()

        elif token_type == "STRING_CONST":
            value = self.tokenizer.stringVal()

            self.vm_writer.writePush(
                "constant",
                len(value)
            )
            self.vm_writer.writeCall(
                "String.new",
                1
            )

            for char in value:
                self.vm_writer.writePush(
                    "constant",
                    ord(char)
                )
                self.vm_writer.writeCall(
                    "String.appendChar",
                    2
                )

            self.eat()

        elif token_type == "KEYWORD":
            keyword = self.current

            if keyword == "true":
                self.vm_writer.writePush("constant", 0)
                self.vm_writer.writeArithmetic("not")

            elif keyword in ("false", "null"):
                self.vm_writer.writePush("constant", 0)

            elif keyword == "this":
                self.vm_writer.writePush("pointer", 0)

            self.eat()

        elif token_type == "IDENTIFIER":
            name = self.current
            self.eat()

            if self.current == "[":
                self.eat("[")
                self.compileExpression()
                self.eat("]")

                kind = self.symbol_table.kindOf(name)
                index = self.symbol_table.indexOf(name)

                self.vm_writer.writePush(
                    self.kindToSegment(kind),
                    index
                )
                self.vm_writer.writeArithmetic("add")
                self.vm_writer.writePop("pointer", 1)
                self.vm_writer.writePush("that", 0)

            elif self.current in ("(", "."):
                self.compileSubroutineCallAfterName(name)

            else:
                kind = self.symbol_table.kindOf(name)
                index = self.symbol_table.indexOf(name)

                self.vm_writer.writePush(
                    self.kindToSegment(kind),
                    index
                )

        elif self.current == "(":
            self.eat("(")
            self.compileExpression()
            self.eat(")")

        elif self.current in ("-", "~"):
            op = self.current
            self.eat()

            self.compileTerm()

            self.vm_writer.writeArithmetic(
                "neg" if op == "-" else "not"
            )

    def compileSubroutineCall(self):
        name = self.current
        self.eat()

        self.compileSubroutineCallAfterName(name)

    def compileSubroutineCallAfterName(self, name):
        n_args = 0

        if self.current == ".":
            self.eat(".")

            subroutine = self.current
            self.eat()

            kind = self.symbol_table.kindOf(name)

            if kind != "NONE":
                self.vm_writer.writePush(
                    self.kindToSegment(kind),
                    self.symbol_table.indexOf(name)
                )
                n_args = 1
                full_name = (
                    self.symbol_table.typeOf(name)
                    + "."
                    + subroutine
                )
            else:
                full_name = name + "." + subroutine

        else:
            self.vm_writer.writePush("pointer", 0)
            n_args = 1
            full_name = self.class_name + "." + name

        self.eat("(")

        n_args += self.compileExpressionList()

        self.eat(")")

        self.vm_writer.writeCall(full_name, n_args)

    def compileExpressionList(self):
        count = 0

        if self.current == ")":
            return 0

        while True:
            self.compileExpression()
            count += 1

            if self.current != ",":
                break

            self.eat(",")

        return count

    def kindToSegment(self, kind):
        return {
            "static": "static",
            "field": "this",
            "argument": "argument",
            "var": "local"
        }.get(kind, "local")

    def newLabel(self, prefix):
        label = f"{prefix}{self.label_count}"
        self.label_count += 1
        return label