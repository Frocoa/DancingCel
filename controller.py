import glfw
from camera import Camera

# Clase controlador con variables para manejar el estado de ciertos botones
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True

        # Variables para controlar la camara
        self.is_up_pressed = False
        self.is_down_pressed = False
        self.is_left_pressed = False
        self.is_right_pressed = False
        self.is_tab_pressed = False
        self.manual = True
        self.slow = False
        self.is_3_pressed = False

# Metodo para leer el input del teclado
def on_key(self, window, key, scancode, action, mods):

    # Caso de detectar la tecla [UP], actualiza estado de variable
    if key == glfw.KEY_UP:
        if action == glfw.PRESS:
            self.is_up_pressed = True
        elif action == glfw.RELEASE:
            self.is_up_pressed = False

    # Caso de detectar la tecla [DOWN], actualiza estado de variable
    if key == glfw.KEY_DOWN:
        if action == glfw.PRESS:
            self.is_down_pressed = True
        elif action == glfw.RELEASE:
            self.is_down_pressed = False

    # Caso de detectar la tecla [RIGHT], actualiza estado de variable
    if key == glfw.KEY_RIGHT:
        if action == glfw.PRESS:
            self.is_right_pressed = True
        elif action == glfw.RELEASE:
            self.is_right_pressed = False

    # Caso de detectar la tecla [LEFT], actualiza estado de variable
    if key == glfw.KEY_LEFT:
        if action == glfw.PRESS:
            self.is_left_pressed = True
        elif action == glfw.RELEASE:
            self.is_left_pressed = False
    
    # Caso de detectar la barra espaciadora, se cambia el metodo de dibujo
    if key == glfw.KEY_SPACE:
        if action == glfw.PRESS:
            self.fillPolygon = not self.fillPolygon

    # Caso de detectar el tab se cambian los pipelines
    if key == glfw.KEY_TAB:
        if action == glfw.PRESS:
            self.is_tab_pressed = not self.is_tab_pressed

    # Caso de detectar el numero 1
    if key == glfw.KEY_1:
        if action == glfw.PRESS:
            self.slow = not self.slow  

    # Caso de detectar el numero 2
    if key == glfw.KEY_2:
        if action == glfw.PRESS:
            self.manual = not self.manual

    # Caso de detectar el numero 3
    if key == glfw.KEY_3:
        if action == glfw.PRESS:
            self.is_3_pressed = not self.is_3_pressed                

    # Caso en que se cierra la ventana
    if key == glfw.KEY_ESCAPE:
        if action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

