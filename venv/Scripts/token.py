class Token:
	def __init__(self, val, tokenTypeVal):
		self.value = val
		self.tokenType = tokenTypeVal
		#self.depth = depthVal
	def getValue(self):
		return self.value
	def getType(self):
		return self.tokenType
	#def getDepth(self):
	#	return self.depth