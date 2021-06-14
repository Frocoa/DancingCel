import numpy as np
import grafica.transformations as tr
import curves as cv
import math

# Clase para manejar una camara que se mueve en coordenadas polares
class Camera:
    
    def __init__(self, controller):
        self.controller = controller
        self.at = np.array([0.0, 0.0, -0.5])     # donde mira la camara
        self.eye = np.array([0.0, 0.0, 0.0])     # posicion de la camara
        self.up = np.array([0, 0, 1])            # vector up
        self.viewMatrix = None                   # Matriz de vista
        self.projection = None                   # Matriz de proyeccion
        self.N = 1200                            # Cantidad de puntos en las curvas
        self.index = 1                           # Posicion de las curvas en las que se encuentra la camara
        self.objective = None                    # A que objeto mantiene siempre en la mira

        #Trayectorias que puede tomar la cámara
        #se calculan en el constructor para que se haga solo una vez
        self.autoCurve = cv.evalMultiCatCurve([[0, 0, 4], [10, 0, 4],[3,0,-0.5], [0.0, 7.0, 4], [-10.0, 0, 4], [-4, 0, -0.5], [0.0, -7.0, 4], [10, 0, 4],\
                                                 [0, 0, 4]], self.N)

        self.manualCurve = cv.evalMultiCatCurve([[5, 5, 1], [5, 5, 3], [0, 5, 3], [-5, 5, 1], [-5, 0, 3], [-5, -5, 6], [0, -5, 3], [5, -5, 3], [5, 0, 1],\
                                                 [5, 5, 3],[5, 5, 1]], self.N)
    
    # Añadir la matriz de proyeccion
    def setProjection(self, projection):
        self.projection = projection

    def setObjective(self, GameObject):
        self.objective = GameObject

    def setAt(self, at):
        self.at = at    

    # Actualizar la matriz de vista
    def update_view(self, delta):

        # Se calcula la posición de la camara
        if self.controller.manual == True:
            self.eye[0] = self.manualCurve[math.floor(self.index*2) % self.N][0]
            self.eye[1] = self.manualCurve[math.floor(self.index*2) % self.N][1]
            self.eye[2] = self.manualCurve[math.floor(self.index*2) % self.N][2]

        else:
            self.eye[0] = self.autoCurve[math.floor(self.index*1.5) % self.N][0]
            self.eye[1] = self.autoCurve[math.floor(self.index*1.5) % self.N][1]
            self.eye[2] = self.autoCurve[math.floor(self.index*1.5) % self.N][2]
            self.index += self.N/10 * delta 

        
        # Se genera la matriz de vista
        viewMatrix = tr.lookAt(
            self.eye,
            self.at,
            self.up
        )

        self.viewMatrix = viewMatrix

    #Funcion que recibe el input para manejar la camara y controlar sus coordenadas
    def update(self, delta):
        if self.controller.manual == True:
            # Camara se mueve a la derecha  
            if self.controller.is_left_pressed:
                self.index -= self.N/10 * delta

            # Camara se mueve a la izquierda
            if self.controller.is_right_pressed:
                self.index += self.N/10 * delta

        self.update_view(delta)    