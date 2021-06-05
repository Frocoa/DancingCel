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
		self.scale = (1, 1, 1)
		self.time = 0

		self.pipeline = pipeline
		self.nodo = sg.SceneGraphNode(nombre)
		self.nodo.transform = tr.matmul([tr.translate(0,0,0), tr.scale(0.1,0.1,0.1)])
		self.nodo.childs = []
	
	
	def setModel(self, modelo):
		self.nodo.childs = [modelo]

	def addChilds(self, childList):
		# En particular, un GameObject con modelo no puede tener mas hijos
		if len(self.nodo.childs) > 0:
			assert not isinstance(self.nodo.childs[0], gs.GPUShape) , "Un GameObject con modelo no puede tener mas hijos"

		self.nodo.childs += childList

	def setPosition(self, position_vector):
		self.position = position_array

	def translate(self, position_vector):
		self.position = [
						self.position[0] + position_vector[0],
						self.position[1] + position_vector[1],
						self.position[2] + position_vector[2]]

	def setRotation(rotation_vector):
		self.rotation = rotation_vector

	def rotate(self, rotation_vector):
		self.rotation = [
						self.rotation[0] + rotation_vector[0],
						self.rotation[1] + rotation_vector[1],
						self.rotation[2] + rotation_vector[2]]

	def setScale(self, scale_vector):
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