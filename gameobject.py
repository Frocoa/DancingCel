import grafica.scene_graph as sg
import grafica.transformations as tr

class GameObject:

	def __init__(self, nombre, shape, pipeline):
		self.DEG_TO_RAD = 0.0174533

		self.position = [0, 0]
		self.rotation = 0
		self.scale = [1, 1, 1]
		self.modelo = shape

		self.time = 0

		self.pipeline = pipeline
		self.nodo = sg.SceneGraphNode(nombre)
		self.nodo.transform = tr.matmul([tr.translate(0,0,0), tr.scale(0.1,0.1,1.0)])
		self.nodo.childs = [self.modelo]

	def update(self, deltaTime):
		self.time += deltaTime
		self.nodo.transform = tr.matmul([

				tr.translate(self.position[0], self.position[1], 0),
                tr.rotationZ(self.rotation * self.DEG_TO_RAD),
                tr.scale(self.scale[0], self.scale[1], self.scale[2])
			])
		sg.drawSceneGraphNode(self.nodo, self.pipeline, "transform")		