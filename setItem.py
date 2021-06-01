from baseEquipment import BaseEquipment


class SetItemParser(BaseEquipment):
    def __init__(self, line):
        self.lvl = "0"
        self.lvlReq = "0"
        self.enabled = "1"
        self.set = ""

        BaseEquipment.__init__(self, line)

    def parse(self, parser):
        self.name = self.raw["index"]
        self.lvl = self.raw["lvl"]
        self.lvlReq = self.raw["lvlreq"]
        self.set = self.raw["set"]

        self.parseProperties(9, "prop{}", "par{}", "min{}", "max{}", parser)
        # TODO Set props

    def verify(self):
        return self.name and self.enabled == "1"

    @staticmethod
    def getName():
        return "setitems"
