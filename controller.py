import glfw
from camera import Camera

# Clase controlador con variables para manejar el estado de ciertos botones
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True

        # Variables para controlar la camara
        self.is_w_pressed = False
        self.is_s_pressed = False
        self.is_a_pressed = False
        self.is_d_pressed = False

# Metodo para leer el input del teclado
def on_key(self, window, key, scancode, action, mods):

    # Caso de detectar la tecla [UP], actualiza estado de variable
    if key == glfw.KEY_UP:
        if action == glfw.PRESS:
            self.is_w_pressed = True
        elif action == glfw.RELEASE:
            self.is_w_pressed = False

    # Caso de detectar la tecla [DOWN], actualiza estado de variable
    if key == glfw.KEY_DOWN:
        if action == glfw.PRESS:
            self.is_s_pressed = True
        elif action == glfw.RELEASE:
            self.is_s_pressed = False

    # Caso de detectar la tecla [RIGHT], actualiza estado de variable
    if key == glfw.KEY_RIGHT:
        if action == glfw.PRESS:
            self.is_d_pressed = True
        elif action == glfw.RELEASE:
            self.is_d_pressed = False

    # Caso de detectar la tecla [LEFT], actualiza estado de variable
    if key == glfw.KEY_LEFT:
        if action == glfw.PRESS:
            self.is_a_pressed = True
        elif action == glfw.RELEASE:
            self.is_a_pressed = False
    
    # Caso de detectar la barra espaciadora, se cambia el metodo de dibujo
    if key == glfw.KEY_SPACE:
        if action == glfw.PRESS:
            self.fillPolygon = not self.fillPolygon

    # Caso en que se cierra la ventana
    if key == glfw.KEY_ESCAPE:
        if action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    # Caso de detectar Control izquierdo, se cambia el metodo de dibujo
    elif key == glfw.KEY_LEFT_CONTROL:
        if action == glfw.PRESS:
            self.showAxis = not self.showAxis
