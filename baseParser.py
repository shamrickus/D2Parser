from utils import headerParse

class BaseParser:
	def __init__(self, line):
		self.raw = {}
		for prop in line:
			self.raw[headerParse(prop)] = line[prop]

	@staticmethod
	def getName():
		return "ERROR"

	def verify(self):
		return True

	def json(self):
		return "ERROR"

	def format(self, list):
		return "[\"" + "\",\"".join(x for x in list) + "\"]"
