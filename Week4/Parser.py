class Parser:
    def __init__(self, filename):
        with open(filename, "r") as f:
            self.lines = [
                line.split("//")[0].strip()
                for line in f
                if line.split("//")[0].strip()
            ]
        self.index = -1
        self.current = None

    def hasMoreCommands(self):
        return self.index + 1 < len(self.lines)

    def advance(self):
        self.index += 1
        self.current = self.lines[self.index]

    def commandType(self):
        if self.current.startswith("@"):
            return "A_COMMAND"
        if self.current.startswith("("):
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self):
        if self.commandType() == "A_COMMAND":
            return self.current[1:]
        return self.current[1:-1]

    def dest(self):
        if "=" in self.current:
            return self.current.split("=")[0]
        return None

    def comp(self):
        command = self.current

        if "=" in command:
            command = command.split("=")[1]

        if ";" in command:
            command = command.split(";")[0]

        return command

    def jump(self):
        if ";" in self.current:
            return self.current.split(";")[1]
        return None