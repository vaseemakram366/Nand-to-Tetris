import re


class JackTokenizer:
    KEYWORDS = {
        "class", "constructor", "function", "method",
        "field", "static", "var", "int", "char", "boolean",
        "void", "true", "false", "null", "this",
        "let", "do", "if", "else", "while", "return"
    }

    SYMBOLS = set("{}()[].,;+-*/&|<>=~")

    def __init__(self, filename):
        with open(filename, "r") as f:
            text = f.read()

        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        text = re.sub(r"//.*", "", text)

        pattern = r'"[^"\n]*"|[{}()\[\].,;+\-*/&|<>=~]|[A-Za-z_]\w*|\d+'
        self.tokens = re.findall(pattern, text)

        self.index = -1
        self.current = None

    def hasMoreTokens(self):
        return self.index + 1 < len(self.tokens)

    def advance(self):
        self.index += 1
        self.current = self.tokens[self.index]

    def tokenType(self):
        token = self.current

        if token in self.KEYWORDS:
            return "KEYWORD"

        if token in self.SYMBOLS:
            return "SYMBOL"

        if token.startswith('"'):
            return "STRING_CONST"

        if token.isdigit():
            return "INT_CONST"

        return "IDENTIFIER"

    def keyword(self):
        return self.current

    def symbol(self):
        return self.current

    def identifier(self):
        return self.current

    def intVal(self):
        return int(self.current)

    def stringVal(self):
        return self.current[1:-1]