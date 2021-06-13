""" Funciones para crear distintas figuras y escenas en 3D """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import LightShaders as ls
import grafica.gpu_shape as gs

def createGPUShape(pipeline, shape):
     # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = gs.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = gs.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = ls.textureSimpleSetup(
        path, GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)
    return gpuShape

def createTextureNormalPlane():  
    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions        texture   normales
        -0.5,  0.0, -0.5,  0, 1,   0,  1, 0,
         0.5,  0.0, -0.5,  1, 1,   0,  1, 0,
         0.5,  0.0,  0.5,  1, 0,   0,  1, 0,
        -0.5,  0.0,  0.5,  0, 0,   0,  1, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return bs.Shape(vertices, indices)

def createLegShape():
    # esta hecho para ser dibujado con lineas
    # va a tener una articulacion doble para que pueda 
    # doblar la rodilla utilizando dibujo dinamico (al final no lo hice)
    vertices = [
             0,     0,  0.5,  0, 0, 0,
             0,     0,  0.0,  0, 0, 0,
             0,     0, -0.5,  0, 0, 0,
        -0.177, 0.177,    0,  0, 0, 0]

    indices = [
            0, 1,
            1, 2,
            2, 3]     

    return bs.Shape(vertices, indices)

def createArmShape():
    # debe ser dibujado con lineas
    vertices = [
              0.0, -0.5, 0, 0, 0, 0,
              0.0,  0.5, 0, 0, 0, 0]

    indices = [0, 1]

    return bs.Shape(vertices, indices)                      