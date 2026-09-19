import sys
import os

from JackTokenizer import JackTokenizer
from CompilationEngineXML import CompilationEngineXML


def analyze_file(input_file):
    output_file = os.path.splitext(input_file)[0] + ".xml"

    tokenizer = JackTokenizer(input_file)

    with open(output_file, "w") as f:
        if tokenizer.hasMoreTokens():
            tokenizer.advance()

            engine = CompilationEngineXML(
                tokenizer,
                f
            )

            engine.compileClass()


def main():
    if len(sys.argv) != 2:
        print("Usage: python JackAnalyzerMain.py <file.jack>")
        return

    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith(".jack"):
                analyze_file(
                    os.path.join(input_path, filename)
                )
    else:
        analyze_file(input_path)


if __name__ == "__main__":
    main()