""" Funciones para crear distintas figuras y escenas en 3D """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.scene_graph as sg
import newLightShaders as nl

def createGPUShape(pipeline, shape):
     # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape


def sceneChilds(pipeline):
    # Se crea la escena base

    # Se crean las shapes en GPU
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(1.0,0.7,0.7)) # Shape del cubo gris

    # Nodo del cubo gris
    grayCubeNode = sg.SceneGraphNode("grayCube")
    grayCubeNode.childs = [gpuGrayCube]

    # Nodo del suelo de color gris
    floorNode = sg.SceneGraphNode("floor")
    floorNode.transform = tr.translate(0, 0, -1)
    floorNode.childs = [grayCubeNode]

    # Nodo de la escena para realizar un escalamiento
    sceneNode = sg.SceneGraphNode("scene")
    sceneNode.transform = tr.matmul([tr.translate(0, 0, -1.5), tr.scale(5, 5, 1)])
    sceneNode.childs = [floorNode]

    # Nodo final de la escena 
    trSceneNode = sg.SceneGraphNode("tr_scene")
    trSceneNode.childs = [sceneNode]

    return trSceneNode.childs

def createCube1(pipeline):
    # Funcion para crear Grafo de un objeto de la escena, se separa en otro grafo, por si se quiere dibujar con otro material
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(0.5, 0.5, 0.5)) # Shape del cubo gris

    # Nodo del cubo gris
    grayCubeNode = sg.SceneGraphNode("grayCube")
    grayCubeNode.childs = [gpuGrayCube]

    # Nodo del cubo escalado 
    objectNode = sg.SceneGraphNode("object1")
    objectNode.transform = tr.matmul([
        tr.translate(0.25,-0.15,-0.25),
        tr.rotationZ(np.pi*0.15),
        tr.scale(0.2,0.2,0.5)
    ])
    objectNode.childs = [grayCubeNode]

    # Nodo del del objeto escalado con el mismo valor de la escena base
    scaledObject = sg.SceneGraphNode("object1")
    scaledObject.transform = tr.scale(5, 5, 5)
    scaledObject.childs = [objectNode]

    return scaledObject

def createCube2(pipeline):
    # Funcion para crear Grafo de un objeto de la escena, se separa en otro grafo, por si se quiere dibujar con otro material
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(0.5, 0.5, 0.5)) # Shape del cubo gris

    # Nodo del cubo gris
    grayCubeNode = sg.SceneGraphNode("grayCube")
    grayCubeNode.childs = [gpuGrayCube]

    # Nodo del cubo escalado 
    objectNode = sg.SceneGraphNode("object1")
    objectNode.transform = tr.matmul([
        tr.translate(-0.25,-0.15,-0.35),
        tr.rotationZ(np.pi*-0.2),
        tr.scale(0.3,0.3,0.3)
    ])
    objectNode.childs = [grayCubeNode]

    # Nodo del del objeto escalado con el mismo valor de la escena base
    scaledObject = sg.SceneGraphNode("object1")
    scaledObject.transform = tr.scale(5, 5, 5)
    scaledObject.childs = [objectNode]

    return scaledObject

