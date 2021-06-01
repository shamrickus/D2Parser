
from baseParser import BaseParser


class SkillParser(BaseParser):
    def __init__(self, line):
        self.skill = ""
        self.id = 0
        self.desc = ""
        self.char = ""

        BaseParser.__init__(self, line)

    def parse(self, parser: "Parser"):
        self.skill = self.raw["skill"]
        self.id = self.raw["Id"]
        self.char = self.raw["charclass"]

    def __str__(self):
        return "Name:{}, Id:{}, Char: {}".format(self.skill,self.id,self.char)

    @staticmethod
    def getName():
        return "Skills"

