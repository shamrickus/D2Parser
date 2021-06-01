from baseParser import BaseParser
from property import Property

_slots = ["Weapon", "Armor", "Shield"]
class GemsParser(BaseParser):
    def __str__(self):
        out = "name: {}, letter: {}, transform: {}, code: {}, mods: {}, gem: {}, rune: {}\r\n\t".format(self.name, self.letter, self.transform, self.code, self.mods, self.isGem(), self.isRune())
        for type in self._props:
            out+= type + ":\r\n\t"
            for prop in self._props[type]:
                out += "\t" + str(prop) + "\r\n\t"
        return out

    def json(self):
        out = "{" + "\"name\": \"{}\", \"letter\": \"{}\", \"transform\": \"{}\", \"code\": \"{}\", \"mods\": \"{}\", \"gem\": \"{}\", \"rune\": \"{}\",".format(self.name, self.letter, self.transform, self.code, self.mods, self.isGem(), self.isRune())
        out += "\"Properties\": ["
        for type in self._props:
            out+= "{\"" + type + "\": ["
            for prop in self._props[type]:
                out += prop.json() + ","
            out+= "]},"
        return out + "]}"

    def isRune(self):
        return self.code.startswith('r')

    def isGem(self):
        return not self.isRune()

    def __init__(self, parseLine):
        self.name = ""
        self.letter = ""
        self.transform = 0
        self.code = ""
        self.mods = 0
        self._props = {}
        for slot in _slots:
            self._props[slot] = []
        BaseParser.__init__(self, parseLine)

    def Name(self):
        if self.isRune():
            return "rune" + self.letter[:4].replace('Jah', 'Jo')
        else:
            return self.name.replace('FlwlessSaphire', "FlawlessSaphire")

    def FileName(self):
        if self.isRune():
            return self.letter
        else:
            return self.name.replace('FlwlessSaphire', 'FlawlessSaphire')

    def parse(self, parser: "Parser"):
        if(self.raw["name"] == "Expansion"):
            return
        self.name = self.raw["name"]
        self.letter = self.raw["letter"]
        self.transform = self.raw["transform"]
        self.code = self.raw["code"]
        self.mods = int(self.raw["nummods"])
        if(self.valid() and self.isRune()):
            self.mods = 2
        elif(self.valid and self.isGem()):
            self.mods = self.mods
        for slot in _slots:
            for i in range(1, self.mods + 1):
                propName = ""
                if slot == "Weapon":
                    propName = "weapon"
                elif slot == "Armor":
                    propName = "helm"
                elif slot == "Shield":
                    propName = "shield"
                prop = Property(self.raw[propName + "Mod" + str(i) + "Code"], self.raw[propName + "Mod" + str(i) + "Param"],
                                self.raw[propName + "Mod" + str(i) + "Min"], self.raw[propName + "Mod" + str(i) + "Max"])

                if prop is None or prop.prop is None:
                    continue
                self._props[slot].append(prop)
            parser.parse(self._props[slot])

    def valid(self):
        return self.name != None

    def fileName(self):
        if self.isRune():
            return 'runes'
        else:
            return "gems"


    @staticmethod
    def getName():
        return "gems"


if __name__ == "__main__":
    Items = BaseParser.read(GemsParser)
    gems = open("gems.ts", "w")
    gems.write("export const gems = [")
    runes = open("runes.ts", "w")
    runes.write("export const runes = [")
    for item in Items:
        if item.isGem():
            gems.write(item.json() + ",")
        elif item.isRune():
            runes.write(item.json() + ",")
    gems.write("];")
    runes.write("];")
    gems.close()
    runes.close()