def createColorNormalToro(N, r, g, b):
    # Funcion para crear un toroide con normales

    vertices = []           # lista para almacenar los verices
    indices = []            # lista para almacenar los indices
    dTheta = 2 * np.pi /N   # angulo que hay entre cada iteracion de la coordenada theta
    dPhi = 2 * np.pi /N     # angulo que hay entre cada iteracion de la coordenada phi
    rho = 0.2
    R = 0.5               # radio de el toroide
    c = 0                   # contador de vertices, para ayudar a indicar los indices

    # Se recorre la coordenada theta
    for i in range(N):
        theta = i * dTheta # angulo theta en esta iteracion
        theta1 = (i + 1) * dTheta # angulo theta en la iteracion siguiente
        # Se recorre la coordenada phi
        for j in range(N):
            phi = j*dPhi # angulo phi en esta iteracion
            phi1 = (j+1)*dPhi # angulo phi en la iteracion siguiente

            # Se crean los vertices necesarios son coordenadas esfericas para cada iteracion

            # Vertice para las iteraciones actuales de theta (i) y phi (j) 
            v0 = [np.cos(theta)*(R+rho*np.cos(phi)),np.sin(theta)*(R+rho*np.cos(phi)), rho*np.sin(phi)]
            # Vertice para las iteraciones siguiente de theta (i + 1) y actual de phi (j) 
            v1 = [np.cos(theta1)*(R+rho*np.cos(phi)),np.sin(theta1)*(R+rho*np.cos(phi)), rho*np.sin(phi)]
            # Vertice para las iteraciones actual de theta (i) y siguiente de phi (j + 1) 
            v2 = [np.cos(theta1)*(R+rho*np.cos(phi1)),np.sin(theta1)*(R+rho*np.cos(phi1)), rho*np.sin(phi1)]
            # Vertice para las iteraciones siguientes de theta (i + 1) y phi (j + 1) 
            v3 = [np.cos(theta)*(R+rho*np.cos(phi1)),np.sin(theta)*(R+rho*np.cos(phi1)), rho*np.sin(phi1)]
            
            # Se crean los vectores normales para cada vertice segun los valores de rho tongo 
            n0 = [np.cos(theta)*np.cos(phi), np.sin(theta)*np.cos(phi), np.sin(phi)]
            n1 = [np.cos(theta1)*np.cos(phi), np.sin(theta1)*np.cos(phi), np.sin(phi)]
            n2 = [np.cos(theta1)*np.cos(phi1), np.sin(theta1)*np.cos(phi1), np.sin(phi1)]
            n3 = [np.cos(theta)*np.cos(phi1), np.sin(theta)*np.cos(phi1), np.sin(phi1)]
            
            # Creamos los quads intermedios
            #  v0 -------------- v3
            #  | \                |
            #  |    \             |
            #  |       \          |
            #  |          \       |
            #  |             \    |
            #  |                \ |
            #  v1 -------------- v2
            
            #           vertices              color    normales
            vertices += [v0[0], v0[1], v0[2], r, g, b, n0[0], n0[1], n0[2]]
            vertices += [v1[0], v1[1], v1[2], r, g, b, n1[0], n1[1], n1[2]]
            vertices += [v2[0], v2[1], v2[2], r, g, b, n2[0], n2[1], n2[2]]
            vertices += [v3[0], v3[1], v3[2], r, g, b, n3[0], n3[1], n3[2]]
            indices += [ c + 0, c + 1, c +2 ]
            indices += [ c + 2, c + 3, c + 0 ]
            c += 4
    return bs.Shape(vertices, indices)

def createTextureNormalPlane():  
    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions        texture   normales
        -0.5,  0.0, -0.5,  0, 1,   0, -1, 0,
         0.5,  0.0, -0.5,  1, 1,   0, -1, 0,
         0.5,  0.0,  0.5,  1, 0,   0, -1, 0,
        -0.5,  0.0,  0.5,  0, 0,   0, -1, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return bs.Shape(vertices, indices)

def createTexPlaneNode(pipeline):
    plane = createTextureGPUShape(createTextureNormalPlane(), pipeline, "assets/barras.png")

    # Nodo del toroide trasladado y escalado
    planeNode = sg.SceneGraphNode("plane")
    planeNode.transform =tr.matmul([
        tr.translate(0.25,4,-0.35),
        tr.scale(1.0,1.0,1.0),
        tr.rotationX(0.2)
    ])
    planeNode.childs = [plane]

    return planeNode

