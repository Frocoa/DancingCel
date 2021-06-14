import math
from gameobject import GameObject, findGameObject

#Un plano con texturas que genera un falso efecto de 3d siguiendo siempre a la camara
class Plane3D(GameObject):

	def __init__(self, nombre, pipeline):
		super(Plane3D, self).__init__(nombre, pipeline)

		self.RAD_TO_DEG = 57.2958
		self.hasTexture = True # Por defecto deberia tener textura

	# update sin dibujar
	def update_transform(self, delta, camera):
		
		# Mirar siempre a camara
		angulo = 90 + math.atan((camera.eye[1] - self.position[1])/(camera.eye[0] - self.position[0]))* self.RAD_TO_DEG
		self.rotation = [self.rotation[0], self.rotation[1], angulo]

		GameObject.update_transform(self, delta, camera)



