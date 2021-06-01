from baseEquipment import BaseEquipment


class UniqueParser(BaseEquipment):
    def __init__(self, line):
        self.lvl = "0"
        self.lvlReq = "0"
        self.enabled = "1"

        BaseEquipment.__init__(self, line)

    def parse(self, parser):
        self.name = self.raw["index"]
        self.lvl = self.raw["lvl"]
        self.lvlReq = self.raw["lvlreq"]
        self.enabled = self.raw["enabled"]

        self.parseProperties(12, "prop{}", "par{}", "min{}", "max{}", parser)

    def verify(self):
        return self.name and self.enabled == "1"

    @staticmethod
    def getName():
        return "uniqueitems"
