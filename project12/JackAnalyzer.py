import sys
import os
from JackTokenizer import JackTokenizer


class JackAnalyzer:
    def __init__(self, input_file):
        self.tokenizer = JackTokenizer(input_file)
        self.output = []

    def escape(self, value):
        return (
            value.replace("&", "&amp;")
                 .replace("<", "&lt;")
                 .replace(">", "&gt;")
                 .replace('"', "&quot;")
        )

    def write(self, line):
        self.output.append(line)

    def analyze(self):
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            token_type = self.tokenizer.tokenType()
            token = self.tokenizer.current

            if token_type == "KEYWORD":
                self.write(
                    f"<keyword> {token} </keyword>"
                )

            elif token_type == "SYMBOL":
                self.write(
                    f"<symbol> {self.escape(token)} </symbol>"
                )

            elif token_type == "IDENTIFIER":
                self.write(
                    f"<identifier> {token} </identifier>"
                )

            elif token_type == "INT_CONST":
                self.write(
                    f"<integerConstant> {token} </integerConstant>"
                )

            elif token_type == "STRING_CONST":
                self.write(
                    f"<stringConstant> "
                    f"{self.tokenizer.stringVal()} "
                    f"</stringConstant>"
                )

    def save(self, output_file):
        with open(output_file, "w") as f:
            f.write("<tokens>\n")

            for line in self.output:
                f.write(line + "\n")

            f.write("</tokens>\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python JackAnalyzer.py <file.jack>")
        return

    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith(".jack"):
                input_file = os.path.join(input_path, filename)
                output_file = os.path.splitext(input_file)[0] + "T.xml"

                analyzer = JackAnalyzer(input_file)
                analyzer.analyze()
                analyzer.save(output_file)

    else:
        output_file = os.path.splitext(input_path)[0] + "T.xml"

        analyzer = JackAnalyzer(input_path)
        analyzer.analyze()
        analyzer.save(output_file)


if __name__ == "__main__":
    main()