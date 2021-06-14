from OpenGL.GL import *
import uniformhandler as uh
import grafica.transformations as tr
import grafica.gpu_shape as gs
import numpy as np

class GameObject:

	def __init__(self, nombre, pipeline):
		self.DEG_TO_RAD = 0.0174533

		self.nombre = nombre # nombre del objeto por el cual puede ser buscado
		self.position = [0, 0, 0] # posicion del objeto (x, y, z)
		self.rotation = [0, 0, 0] # rotacion en grados
		self.scale = [1, 1, 1] # tamaño del objeto
		self.childs = [] # gameobjects
		self.time = 0 # tiempo

		self.pipeline = pipeline # pipeline con la cual se dibuja
		self.drawType = "triangles" # metodo de dibujo 
		self.hasTexture = False # determina si el objeto usa texturas o solo geometria
		self.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.1, 0.1, 0.1)]) # transformacion

		#Material
		self.Ka = (0.3, 0.3, 0.3) # componente ambiental
		self.Kd = (0.5, 0.5, 0.5) # componente difusa
		self.Ks = (0.1, 0.1, 0.1) # componente especular
		self.shininess = 50       # (int) brillo 


	
	# cambia el pipeline
	def changePipeline(self, pipeline):
		self.pipeline = pipeline

	# cambia los pipelines de este GameObject y todos sus hijos
	def changeTreesPipeline(self, pipeline, tex_pipeline):
		
		if self.hasTexture == False:
			self.pipeline = pipeline
		else:
			self.pipeline = tex_pipeline

		for child in self.childs:
			if not isinstance(child, gs.GPUShape):
				child.changeTreesPipeline(pipeline, tex_pipeline)			
	
	# define el material del objeto
	def setMaterial(self, Ka, Kd, Ks, shininess):
		self.Ka = Ka
		self.Kd = Kd
		self.Ks = Ks
		self.shininess = shininess

	# Le pone el mismo material al objeto y a todos sus hijos
	def setTreesMaterial(self, Ka, Kd, Ks, shininess):
		self.setMaterial(Ka, Kd, Ks, shininess)

		for child in self.childs:
			if not isinstance(child, gs.GPUShape):
				child.setTreesMaterial(Ka, Kd, Ks, shininess)

	# le asocia un modelo al GameObject
	def setModel(self, modelo, hasTexture = False):
		self.childs = [modelo]
		if hasTexture == True:
			self.hasTexture = True
	
	# añade hijos que son GameObjects, sirve para poder hacer que los hijos se muevan mientras siguen conectados al padre
	def addChilds(self, childList):	
		
		if len(self.childs) > 0:
			assert not isinstance(self.childs[0], gs.GPUShape) , "Un GameObject con modelo no puede tener mas hijos"

		for child in childList:
			self.childs += [child]
    

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
		for child in self.childs:
			# aprovecho que GPUShape tiene un metodo clear
			child.clear()

	# update
	def update(self, delta, camera, lights):
		self.time += delta

		self.update_transform(delta, camera)
		self.draw(self.pipeline, "model", camera, lights)

	# solo actualiza las coordenadas para poder llamar un gameobject hijo sin volver a dibujarlo
	def update_transform(self, delta, camera):

		self.transform = tr.matmul([
			tr.translate(self.position[0], self.position[1], self.position[2]),

			# las rotaciones siempre van a ser en orden x,y,z
			tr.rotationX(self.rotation[0] * self.DEG_TO_RAD),
			tr.rotationY(self.rotation[1] * self.DEG_TO_RAD),
            tr.rotationZ(self.rotation[2] * self.DEG_TO_RAD),
            tr.scale(self.scale[0], self.scale[1], self.scale[2])
		])

		for child in self.childs:
			if not isinstance(child, gs.GPUShape):
				child.update_transform(delta, camera)

	# dibuja al GameObject y a sus hijos
	def draw(self, pipeline, transformName, camera, lights, parentTransform=tr.identity()):

		# Composing the transformations through this path
		newTransform = np.matmul(parentTransform, self.transform)

		# If the child is a leaf, it should be a GPUShape.
		# Hence, it can be drawn with drawCall
		if len(self.childs) == 1 and isinstance(self.childs[0], gs.GPUShape):
		    leaf = self.childs[0]

		    uh.setLightUniforms(pipeline, lights)
		    uh.setMaterialUniforms(pipeline, self.Ka, self.Kd, self.Ks, self.shininess)
		    uh.setCameraUniforms(pipeline, camera, camera.projection, camera.viewMatrix )
		    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, transformName), 1, GL_TRUE, newTransform)
		    

		    if self.drawType == "triangles":
		    	pipeline.drawCall(leaf)
		    	
		    if self.drawType == "lines":
		    	pipeline.drawCall(leaf,GL_LINES)	

		# If the child is not a leaf, it MUST be a GameObject,
		# so this draw function is called recursively
		else:
		    for child in self.childs:
		        child.draw(child.pipeline, transformName, camera, lights, newTransform)


		
def findGameObject(nombre, gameobject):
	# El objeto no se encontro
    if isinstance(gameobject, gs.GPUShape):
        return None

    # Se encuentra el GameObject buscado
    if gameobject.nombre == nombre:
        return gameobject

    # El GameObject no esta en esta rama
    if len(gameobject.childs) == 0:
    	return  
    
    # Se busca en todas las ramificaciones
    for child in gameobject.childs:
        foundGameObject = findGameObject(nombre, child)
        if foundGameObject != None:
            return foundGameObject