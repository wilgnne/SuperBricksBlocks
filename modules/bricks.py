import random

class Vector2():
	"""docstring for Vector2"""
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return 'Vector2({}, {})'.format(self.x, self.y)

	def translate(self, vector2):
		self.x += vector2.x
		self.y += vector2.y

class GameObject():
	"""docstring for GameObject"""
	def __init__(self, position = Vector2(0, 0)):
		self.position = position

	def setMesh(self, mesh):
		self.mesh = mesh

	def fazgirar(self):
		transposta = []
		for j in range(0, len(self.mesh[0])):
			linha = []
			for i in range(0, len(self.mesh)):
				linha.append(self.mesh[i][j])
			transposta.append(linha)
		espelhada = []
		for i in transposta[::-1]:
			espelhada.append(i)
		self.setMesh(espelhada)

		if len(self.mesh[0]) + self.position.x > 10:
			rtn = (len(self.mesh[0]) + self.position.x) - 10
			self.position.translate(Vector2(-rtn, 0))

def randomVector2(exep = []):
	fim = False
	while fim == False:
		fim = True
		x = random.randint(0, 9)
		y = random.randint(0, 19)
		for elem in exep:
			if x == elem.position.x and y == elem.position.y:
				fim = False
	return Vector2(x, y)