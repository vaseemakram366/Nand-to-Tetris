class CompilationEngineXML:

    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output = output_file
        self.indent = 0

    def write(self, text):
        self.output.write("  " * self.indent + text + "\n")

    def escape(self, value):
        return (
            value.replace("&", "&amp;")
                 .replace("<", "&lt;")
                 .replace(">", "&gt;")
        )

    def advance(self):
        self.tokenizer.advance()

    def current(self):
        return self.tokenizer.current

    def tokenType(self):
        return self.tokenizer.tokenType()

    def eat(self, value=None):
        if value is not None and self.current() != value:
            raise SyntaxError(
                f"Expected {value}, got {self.current()}"
            )

        token = self.current()
        token_type = self.tokenType()

        if token_type == "KEYWORD":
            tag = "keyword"
        elif token_type == "SYMBOL":
            tag = "symbol"
        elif token_type == "IDENTIFIER":
            tag = "identifier"
        elif token_type == "INT_CONST":
            tag = "integerConstant"
        elif token_type == "STRING_CONST":
            tag = "stringConstant"
            token = self.tokenizer.stringVal()
        else:
            raise SyntaxError("Invalid token")

        token = self.escape(token)

        self.write(f"<{tag}> {token} </{tag}>")
        self.advance()

    def compileClass(self):
        self.write("<class>")
        self.indent += 1

        self.eat("class")
        self.eat()

        self.eat("{")

        while self.current() in ("static", "field"):
            self.compileClassVarDec()

        while self.current() in (
            "constructor",
            "function",
            "method"
        ):
            self.compileSubroutine()

        self.eat("}")

        self.indent -= 1
        self.write("</class>")

    def compileClassVarDec(self):
        self.write("<classVarDec>")
        self.indent += 1

        self.eat()
        self.eat()
        self.eat()

        while self.current() == ",":
            self.eat(",")
            self.eat()

        self.eat(";")

        self.indent -= 1
        self.write("</classVarDec>")

    def compileSubroutine(self):
        self.write("<subroutineDec>")
        self.indent += 1

        self.eat()
        self.eat()
        self.eat()

        self.eat("(")
        self.compileParameterList()
        self.eat(")")

        self.compileSubroutineBody()

        self.indent -= 1
        self.write("</subroutineDec>")

    def compileParameterList(self):
        self.write("<parameterList>")
        self.indent += 1

        if self.current() != ")":
            self.eat()
            self.eat()

            while self.current() == ",":
                self.eat(",")
                self.eat()
                self.eat()

        self.indent -= 1
        self.write("</parameterList>")

    def compileSubroutineBody(self):
        self.write("<subroutineBody>")
        self.indent += 1

        self.eat("{")

        while self.current() == "var":
            self.compileVarDec()

        self.compileStatements()

        self.eat("}")

        self.indent -= 1
        self.write("</subroutineBody>")

    def compileVarDec(self):
        self.write("<varDec>")
        self.indent += 1

        self.eat("var")
        self.eat()
        self.eat()

        while self.current() == ",":
            self.eat(",")
            self.eat()

        self.eat(";")

        self.indent -= 1
        self.write("</varDec>")

    def compileStatements(self):
        self.write("<statements>")
        self.indent += 1

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
            else:
                self.compileReturn()

        self.indent -= 1
        self.write("</statements>")

    def compileLet(self):
        self.write("<letStatement>")
        self.indent += 1

        self.eat("let")
        self.eat()

        if self.current() == "[":
            self.eat("[")
            self.compileExpression()
            self.eat("]")

        self.eat("=")
        self.compileExpression()
        self.eat(";")

        self.indent -= 1
        self.write("</letStatement>")

    def compileIf(self):
        self.write("<ifStatement>")
        self.indent += 1

        self.eat("if")
        self.eat("(")
        self.compileExpression()
        self.eat(")")

        self.eat("{")
        self.compileStatements()
        self.eat("}")

        if self.current() == "else":
            self.eat("else")
            self.eat("{")
            self.compileStatements()
            self.eat("}")

        self.indent -= 1
        self.write("</ifStatement>")

    def compileWhile(self):
        self.write("<whileStatement>")
        self.indent += 1

        self.eat("while")
        self.eat("(")
        self.compileExpression()
        self.eat(")")

        self.eat("{")
        self.compileStatements()
        self.eat("}")

        self.indent -= 1
        self.write("</whileStatement>")

    def compileDo(self):
        self.write("<doStatement>")
        self.indent += 1

        self.eat("do")
        self.eat()

        if self.current() == ".":
            self.eat(".")
            self.eat()

        self.eat("(")
        self.compileExpressionList()
        self.eat(")")
        self.eat(";")

        self.indent -= 1
        self.write("</doStatement>")

    def compileReturn(self):
        self.write("<returnStatement>")
        self.indent += 1

        self.eat("return")

        if self.current() != ";":
            self.compileExpression()

        self.eat(";")

        self.indent -= 1
        self.write("</returnStatement>")

    def compileExpression(self):
        self.write("<expression>")
        self.indent += 1

        self.compileTerm()

        while self.current() in (
            "+", "-", "*", "/", "&",
            "|", "<", ">", "="
        ):
            self.eat()
            self.compileTerm()

        self.indent -= 1
        self.write("</expression>")

    def compileTerm(self):
        self.write("<term>")
        self.indent += 1

        if self.current() in ("-", "~"):
            self.eat()
            self.compileTerm()

        elif self.current() == "(":
            self.eat("(")
            self.compileExpression()
            self.eat(")")

        else:
            self.eat()

            if self.current() == "[":
                self.eat("[")
                self.compileExpression()
                self.eat("]")

            elif self.current() in ("(", "."):
                if self.current() == ".":
                    self.eat(".")
                    self.eat()

                self.eat("(")
                self.compileExpressionList()
                self.eat(")")

        self.indent -= 1
        self.write("</term>")

    def compileExpressionList(self):
        self.write("<expressionList>")
        self.indent += 1

        if self.current() != ")":
            self.compileExpression()

            while self.current() == ",":
                self.eat(",")
                self.compileExpression()

        self.indent -= 1
        self.write("</expressionList>")