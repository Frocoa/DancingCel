from gameobject import GameObject, findGameObject

class Character(GameObject):

	def __init__(self, pipeline):
		super(Character, self).__init__("Character", pipeline)
		

	def update(self, deltaTime, camera, projection, viewMatrix):
		tail1 = findGameObject("joint1", self)
		tail1 = findGameObject("joint1", self)
		tail1 = findGameObject("joint1", self)
		tail1.rotate([0,0,self.time*deltaTime*200])

		GameObject.update(self, deltaTime, camera, projection, viewMatrix)	