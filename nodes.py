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

# crea un plano con textura
def createPlane(pipeline, nombre, texture_name):
    plane = GameObject(nombre, pipeline)
    path = "assets/" + texture_name +".png"
    plane.setModel(createTextureGPUShape(createTextureNormalPlane(), pipeline, path), True)

    return plane

# crea un plano con textura que siempre mira a camara
def create3dPlane(pipeline, nombre, texture_name):
    plane = Plane3D(nombre, pipeline)
    path =  "assets/" + texture_name +".png"
    plane.setModel(createTextureGPUShape(createTextureNormalPlane(), pipeline, path), True)

    return plane

# crea a Maru
def createCharacter(pipeline, tex_pipeline, controller):
    bodyMesh = mh.createBodyMesh()
    legModel = createGPUShape(pipeline, createLegShape())
    armModel = createGPUShape(pipeline, createArmShape())
    faceObject = createPlane(tex_pipeline, "face", "smile" )
    tailObject = createTail(pipeline)


    torsoShape = GameObject("torso", pipeline)
    torsoShape.setModel(createGPUShape(pipeline, mh.toShape(bodyMesh, color=(255/255, 128/255, 0.0))))
    torsoShape.uniformScale(1.3)

    leg1Object = GameObject("leg1", pipeline)
    leg1Object.setModel(legModel)
    leg1Object.setPosition([0, 0, -0.4])
    leg1Object.setRotation([0, 0, 180])
    leg1Object.setDrawType("lines")

    leg1Joint = GameObject("leg1joint", pipeline)
    leg1Joint.setPosition([0, -0.2, -0.4])
    leg1Joint.setRotation([0, 0, 0])
    leg1Joint.addChilds([leg1Object])

    leg2Object = GameObject("leg2", pipeline)
    leg2Object.setModel(legModel)
    leg2Object.setPosition([0, 0, -0.4])
    leg2Object.setRotation([0, 0, -90])
    leg2Object.setDrawType("lines")

    leg2Joint = GameObject("leg2joint", pipeline)
    leg2Joint.setPosition([0, 0.2, -0.4])
    leg2Joint.setRotation([0, 0, 0])
    leg2Joint.addChilds([leg2Object])

    legs = GameObject("legs", pipeline)
    legs.addChilds([leg1Joint, leg2Joint])
    legs.setPosition([0, 0, 0])

    leftArm = GameObject("arm1", pipeline)
    leftArm.setDrawType("lines")
    leftArm.setModel(armModel)
    leftArm.setPosition([0, 0.5, 0])

    leftJoint = GameObject("ljoint", pipeline)
    leftJoint.setPosition([0, 0.5, 0])
    leftJoint.addChilds([leftArm])

    rightArm = GameObject("arm2", pipeline)
    rightArm.setDrawType("lines")
    rightArm.setModel(armModel)
    rightArm.setPosition([0, -0.25, 0])

    rightJoint = GameObject("rjoint", pipeline)
    rightJoint.setPosition([0, -0.20, 0])
    rightJoint.addChilds([rightArm])

    faceObject.setPosition([0.57, 0, 0])
    faceObject.setRotation([0, 0, 90])

    body = GameObject("body", pipeline,)
    body.addChilds([torsoShape, faceObject, tailObject, rightJoint, leftJoint])

    character = Character(pipeline, [body, legs], controller) 
    character.setPosition([0, 0, -1])
    character.setTreesMaterial((0.3, 0.3, 0.3), (0.4, 0.4, 0.4), (0.01, 0.01, 0.01), 10) # Un material menos metalico 
    faceObject.setMaterial((0.7, 0.7, 0.7), (0.4, 0.4, 0.4), (0.01, 0.00, 0.00), 10) # Para que la carita siempre sea bien visible :)

    return character

