import grafica.scene_graph as sg
import grafica.transformations as tr

class GameObject:

	def __init__(self, nombre, pipeline):
		self.DEG_TO_RAD = 0.0174533

		self.nombre = nombre

		self.position = (0, 0, 0)
		self.rotation = (0, 0, 0) # rotacion en grados
		self.scale = (1, 1, 1)
		self.time = 0

		self.pipeline = pipeline
		self.nodo = sg.SceneGraphNode(nombre)
		self.nodo.transform = tr.matmul([tr.translate(0,0,0), tr.scale(0.1,0.1,0.1)])
		self.nodo.childs = []
	
	# En particular, un GameObject con modelo no puede tener mas hijos
	def setModel(self, modelo):
		self.nodo.childs = [modelo]

	def addChilds(self, childList):	
		self.nodo.childs += childList

	def setPosition(position_vector):
		self.position = position_array

	def translate(position_vector):
		self.position = self.position + position_vector

	def setRotation(rotation_vector):
		self.rotation = rotation_vector

	def rotate(rotation_vector):
		self.rotation = self.rotation + rotation_vector

	def setScale(scale_vector):
		self.scale = scale_vector			

	def clear(self):
		self.nodo.clear()

	def update(self, deltaTime):
		self.time += deltaTime
		self.nodo.transform = tr.matmul([

				tr.translate(self.position[0], self.position[1], self.position[2]),
				tr.rotationX(self.rotation[0] * self.DEG_TO_RAD),
				tr.rotationY(self.rotation[1] * self.DEG_TO_RAD),
                tr.rotationZ(self.rotation[2] * self.DEG_TO_RAD),
                tr.scale(self.scale[0], self.scale[1], self.scale[2])
			])
		sg.drawSceneGraphNode(self.nodo, self.pipeline, "model")					