from baseParser import BaseParser

class ItemType(BaseParser):
    def __init__(self, line):
        self.name = ""
        self.code = ""
        self.equiv = ""
        self.equiv1 = ""
        self.children = []
        self.parents = []
        BaseParser.__init__(self, line)

    def parse(self, parser):
        self.name = self.raw["ItemType"]
        self.code = self.raw["Code"]
        self.equiv = self.raw["Equiv1"]
        self.equiv1 = self.raw["Equiv2"]

    def __str__(self):
        return self.name + ", " + self.code + ", " + self.equiv + ", " + self.equiv1

    def verify(self):
        return self.name != "None" and self.name != "Not Used"

    @staticmethod
    def getName():
        return "ItemTypes"

    def hasChildren(self):
        return len(self.chidlren) > 1

    def parseItems(self, itemAgg):
        d = 2

    def isShield(self) -> bool:
        return self.code in ["shld", "shie", "boot", 'head', 'ashd', 'phlm', 'pelt', 'circ', 'pala']

    def isWeapon(self) -> bool:
        if self.code in ['club', 'mele', 'glov', 'scep', 'wand', 'staf', \
                         'bow', 'xbow', 'axe', 'swor', 'hamm', 'knif', \
                         'spear', 'pole', 'mace', 'tkni', 'taxe', 'jave', 'weap', \
                         'abow', 'aspe', 'ajav', 'mboq', 'mxbq'] \
                or self.equiv in ['weap', 'rod', 'mele', 'blun', 'comb']:
            return True
        return False

    def isArmor(self):
        if self.code in ['tors', 'ring', 'amul', 'belt', 'helm', 'armo', 'cloa']:
            return True
        return False

    def getTypeStr(self):
        type = None
        if self.isShield():
            type = "Shield"
        elif self.isWeapon():
            type = "Weapon"
        elif self.isArmor():
            type = "Armor"
        return type

    def json(self):
        retStr = "{\"name\": \"%s\", \"children\":[" % self.name
        for c in self.children:
            retStr += c.json() + ","
        retStr += "]}"
        return retStr

    def allParents(self):
        parents = []
        parents.extend(self.parents)
        for p in self.parents:
            parents.extend(p.allParents())
        return parents


    def allChildren(self):
        children = []
        children.extend(self.children)
        for c in self.children:
            children.extend(c.allChildren())
        return children
