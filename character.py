import math
from gameobject import GameObject, findGameObject
from curves import *

class Character(GameObject):

	def __init__(self, pipeline, childs):
		super(Character, self).__init__("Character", pipeline)

		self.index = 0
		self.N = 600
		self.childs = childs

		# Se recuperan las partes del arbol que se quieran mover
		self.joint1 = findGameObject("joint1", self)
		self.joint2 = findGameObject("joint2", self)
		self.joint3 = findGameObject("joint3", self)
		self.joint4 = findGameObject("joint4", self)
		self.body = findGameObject("body", self)

		#Curvas que usa para bailar
		self.tailShakingCurve = evalMultiCatCurve( [[0, 10, 0], [0, 0, 0], [5, 15, 0], [15, -15, 0], [20, 0, 0], [20, -10, 0]], self.N)		

	def update(self, delta, camera):
		

		

		joint_1_rot = self.tailShakingCurve[math.floor(self.index) % self.N][1]
		joint_2_rot = self.tailShakingCurve[math.floor(self.index + self.N/3) % self.N][1]
		joint_3_rot = self.tailShakingCurve[math.floor(self.index + (2 * self.N)/3) % self.N][1]
		joint_4_rot = self.tailShakingCurve[math.floor(self.index) % self.N][1]

		self.joint1.setRotation([joint_1_rot, -90, 0])
		self.joint2.setRotation([joint_2_rot, 15, 0])
		self.joint3.setRotation([joint_3_rot, 15, 0])
		self.joint4.setRotation([joint_4_rot, 15, 0])
		self.body.setRotation([0, 0, joint_1_rot])

		GameObject.update(self, delta, camera)
		self.index += 1	