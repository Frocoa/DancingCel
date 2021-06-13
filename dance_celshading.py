import glfw
import math
import OpenGL.GL.shaders
import grafica.performance_monitor as pm
import LightShaders as ls
import grafica.transformations as tr
import nodes as nd
from controller import Controller, on_key
from light import Light
from camera import Camera
from gameobject import GameObject
from shapes3d import *
from OpenGL.GL import *

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800
    title = "Cel Dance"

    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    controller = Controller()
    def on_key_wrapper(window, key, scancode, action, mods):
        on_key(controller, window, key, scancode, action, mods)

    # Connecting the callback function 'on_key_wrapper' to handle keyboard events
    glfw.set_key_callback(window, on_key_wrapper)

    # Pipeline con shaders con multiples fuentes de luz
    phongPipeline = ls.MultiplePhongShaderProgram()
    celPipeline = ls.MultipleCelShaderProgram()
    phongSpotPipeline = ls.MultiplePhongSpotShaderProgram()
    celSpotPipeline = ls.MultipleSpotCelShaderProgram()

    phongTexPipeline = ls.MultipleTexturePhongShaderProgram()
    celTexPipeline = ls.MultipleTextureCelShaderProgram()
    phongTexSpotPipeline = ls.MultipleTexturePhongSpotShaderProgram()
    celTexSpotPipeline = ls.MultipleTextureSpotCelShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    glLineWidth(10)

    camera = Camera(controller)
    camera.setProjection(tr.perspective(60, float(width) / float(height), 0.1, 100))

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    t0 = glfw.get_time()
    t_inicial = glfw.get_time()

    # Se instancian las luces que se van a utilizar
    lights = []

    light1Coords = [[0, 0, 0], [0, 0, 3], [0, 0, 3],    [2, 2, 4],   [2, 0, 4],    [0, 0, 3],     [0, 0, 0]]
    light1Colors = [[0, 0, 0], [100, 0, 0], [0.1, 0, 0], [-0.1, 0, 0], [-0.01, 0, 0], [0, 0, 0]]
    light1 = Light(light1Coords, light1Colors)
    lights.append(light1)
    light2Coords = [[0, 0, 0], [0, 0, 3], [0, 0, 3],[-2 , 2, 4], [-2 , 0, 4],   [0, 0, 3], [0, 0, 0]]
    light2Colors = [[0, 0, 0], [0, 100, 0], [0, 0.1, 0], [0, -0.1, 0], [0, -0.01, 0], [0, 0, 0]]
    light2 = Light(light2Coords, light2Colors)
    lights.append(light2)
    light3Coords = [[0, 0, 0], [0, 0, 3], [0, 0, 3],[0, -2, 4], [-2, -2, 4], [0, 0, 3], [0, 0, 0]]
    light3Colors = [[0, 0, 0], [0, 0, 100], [0, 0, 0.1], [0, 0, -0.1], [0, 0, -0.01], [0, 0, 0]]
    light3 = Light(light3Coords, light3Colors)
    lights.append(light3)

    light1.setPosition([2, 2, 3])
    light2.setPosition([-2, -2, 3])
    light3.setPosition([0, 0, 6]) 

    # Las pipelines que se dan aqui son solo las default, luego se pueden cambiar
    character = nd.createCharacter(celPipeline, celTexPipeline)
    scene = nd.createScene(celPipeline, celTexPipeline)

    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

        # Using GLFW to check for input events
        glfw.poll_events()

        #actualizar posicion de la camera y matriz de vista
        camera.update(delta)
        
        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Agregando el rendimiento
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Filling or not the shapes depending on the controller state
        if (controller.is_tab_pressed):
            character.changeTreesPipeline(phongSpotPipeline, phongTexSpotPipeline)
            scene.changeTreesPipeline(phongSpotPipeline, phongTexSpotPipeline)
        else:
            character.changeTreesPipeline(celSpotPipeline, celTexSpotPipeline)
            scene.changeTreesPipeline(celSpotPipeline, celTexSpotPipeline)

        ########          Luz         #######
        for light in lights:
            light.update(delta)

        ########          Dibujo          ########
        scene.update(delta, camera, lights)
        character.update(delta, camera, lights)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    scene.clear()
    character.clear()

    glfw.terminate()