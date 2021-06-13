import math
from gameobject import GameObject, findGameObject
from curves import *

class Character(GameObject):

	def __init__(self, pipeline, childs, controller):
		super(Character, self).__init__("Maru", pipeline)

		self.index = 0
		self.slowCount = 0
		self.N = 1200
		self.childs = childs
		self.controller = controller

		# Se recuperan las partes del arbol que se quieran mover
		self.joint1 = findGameObject("joint1", self)
		self.joint2 = findGameObject("joint2", self)
		self.joint3 = findGameObject("joint3", self)
		self.joint4 = findGameObject("joint4", self)
		self.body = findGameObject("body", self)
		self.legs = findGameObject("legs", self)
		self.leg1 = findGameObject("leg1joint", self)
		self.leg2 = findGameObject("leg2joint", self)
		self.larm = findGameObject("ljoint", self)
		self.rarm = findGameObject("rjoint", self)

		#Curvas que usa para bailar
		self.tailCurve = evalMultiCatCurve( [[0, 10, 0], [0, 0, 0], [0, 15, 0],[0, 0, 0], [0, -15, 0], [0, 0, 0], [0, 10, 0]], self.N)
		self.bodyCurve = evalMultiCatCurve([[0, 0, 0], [0, 0, 0], [2, 1.5, -0.2], [0, 1.5 , 0], [-1.5, 1.5, -0.2], [0, 1.5, 0],\
										    [1.5, 0, -0.2], [1.5, -1.5, 0], [0, -1.5, -0.2], [-1.5, -1.5, 0], [0, 0, 0], [0, 0, 0]], self.N)

		self.legsRot = evalMultiCatCurve([[0, 0, 0], [0, 0, 0], [0, 60, 0], [0, 0, 0], [0, -60, 0], [0, 0, 0], [0, 0, 0]], self.N)
		self.armsRot = evalMultiCatCurve([[0, 0, 0], [0, 0, 0], [0, 0, 30], [30, 0, 0],[0, 0, -30], [-30, 0, 0],[0, 0, 0],\
										 [50, 0, 0], [-50, 0, 0],[50, 0, 0], [-50, 0, 0], [50, 0, 0], [-50, 0, 0], [0, 0, 0], [0, 0, 0]], self.N)									    		

	def update(self, delta, camera, lights):
		
		if self.controller.slow == False or self.slowCount == 25:
			joint_1_rot = self.tailCurve[math.floor(self.index*10) % self.N][1]
			joint_2_rot = self.tailCurve[math.floor(self.index*10 + self.N/3) % self.N][1]
			joint_3_rot = self.tailCurve[math.floor(self.index*10 + (2 * self.N)/3) % self.N][1]
			joint_4_rot = self.tailCurve[math.floor(self.index*10) % self.N][1]

			bodyX = self.bodyCurve[math.floor(self.index) % self.N-6][0]
			bodyY = self.bodyCurve[math.floor(self.index) % self.N-6][1]
			bodyZ = self.bodyCurve[math.floor(self.index) % self.N-6][2]

			leg1Rot = self.legsRot[math.floor(self.index*8) % self.N][1]
			leg2Rot = self.legsRot[math.floor((self.index + 60)*8) % self.N][1]

			armsRotX = self.armsRot[math.floor(self.index*2) % self.N][0]
			armsRotZ = self.armsRot[math.floor(self.index*2) % self.N][2]

			self.joint1.setRotation([joint_1_rot, -90 + joint_1_rot*1.5, 0])
			self.joint2.setRotation([joint_2_rot, 15 - joint_2_rot, 0])
			self.joint3.setRotation([joint_3_rot, 15 + joint_3_rot*2, 0])
			self.joint4.setRotation([joint_4_rot, 15, 0])

			self.body.setRotation([0, 0, joint_1_rot/2])
			self.body.setPosition([0, 0, bodyZ])

			self.setPosition([bodyX, bodyY, -1])
			# Quiero que las piernas se muevan junto al cuerpo pero solo en x,y
			self.leg1.setRotation([0, leg1Rot, 0])
			self.leg2.setRotation([0, leg2Rot, 0])

			#Brazos
			self.larm.setRotation([armsRotX, 0, armsRotZ])
			self.rarm.setRotation([-armsRotX, 0, armsRotZ])

			
		GameObject.update(self, delta, camera, lights)
		self.slowCount = (self.slowCount + 1) % 26
		self.index += self.N/10 * delta	