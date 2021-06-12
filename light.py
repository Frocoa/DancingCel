class Light():

	def __init__(self, pos_curve_coords, color_curve_coords):

		self.position = [0, 0, 0]
		self.La = [0.25, 0.25, 0.25]
		self.Ld = [0.5, 0.5, 0.5]
		self.Ls = [0.8, 0.8, 0.8]
		self.pos_curve = pos_curve_coords
		self.color_curve = color_curve_coords
		self.N =  600
		self.index

	def setPosition(self, position_array):
		self.position = position_array

	def setLa(self, new_La):
		self.La = new_La

	def setLa(self, new_Ld):
		self.Ld = new_Ld

	def setLs(self, new_Ls):
		self.Ls = new_Ls

	def addColor(self, color):
		self.setLa = [self.La[0] + color[0]/4, self.La[1] + color[1]/4, self.La[2] + color[2]/4]
		self.setLd = [self.Ld[0] + color[0]/2, self.Ld[1] + color[1]/2, self.Ld[2] + color[2]/2]
		self.setLs = [self.Ls[0] + color[0], self.Ls[1] + color[1], self.Ls[2] + color[2]]

	def update(self, delta):
		position[0] = self.pos_curve[math.floor(self.index) % self.N][0]
		position[1] = self.pos_curve[math.floor(self.index) % self.N][1]
		position[2] = self.pos_curve[math.floor(self.index) % self.N][2]
		self.setPosition(position)

		color[0] = self.color_curve[math.floor(self.index) % self.N][0]
		color[1] = self.color_curve[math.floor(self.index) % self.N][1]
		color[2] = self.color_curve[math.floor(self.index) % self.N][2]

		self.index += 1

