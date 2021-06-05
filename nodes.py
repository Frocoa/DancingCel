import meshes as mh
from gameobject import GameObject
from shapes3d import *


def createScene(pipeline):
    scene = GameObject("escena", pipeline)
    scene.nodeAddChilds(sceneChilds(pipeline))

    return scene

def createTail(pipeline):
    tailMesh = mh.createTailMesh()
    tailGPU = createGPUShape(pipeline, mh.toShape(tailMesh, color=(255/255, 128/255, 0.0)))
    tail1 = GameObject("tail1", pipeline)
    tail1.setModel(tailGPU)

    tail1.setPosition([0, 0, -1])

    tail2 = GameObject("tail2", pipeline)
    tail2.setModel(tailGPU)
    tail2.setPosition([0, 0.1, 0])
    tail2.setRotation([-10,0,0])

    tail = GameObject("tail", pipeline)
    tail.addChilds([tail1, tail2])
    tail.uniformScale(0.35)
    tail.setPosition([0,-1,0])
    tail.setRotation([90,0,0])

    return tail

def createPlane(pipeline):
    plane = GameObject("planito", pipeline)
    plane.setModel(createTextureGPUShape(createTextureNormalPlane(), pipeline, "assets/barras.png"))

    return plane

def createCharacter(pipeline):
    bodyMesh = mh.createBodyMesh()
    tailObject = createTail(pipeline)

    bodyShape = GameObject("body", pipeline)
    bodyShape.setModel(createGPUShape(pipeline, mh.toShape(bodyMesh, color=(255/255, 128/255, 0.0))))

    character = GameObject("character", pipeline)
    character.addChilds([bodyShape, tailObject])


    return character    