import meshes as mh
from gameobject import GameObject
from shapes3d import *


def createScene(pipeline):
    # Se crea la escena base

    # Se crean las shapes en GPU
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(1.0,0.7,0.7)) # Shape del cubo gris

    # Nodo del cubo gris
    grayCube = GameObject("grayCube", pipeline)
    grayCube.setModel(gpuGrayCube)

    # Nodo del suelo de color gris
    floor = GameObject("floor", pipeline)
    floor.setPosition([0, 0, -1])
    floor.addChilds([grayCube])

    # Nodo de la escena para realizar un escalamiento
    scene = GameObject("scene", pipeline)
    scene.setPosition([0, 0, -1.5])
    scene.setScale([5,5,1])
    scene.addChilds([floor])

    # Nodo final de la escena 
    trScene = GameObject("trScene", pipeline)
    trScene.addChilds([scene])

    return trScene

    

def createTail(pipeline):
    tailMesh = mh.createTailMesh()
    tailGPU = createGPUShape(pipeline, mh.toShape(tailMesh, color=(255/255, 128/255, 0.0)))

    tail4 = GameObject("tail4", pipeline)
    tail4.setModel(tailGPU)
    tail4.setPosition([0, 0, 1])

    joint4 = GameObject("joint4", pipeline)
    joint4.addChilds([tail4]) 
    joint4.setPosition([0, 0, 0.5])
    joint4. setRotation([0, 15, 0])

    tail3 = GameObject("tail3", pipeline)
    tail3.setModel(tailGPU)
    tail3.setPosition([0, 0, 1])

    joint3 = GameObject("joint3", pipeline)
    joint3.addChilds([tail3, joint4]) 
    joint3.setPosition([0, 0, 0.5])
    joint3. setRotation([0, 15, 0])
    
    tail2 = GameObject("tail2", pipeline)
    tail2.setModel(tailGPU)
    tail2.setPosition([0, 0, 1])

    joint2 = GameObject("joint2", pipeline)
    joint2.addChilds([tail2, joint3])
    joint2.setPosition([0, 0, 0.5])
    joint2.setRotation([0, 15, 0])

    tail1 = GameObject("tail1", pipeline)
    tail1.setModel(tailGPU)
    tail1.setPosition([0, 0, 1])

    joint1 = GameObject("joint1", pipeline)
    joint1.addChilds([tail1, joint2])
    joint1.setPosition([-1.4,0,0])
    joint1.setRotation([0,-90,0])

    tail = GameObject("tail", pipeline)
    tail.addChilds([joint1])
    tail.uniformScale(0.35)

    return tail

def createPlane(pipeline, nombre, texture_name):
    plane = GameObject(nombre, pipeline)
    path = "assets/" + texture_name +".png"
    plane.setModel(createTextureGPUShape(createTextureNormalPlane(), pipeline, path))

    return plane

def createCharacter(pipeline, tex_pipeline):
    bodyMesh = mh.createBodyMesh()
    legModel = createGPUShape(pipeline, createLegShape())
    faceObject = createPlane(tex_pipeline, "face", "smile" )
    tailObject = createTail(pipeline)


    bodyShape = GameObject("body", pipeline)
    bodyShape.setModel(createGPUShape(pipeline, mh.toShape(bodyMesh, color=(255/255, 128/255, 0.0))))
    bodyShape.uniformScale(1.3)

    leg1Object = GameObject("leg1", pipeline)
    leg1Object.setModel(legModel)
    leg1Object.setPosition([0, -0.2, -0.8])
    leg1Object.setRotation([0, 0, 180])
    leg1Object.setDrawType("lines")

    leg2Object = GameObject("leg2", pipeline)
    leg2Object.setModel(legModel)
    leg2Object.setPosition([0, 0.2, -0.8])
    leg2Object.setRotation([0, 0, -90])
    leg2Object.setDrawType("lines")

    faceObject.setPosition([0.57, 0, 0])
    faceObject.setRotation([0, 0, 90])

    character = GameObject("character", pipeline)
    character.addChilds([bodyShape, tailObject, faceObject,leg1Object, leg2Object])


    return character    