def createTextureNormalToroide(N):
    # Funcion para crear un toroide con normales y textura

    vertices = []           # lista para almacenar los verices
    indices = []            # lista para almacenar los indices
    dTheta = 2 * np.pi /N   # angulo que hay entre cada iteracion de la coordenada theta
    dPhi = 2 * np.pi /N     # angulo que hay entre cada iteracion de la coordenada phi
    rho = 0.2
    R = 0.5               # radio de la toroide
    c = 0                   # contador de vertices, para ayudar a indicar los indices

    # Se recorre la coordenada theta
    for i in range(N):
        theta = i * dTheta # angulo theta en esta iteracion
        theta1 = (i + 1) * dTheta # angulo theta en la iteracion siguiente
        # Se recorre la coordenada phi
        for j in range(N):
            phi = j*dPhi # angulo phi en esta iteracion
            phi1 = (j+1)*dPhi # angulo phi en la iteracion siguiente

            # Se crean los vertices necesarios son coordenadas esfericas para cada iteracion

            # Vertice para las iteraciones actuales de theta (i) y phi (j) 
            v0 = [np.cos(theta)*(R+rho*np.cos(phi)),np.sin(theta)*(R+rho*np.cos(phi)), rho*np.sin(phi)]
            # Vertice para las iteraciones siguiente de theta (i + 1) y actual de phi (j) 
            v1 = [np.cos(theta1)*(R+rho*np.cos(phi)),np.sin(theta1)*(R+rho*np.cos(phi)), rho*np.sin(phi)]
            # Vertice para las iteraciones actual de theta (i) y siguiente de phi (j + 1) 
            v2 = [np.cos(theta1)*(R+rho*np.cos(phi1)),np.sin(theta1)*(R+rho*np.cos(phi1)), rho*np.sin(phi1)]
            # Vertice para las iteraciones siguientes de theta (i + 1) y phi (j + 1) 
            v3 = [np.cos(theta)*(R+rho*np.cos(phi1)),np.sin(theta)*(R+rho*np.cos(phi1)), rho*np.sin(phi1)]
            
            # Se crean los vectores normales para cada vertice segun los valores de rho tongo 
            n0 = [np.cos(theta)*np.cos(phi), np.sin(theta)*np.cos(phi), np.sin(phi)]
            n1 = [np.cos(theta1)*np.cos(phi), np.sin(theta1)*np.cos(phi), np.sin(phi)]
            n2 = [np.cos(theta1)*np.cos(phi1), np.sin(theta1)*np.cos(phi1), np.sin(phi1)]
            n3 = [np.cos(theta)*np.cos(phi1), np.sin(theta)*np.cos(phi1), np.sin(phi1)]
            
            # Creamos los quads intermedios
            #  v0 -------------- v3
            #  | \                |
            #  |    \             |
            #  |       \          |
            #  |          \       |
            #  |             \    |
            #  |                \ |
            #  v1 -------------- v2
            
            #           vertices              tex coords    normales
            vertices += [v0[0], v0[1], v0[2], 0, 0, n0[0], n0[1], n0[2]]
            vertices += [v1[0], v1[1], v1[2], 0, 1, n1[0], n1[1], n1[2]]
            vertices += [v2[0], v2[1], v2[2], 1, 1, n2[0], n2[1], n2[2]]
            vertices += [v3[0], v3[1], v3[2], 1, 0, n3[0], n3[1], n3[2]]
            indices += [ c + 0, c + 1, c +2 ]
            indices += [ c + 2, c + 3, c + 0 ]
            c += 4
    return bs.Shape(vertices, indices)


def createToroNode(r, g, b, pipeline):
    # Funcion para crear Grafo de un toroide de la escena, se separa en otro grafo, por si se quiere dibujar con otro material
    sphere = createGPUShape(pipeline, createColorNormalToro(20, r,g,b)) # Shape de la toroide

    # Nodo de la toroide trasladado y escalado
    sphereNode = sg.SceneGraphNode("sphere")
    sphereNode.transform =tr.matmul([
        tr.translate(0.25,0.15,-0.35),
        tr.scale(0.3,0.3,0.3)
    ])
    sphereNode.childs = [sphere]

    # Nodo del del objeto escalado con el mismo valor de la escena base
    scaledSphere = sg.SceneGraphNode("sc_sphere")
    scaledSphere.transform = tr.scale(5, 5, 5)
    scaledSphere.childs = [sphereNode]

    return scaledSphere

def createTexToroNode(pipeline):
    # Funcion para crear Grafo de un toroide texturizada de la escena, se separa en otro grafo, por si se quiere dibujar con otro material
    sphere = createTextureGPUShape(createTextureNormalToroide(20), pipeline, "assets/barras.png") # Shape del toroide texturizada

    # Nodo del toroide trasladado y escalado
    sphereNode = sg.SceneGraphNode("sphere")
    sphereNode.transform =tr.matmul([
        tr.translate(-0.25,0.25,-0.35),
        tr.scale(0.3,0.3,0.3)
    ])
    sphereNode.childs = [sphere]

    # Nodo del del objeto escalado con el mismo valor de la escena base
    scaledSphere = sg.SceneGraphNode("sc_sphere")
    scaledSphere.transform = tr.scale(5, 5, 5)
    scaledSphere.childs = [sphereNode]

    return scaledSphere