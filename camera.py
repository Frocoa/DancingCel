import numpy as np
import grafica.transformations as tr
import curves as cv
import math

# Clase para manejar una camara que se mueve en coordenadas polares
class Camera:
    def __init__(self, controller):
        self.controller = controller
        self.center = np.array([0.0, 0.0, -0.5]) # centro de movimiento de la camara y donde mira la camara
        self.theta = 0                           # coordenada theta, angulo de la camara
        self.rho = 5                             # coordenada rho, distancia al centro de la camara
        self.eye = np.array([0.0, 0.0, 0.0])     # posicion de la camara
        self.height = 0.5                        # altura fija de la camara
        self.up = np.array([0, 0, 1])            # vector up
        self.viewMatrix = None                   # Matriz de vista
        self.projection = None                   # Matriz de proyeccion
        self.N = 240
        self.index = 1
    
    # Añadir la matriz de proyeccion
    def setProjection(self, projection):
        self.projection = projection


    # Añadir ángulo a la coordenada theta
    def set_theta(self, delta):
        self.theta = (self.theta + delta) % (np.pi * 2)

    # Añadir distancia a la coordenada rho, sin dejar que sea menor o igual a 0
    def set_rho(self, delta):
        if ((self.rho + delta) > 0.1):
            self.rho += delta

    # Actualizar la matriz de vista
    def update_view(self, delta):
        """# Se calcula la posición de la camara con coordenadas poleras relativas al centro
        self.eye[0] = self.rho * np.sin(self.theta) + self.center[0]
        self.eye[1] = self.rho * np.cos(self.theta) + self.center[1]
        self.eye[2] = self.height + self.center[2]"""

        curve = cv.evalMultiCatCurve( [[0, 0, 10], [5, 0, 10], [0.0, 5.0, 10], [-5.0, 0, 10], [0.0, -5.0, 10], [5, 0, 10], [0, 0, 10]], self.N)
        self.eye[0] = curve[math.floor(self.index) % self.N][0]
        self.eye[1] = curve[math.floor(self.index) % self.N][1]
        self.eye[2] = curve[math.floor(self.index) % self.N][2]
        # Se genera la matriz de vista
        viewMatrix = tr.lookAt(
            self.eye,
            self.center,
            self.up
        )
        self.viewMatrix = viewMatrix
        self.index += 60*delta 
        print(self.index)

    #Funcion que recibe el input para manejar la camara y controlar sus coordenadas
    def update(self, delta):

        # Camara rota a la izquierda
        if self.controller.is_left_pressed:
            self.set_theta(-2 * delta)

        # Camara rota a la derecha
        if self.controller.is_right_pressed:
            self.set_theta( 2 * delta)
        
        # Camara se acerca al centro
        if self.controller.is_up_pressed:
            self.set_rho(-5 * delta)

        # Camara se aleja del centro
        if self.controller.is_down_pressed:
            self.set_rho(5 * delta)

        self.update_view(delta)    