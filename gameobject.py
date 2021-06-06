from OpenGL.GL import *
import lightHandler as lh
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
		self.drawType = "triangles"
		self.hasTexture = False
		self.nodo = sg.SceneGraphNode(nombre)
		self.nodo.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.1, 0.1, 0.1)])
		self.nodo.childs = []
	
	
	# le asocia un modelo al GameObject
	def setModel(self, modelo, hasTexture = False):
		self.nodo.childs = [modelo]
		if hasTexture == True:
			self.hasTexture = True

	# cambia el pipeline del GameObject
	def changePipeline(self, pipeline):
		self.pipeline = pipeline

	# cambia los pipelines desde este GameObject hacia abajo
	def changeTreesPipeline(self, pipeline, tex_pipeline):
		
		if self.hasTexture == False:
			self.pipeline = pipeline
		else:
			self.pipeline = tex_pipeline

		for child in self.childs:
			child.changeTreesPipeline(pipeline, tex_pipeline)			
				

	# añade nodos que van a ser dibujados siempre en su posicion inicial
	def nodeAddChilds(self, childList):
		# En particular, un GameObject con modelo no puede tener mas hijos
		if len(self.nodo.childs) > 0:
			assert not isinstance(self.nodo.childs[0], gs.GPUShape) , "Un GameObject con modelo no puede tener mas hijos"

		self.nodo.childs += childList

	# añade hijos que son GameObjects, sirve para poder hacer que los hijos se muevan mientras siguen conectados al padre
	def addChilds(self, childList):	
		
		if len(self.nodo.childs) > 0:
			assert not isinstance(self.nodo.childs[0], gs.GPUShape) , "Un GameObject con modelo no puede tener mas hijos"

		for child in childList:
			self.childs += [child]
			self.nodo.childs += [child.nodo]

	# determina el tipo de dibujo que se usara
	def setDrawType(self, newType):
		assert newType == "triangles" or newType == "lines"
		self.drawType = newType

	# especifica una nueva posicion del objeto
	def setPosition(self, position_array):
		self.position = position_array	

	# mueve el GameObject respecto a su posicion anterior
	def translate(self, position_array):
		self.position = [
						self.position[0] + position_array[0],
						self.position[1] + position_array[1],
						self.position[2] + position_array[2]]
    
    # especifica una nueva rotacion del objeto
	def setRotation(self, rotation_array):
		self.rotation = rotation_array

	# rota el GameObject respecto a su posicion anterior
	def rotate(self, rotation_array):
		self.rotation = [
						self.rotation[0] + rotation_array[0],
						self.rotation[1] + rotation_array[1],
						self.rotation[2] + rotation_array[2]]

	# especifica una nuevo tamaño variable en cada coordenada
	def setScale(self, scale_array):
		self.scale = scale_array

	# multiplica uniformemente el tamaño del objeto respecto a un ratio
	def uniformScale(self, ratio):
		self.scale = [
					 self.scale[0] * ratio,
					 self.scale[1] * ratio,
					 self.scale[2] * ratio]				

	# libera la memoria del objeto y de sus hijos
	def clear(self):
		self.nodo.clear()

	# update
	def update(self, deltaTime, camera, projection, viewMatrix):
		self.time += deltaTime

		self.update_transform()
		self.draw(self.pipeline, "model", camera, projection, viewMatrix)

	# solo actualiza las coordenadas para poder llamar un gameobject hijo sin volver a dibujarlo
	def update_transform(self):

		self.nodo.transform = tr.matmul([
			tr.translate(self.position[0], self.position[1], self.position[2]),

			# las rotaciones siempre van a ser en orden x,y,z
			tr.rotationX(self.rotation[0] * self.DEG_TO_RAD),
			tr.rotationY(self.rotation[1] * self.DEG_TO_RAD),
            tr.rotationZ(self.rotation[2] * self.DEG_TO_RAD),
            tr.scale(self.scale[0], self.scale[1], self.scale[2])
		])

		for child in self.childs:
			child.update_transform()

	# dibuja al GameObject y a sus hijos
	def draw(self, pipeline, transformName, camera, projection, viewMatrix, shininess = 100, att = 0.05, parentTransform=tr.identity()):
		node = self.nodo
		assert(isinstance(node, sg.SceneGraphNode))

		# Composing the transformations through this path
		newTransform = np.matmul(parentTransform, node.transform)

		# If the child node is a leaf, it should be a GPUShape.
		# Hence, it can be drawn with drawCall
		if len(node.childs) == 1 and isinstance(node.childs[0], gs.GPUShape):
		    leaf = node.childs[0]

		    lh.setShaderUniforms(pipeline, camera, projection, viewMatrix)
		    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, transformName), 1, GL_TRUE, newTransform)
		    glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), shininess)
		    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), att)

		    if self.drawType == "triangles":
		    	pipeline.drawCall(leaf)
		    	
		    if self.drawType == "lines":
		    	pipeline.drawCall(leaf,GL_LINES)	

		# If the child is not a leaf, it MUST be a GameObject,
		# so this draw function is called recursively
		else:
		    for child in self.childs:
		        child.draw(child.pipeline, transformName, camera, projection, viewMatrix, shininess,att, newTransform)

		
def findGameObject(nombre, gameobject):

    # Se encuentra el GameObject buscado
    if gameobject.nombre == nombre:
        return gameobject

    # El GameObject no esta en esta rama
    print(gameobject.nombre)
    if len(gameobject.childs) == 0:
    	return  
    
    # Se busca en todas las ramificaciones
    for child in gameobject.childs:
        foundGameObject = findGameObject(nombre, child)
        if foundGameObject != None:
            return foundGameObject