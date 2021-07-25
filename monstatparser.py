from baseParser import BaseParser

class MonStatParser(BaseParser):
    def __init__(self, line):
        self.id = ""
        self.name = ""
        BaseParser.__init__(self, line)

    def parse(self, parser: "Parser"):
        self.id = self.raw["hcIdx"]
        self.name = self.raw["NameStr"]

    def verify(self):
        return self.id != "" and self.name != ""

    @staticmethod
    def getName():
        return "monstats"
