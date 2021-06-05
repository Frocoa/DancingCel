import glfw
import OpenGL.GL.shaders
import numpy as np
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.performance_monitor as pm
import grafica.lighting_shaders as ls
import newLightShaders as nl
import lightHandler as lh
from controller import Controller, on_key
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
    phongPipeline = nl.MultiplePhongShaderProgram()
    phongSpotPipeline = nl.MultiplePhongSpotShaderProgram()
    phongTexPipeline = nl.MultipleTexturePhongShaderProgram()

    # This shader program does not consider lighting
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    camera = Camera(controller)

    scene = GameObject("escena", phongPipeline)
    scene.addChilds(sceneChilds(phongPipeline))

    tex_toro = GameObject("tex toro", phongTexPipeline)
    tex_toro.setModel(createTextureGPUShape(createTextureNormalToroide(20), phongTexPipeline, "assets/barras.png"))
    plane1 = GameObject("planito", phongTexPipeline)
    plane1.setModel(createTextureGPUShape(createTextureNormalPlane(), phongTexPipeline, "assets/barras.png"))
      
    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    t0 = glfw.get_time()
    t_inicial = glfw.get_time()

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
        viewMatrix = camera.update_view()

        # Setting up the projection transform
        projection = tr.perspective(60, float(width) / float(height), 0.1, 100)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Agregando el rendimiento
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        lightingPipeline = phongPipeline
        #lightingPipeline = phongSpotPipeline

        # se envian los uniforms asociados a la iluminacion
        lh.setShaderUniforms(lightingPipeline, camera, projection, viewMatrix)
        scene.update(delta)

        # se envian los uniforms asociados a la iluminacion con texturas
        lh.setShaderUniforms(phongTexPipeline, camera, projection, viewMatrix)
        plane1.update(delta)
        tex_toro.update(delta)
        
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    scene.clear()
    toro1.clear()
    tex_toro.clear()
    plane1.clear()

    glfw.terminate()