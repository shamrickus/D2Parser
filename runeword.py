from baseEquipment import BaseEquipment

class RunewordParser(BaseEquipment):
    def __init__(self, line):
        self.name = ""
        self.complete = 0
        self.itypes = []
        self.etypes = []
        self.runes = []
        self.props = []
        BaseEquipment.__init__(self, line)

    def parse(self, parser):
        self.name = self.raw["RuneName"]
        self.complete = self.raw["complete"]
        for i in range(1, 8):
            if i < 4:
                if self.raw['etype' + str(i)] != '':
                    self.etypes.append(self.raw['etype' + str(i)])
            if i < 7:
                if self.raw['itype' + str(i)] != '':
                    self.itypes.append(self.raw["itype" + str(i)])
                if self.raw['Rune' + str(i)] != '':
                    self.runes.append(self.raw['Rune' + str(i)])
        self.parseProperties(8, "T1Code{}", "T1Param{}", "T1Min{}", "T1Max{}", parser)

    def verify(self):
        return self.name and self.complete == str(1)

    def json(self):
        runes = self.format([str(x) for x in self.runes])
        props = self.format([str(x.parsed) for x in self.props])
        types = self.formatObj([x.json() for x in self.itypes])
        out = "{" + \
              "\"Name\":\"{}\",\"classRestriction\": null, \"Runes\":{},\"Version\":\"{}\",\"Properties\":{},\"Type\":{}".format(self.name, runes, "TEST", props, types) + \
              "}"

        return out


    @staticmethod
    def getName():
        return "runes"



