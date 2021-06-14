""" Funciones para crear distintas figuras y escenas en 3D """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import LightShaders as ls
import curves as cv
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

# Aqui se usa Hermite y Bezier    
def createMoon():
    P0 = [0.5, 0, 0]
    P1 = [-0.5, 0, 0]
    P2 = [-0.5, 0, 1]
    P3 = [0.5, 0, 1]
    P4 = [0.5, 0, 0]
    P5 = [0.5, 0, 1]
    T1 = [-0.3, 0, 0]
    T2 = [1.3, 0, 1]
    Bezier = cv.bezierMatrix(P0, P1, P2, P3)
    Hermite = cv.hermiteMatrix(P4, P5, T1, T2)

    bCurve = cv.evalCurve(Bezier, 50)
    hCurve = cv.evalCurve(Hermite, 50)

    vertices = []
    indices = []
    counter = 0

    for i in range(len(bCurve)-1):
        cb1 = bCurve[i]
        cb2 = bCurve[i+1]
        ch1 = hCurve[i]
        ch2 = hCurve[i+1]

        vertices += [cb1[0], 0, cb1[2], 240/255, 196/255, 32/255]
        vertices += [ch1[0], 0, ch1[2], 240/255, 196/255, 32/255]
        vertices += [cb2[0], 0, cb2[2], 240/255, 196/255, 32/255]
        vertices += [ch1[0], 0, ch1[2], 240/255, 196/255, 32/255]
        vertices += [cb2[0], 0, cb2[2], 240/255, 196/255, 32/255]
        vertices += [ch2[0], 0, ch2[2], 240/255, 196/255, 32/255]

        indices += [
                    0+counter, 1+counter, 2+counter,
                    3+counter, 4+counter, 5+counter]
        counter += 6     

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