import math
from gameobject import GameObject, findGameObject

#Un plano con texturas que genera un falso efecto de 3d
class Plane3D(GameObject):

	def __init__(self, nombre, pipeline):
		super(Plane3D, self).__init__(nombre, pipeline)

		self.RAD_TO_DEG = 57.2958
		self.hasTexture = True

	def update_transform(self, delta, camera):
		
		angulo = 90 + math.atan((camera.eye[1] - self.position[1])/(camera.eye[0] - self.position[0]))* self.RAD_TO_DEG
		self.rotation = [self.rotation[0], self.rotation[1], angulo]

		GameObject.update_transform(self, delta, camera)



