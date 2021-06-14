import curves as cv
import math

class Light():

	def __init__(self, controller, pos_curve_coords = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], color_curve_coords = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]):

		self.position = [0, 0, 0] # posicion de la luz
		self.Ld = [0.3, 0.3, 0.3] # componente difusa
		self.Ls = [0.5, 0.5, 0.5] # componente especular
		self.N =  600 # cantidad de puntos en las curvas
		self.slowCount = 0 # control del efecto de slow motion
		self.controller = controller # controlador
		self.pos_curve = cv.evalMultiCatCurve(pos_curve_coords, self.N) # curva con las posiciones de la luz
		self.color_curve = cv.evalMultiCatCurve(color_curve_coords, self.N) # curva que controla el color de la luz
		self.index = 1 # indice para las curvas

	# define una nueva posicion de la luz
	def setPosition(self, position_array):
		self.position = position_array

	# define una nueva componente ambiental de la luz
	def setLa(self, new_La):
		self.La = new_La

	# define una nueva componente difusa de la luz
	def setLd(self, new_Ld):
		self.Ld = new_Ld

	# define una nueva componente especular de la luz
	def setLs(self, new_Ls):
		self.Ls = new_Ls

	# le añade color a las componentes difusa y ambiental
	def addColor(self, color):
		self.setLd ([self.Ld[0] + color[0]/2, self.Ld[1] + color[1]/2, self.Ld[2] + color[2]/2])
		self.setLs ([self.Ls[0] + color[0], self.Ls[1] + color[1], self.Ls[2] + color[2]])

	# update
	def update(self, delta):
		if self.controller.slow == False or self.slowCount == 25:
			position = [0, 0, 0]
			position[0] = self.pos_curve[math.floor(self.index) % self.N][0]
			position[1] = self.pos_curve[math.floor(self.index) % self.N][1]
			position[2] = self.pos_curve[math.floor(self.index) % self.N][2]
			self.setPosition(position)
		self.slowCount = (self.slowCount + 1)%26

		color = [0, 0, 0]
		color[0] = self.color_curve[math.floor(self.index) % self.N][0]
		color[1] = self.color_curve[math.floor(self.index) % self.N][1]
		color[2] = self.color_curve[math.floor(self.index) % self.N][2]
		self.addColor(color)
		self.index += 1

