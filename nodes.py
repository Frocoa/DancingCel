import meshes as mh
from gameobject import GameObject
from plane3d import Plane3D
from character import Character
from shapes3d import *

def createTail(pipeline):
    tailMesh = mh.createTailMesh()
    tailGPU = createGPUShape(pipeline, mh.toShape(tailMesh, color=(255/255, 128/255, 0.0)))
    spikeGPU = createGPUShape(pipeline, mh.toShape(tailMesh, color = (220/255, 220/255, 220/225)))


    tail4 = GameObject("tail4", pipeline)
    tail4.setModel(tailGPU)
    tail4.setPosition([0, 0, 1])

    spike4 = GameObject("spike4", pipeline)
    spike4.setModel(spikeGPU)
    spike4.uniformScale(0.3)
    spike4.setRotation([0, 90, 0])
    spike4.setPosition([0.7, 0, 0.5])

    joint4 = GameObject("joint4", pipeline)
    joint4.addChilds([tail4, spike4]) 
    joint4.setPosition([0, 0, 0.5])
    joint4. setRotation([0, 15, 0])

    tail3 = GameObject("tail3", pipeline)
    tail3.setModel(tailGPU)
    tail3.setPosition([0, 0, 1])

    spike3 = GameObject("spike3", pipeline)
    spike3.setModel(spikeGPU)
    spike3.uniformScale(0.3)
    spike3.setRotation([0, 90, 0])
    spike3.setPosition([0.7, 0, 0.5])

    joint3 = GameObject("joint3", pipeline)
    joint3.addChilds([tail3, spike3, joint4]) 
    joint3.setPosition([0, 0, 0.5])
    joint3. setRotation([0, 15, 0])
    
    tail2 = GameObject("tail2", pipeline)
    tail2.setModel(tailGPU)
    tail2.setPosition([0, 0, 1])

    spike2 = GameObject("spike2", pipeline)
    spike2.setModel(spikeGPU)
    spike2.uniformScale(0.3)
    spike2.setRotation([0, 90, 0])
    spike2.setPosition([0.7, 0, 0.5])

    joint2 = GameObject("joint2", pipeline)
    joint2.addChilds([tail2, spike2, joint3])
    joint2.setPosition([0, 0, 0.5])
    joint2.setRotation([0, 15, 0])

    tail1 = GameObject("tail1", pipeline)
    tail1.setModel(tailGPU)
    tail1.setPosition([0, 0, 1])

    spike1 = GameObject("spike1", pipeline)
    spike1.setModel(spikeGPU)
    spike1.uniformScale(0.3)
    spike1.setRotation([0, 90, 0])
    spike1.setPosition([0.7, 0, 0.5])

    joint1 = GameObject("joint1", pipeline)
    joint1.addChilds([tail1, spike1, joint2])
    joint1.setPosition([-1.4,0,0])
    joint1.setRotation([0,-90,0])

    tail = GameObject("tail", pipeline)
    tail.addChilds([joint1])
    tail.uniformScale(0.35)

    return tail

def createPlane(pipeline, nombre, texture_name):
    plane = GameObject(nombre, pipeline)
    path = "assets/" + texture_name +".png"
    plane.setModel(createTextureGPUShape(createTextureNormalPlane(), pipeline, path), True)

    return plane

def create3dPlane(pipeline, nombre, texture_name):
    plane = Plane3D(nombre, pipeline)
    path =  "assets/" + texture_name +".png"
    plane.setModel(createTextureGPUShape(createTextureNormalPlane(), pipeline, path), True)

    return plane

def createCharacter(pipeline, tex_pipeline):
    bodyMesh = mh.createBodyMesh()
    legModel = createGPUShape(pipeline, createLegShape())
    faceObject = createPlane(tex_pipeline, "face", "smile" )
    tailObject = createTail(pipeline)


    torsoShape = GameObject("torso", pipeline)
    torsoShape.setModel(createGPUShape(pipeline, mh.toShape(bodyMesh, color=(255/255, 128/255, 0.0))))
    torsoShape.uniformScale(1.3)

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

    body = GameObject("body", pipeline)
    body.addChilds([torsoShape, faceObject])

    character = Character(pipeline, [body, tailObject,leg1Object, leg2Object]) 
    character.setPosition([0, 0, -1])
    character.setTreesMaterial((0.3, 0.3, 0.3), (0.4, 0.4, 0.4), (0.01, 0.01, 0.01), 10) # Un material menos metalico 
    faceObject.setMaterial((0.7, 0.7, 0.7), (0.4, 0.4, 0.4), (0.01, 0.01, 0.01), 10) # Para que la carita siempre sea bien visible :)

    return character

def createScene(pipeline, tex_pipeline):
    # Se crea la escena base

    # Se crean las shapes en GPU
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(1.0,0.7,0.7)) # Shape del cubo gris
    
    # Arbol 3D
    arbol3D = create3dPlane(tex_pipeline, "arbol", "tree")
    arbol3D.setScale([1.0, 1.0, 1.3])
    arbol3D.setPosition([-6.0, 3.0, -1.0])

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
    trScene.addChilds([scene, arbol3D])

    return trScene        