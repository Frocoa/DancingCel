import math
from gameobject import GameObject, findGameObject
from curves import *

class Character(GameObject):

	def __init__(self, pipeline):
		super(Character, self).__init__("Character", pipeline)

		self.index = 0
		self.N = 120
		

	def update(self, deltaTime, camera, projection, viewMatrix):
		joint1 = findGameObject("joint1", self)
		joint2 = findGameObject("joint2", self)
		joint3 = findGameObject("joint3", self)
		joint4 = findGameObject("joint4", self)
		body = findGameObject("body", self)

		tailShakingCurve = evalTripleCurve( [0, 10, 0], [0, 0, 0], [5, 15, 0], [15, -15, 0], [20, 0, 0], [20, -10, 0], self.N)

		joint_1_rot = tailShakingCurve[math.floor(self.index)%self.N][1]
		joint_2_rot = tailShakingCurve[math.floor(self.index + self.N/3)%self.N][1]
		joint_3_rot = tailShakingCurve[math.floor(self.index + (2*self.N)/3)%self.N][1]
		joint_4_rot = tailShakingCurve[math.floor(self.index)%self.N][1]

		joint1.setRotation([joint_1_rot, -90, 0])
		joint2.setRotation([joint_2_rot, 15, 0])
		joint3.setRotation([joint_3_rot, 15, 0])
		joint4.setRotation([joint_4_rot, 15, 0])
		body.setRotation([0, 0, joint_1_rot])

		GameObject.update(self, deltaTime, camera, projection, viewMatrix)
		self.index += 1	