def createScene(pipeline, tex_pipeline):
    # Se crea la escena base

    # Se crean las shapes en GPU
    gpuCube = createGPUShape(pipeline, bs.createColorNormalsCube(1.0,0.7,0.7)) # Shape del cubo gris
    terrainMesh = mh.terrenoMesh(20)
    moonShape = createGPUShape(pipeline, createMoon())

    #publico
    gShyGuy = create3dPlane(tex_pipeline, "shyverde", "greenShyGuy")
    gShyGuy.setPosition([-5.5, -5.0, -2.1])

    bShyGuy = create3dPlane(tex_pipeline, "shyazul", "blueShyGuy")
    bShyGuy.setPosition([-5.1, -6.0, -2.1])

    chomp = create3dPlane(tex_pipeline, "chomp", "chomp")
    chomp.setScale([1.5,1,1])
    chomp.setPosition([3.5, 4.5, -2.1])
    chomp.Ka = (0.7, 0.7, 0.7)
    chomp.Ks = (0.9, 0.9, 0.9) # Es bien metalico

    publico = GameObject("publico", pipeline)
    publico.addChilds([ gShyGuy, bShyGuy, chomp])

    # Nubes
    nube_material = [(0.8, 0.8, 0.8), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)] # Se quiere dar la impresion de que estan lejos asi que no seran afectadas por la luz
    nube1 = create3dPlane(tex_pipeline, "nube1", "cloud")
    nube1.setPosition([-5.1, 6, 3])
    nube1.Ka = nube_material[0]
    nube1.Kd = nube_material[1]
    nube1.Ks = nube_material[2]

    nube2 = create3dPlane(tex_pipeline, "nube2", "cloud")
    nube2.setPosition([-5.1, -6, 3])
    nube2.Ka = nube_material[0]
    nube2.Kd = nube_material[1]
    nube2.Ks = nube_material[2]

    # Arboles 3D
    arbol1 = create3dPlane(tex_pipeline, "arbol1", "tree")
    arbol1.setScale([1.0, 1.0, 1.3])
    arbol1.uniformScale(3)
    arbol1.setPosition([-5.5, 5.0, -1.0])

    arbol2 = create3dPlane(tex_pipeline, "arbol2", "tree")
    arbol2.setScale([1.0, 1.0, 1.3])
    arbol2.uniformScale(3)
    arbol2.setPosition([-6.0, 4.0, -1.0])

    arbol3 = create3dPlane(tex_pipeline, "arbol3", "tree2")
    arbol3.setScale([1.0, 1.0, 1.3])
    arbol3.uniformScale(3)
    arbol3.setPosition([5.5, 5.0, -1.0])

    arbol4 = create3dPlane(tex_pipeline, "arbol4", "tree2")
    arbol4.setScale([1.0, 1.0, 1.3])
    arbol4.uniformScale(3)
    arbol4.setPosition([6.0, 4.0, -1.0])

    arbol5 = create3dPlane(tex_pipeline, "arbol5", "tree")
    arbol5.setScale([1.0, 1.0, 1.3])
    arbol5.uniformScale(3)
    arbol5.setPosition([5.2, -4.3, -1.0])

    arboles = GameObject("arboles", pipeline)
    arboles.addChilds([arbol1, arbol2, arbol3, arbol4, arbol5])

    # Terreno
    terreno = GameObject("terreno", pipeline)
    terreno.setModel(createGPUShape(pipeline, mh.toShape(terrainMesh, color=(40/255, 255/255, 40/255))))
    terreno.setScale([20, 20, 10])
    terreno.setPosition([0, 0, -3.5])
    terreno.Kd = (0.15, 0.15, 0.15) # El pasto se ilumina bastante poco con las luces de colores

    # Nodo del cubo
    cube = GameObject("Cube", pipeline)
    cube.setModel(gpuCube)

    # Nodo del escenario
    escenario = GameObject("escenario", pipeline)
    escenario.setPosition([0, 0, -1])
    escenario.addChilds([cube])

    # Nodo de la escena para realizar un escalamiento
    scene = GameObject("scene", pipeline)
    scene.setPosition([0, 0, -1.5])
    scene.setScale([5,5,1])
    scene.addChilds([escenario])

    # Nodo final de la escena 
    trScene = GameObject("trScene", pipeline)
    trScene.addChilds([scene, arboles, terreno, nube1, nube2, publico])

    return trScene        