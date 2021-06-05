import grafica.scene_graph as sg
import grafica.transformations as tr
import grafica.gpu_shape as gs
import numpy as np

class GameObject:

	def __init__(self, nombre, pipeline):
		self.DEG_TO_RAD = 0.0174533

		self.nombre = nombre

		self.position = [0, 0, 0]
		self.rotation = [0, 0, 0] # rotacion en grados
		self.scale = [1, 1, 1]
		self.childs = [] # gameobjects
		self.time = 0

		self.pipeline = pipeline
		self.nodo = sg.SceneGraphNode(nombre)
		self.nodo.transform = tr.matmul([tr.translate(0,0,0), tr.scale(0.1,0.1,0.1)])
		self.nodo.childs = []
	
	
	def setModel(self, modelo):
		self.nodo.childs = [modelo]

	# añade nodos que van a ser dibujados siempre en su posicion inicial
	def nodeAddChilds(self, childList):
		# En particular, un GameObject con modelo no puede tener mas hijos
		if len(self.nodo.childs) > 0:
			assert not isinstance(self.nodo.childs[0], gs.GPUShape) , "Un GameObject con modelo no puede tener mas hijos"

		self.nodo.childs += childList

	# añade hijos que son GameObjects, sirve para poder hacer que los hijos se muevan mientras siguen conectados al padre
	def addChilds(self, childList):	
		# En particular, un GameObject con modelo no puede tener mas hijos
		if len(self.nodo.childs) > 0:
			assert not isinstance(self.nodo.childs[0], gs.GPUShape) , "Un GameObject con modelo no puede tener mas hijos"

		for child in childList:
			self.childs += [child]
			self.nodo.childs += [child.nodo]

	def setPosition(self, position_array):
		self.position = position_array

	def translate(self, position_array):
		self.position = [
						self.position[0] + position_array[0],
						self.position[1] + position_array[1],
						self.position[2] + position_array[2]]

	def setRotation(self, rotation_array):
		self.rotation = rotation_array

	def rotate(self, rotation_array):
		self.rotation = [
						self.rotation[0] + rotation_array[0],
						self.rotation[1] + rotation_array[1],
						self.rotation[2] + rotation_array[2]]

	def setScale(self, scale_array):
		self.scale = scale_array			

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
		for child in self.childs:
			child.update_transform()

		sg.drawSceneGraphNode(self.nodo, self.pipeline, "model")

	# solo actualiza las coordenadas para poder llamar un gameobject hijo sin volver a dibujarlo
	def update_transform(self):

			self.nodo.transform = tr.matmul([
				tr.translate(self.position[0], self.position[1], self.position[2]),
				tr.rotationX(self.rotation[0] * self.DEG_TO_RAD),
				tr.rotationY(self.rotation[1] * self.DEG_TO_RAD),
                tr.rotationZ(self.rotation[2] * self.DEG_TO_RAD),
                tr.scale(self.scale[0], self.scale[1], self.scale[2])
			])