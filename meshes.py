import openmesh
import math
import numpy as np
import grafica.basic_shapes as bs

def createTailMesh(textured=False):

	mesh = openmesh.TriMesh()

	# abajo
	d1 = mesh.add_vertex(np.array([  0.5,   0.0,  -1.0]))
	d2 = mesh.add_vertex(np.array([ 0.25, -0.433, -1.0]))
	d3 = mesh.add_vertex(np.array([-0.25, -0.433, -1.0]))
	d4 = mesh.add_vertex(np.array([ -0.5,    0.0, -1.0]))
	d5 = mesh.add_vertex(np.array([-0.25,  0.433, -1.0]))
	d6 = mesh.add_vertex(np.array([ 0.25,  0.433, -1.0])) 

	# arriba
	u1 = mesh.add_vertex(np.array([  0.3,   0.0,  0.0]))
	u2 = mesh.add_vertex(np.array([ 0.15, -0.259, 0.0]))
	u3 = mesh.add_vertex(np.array([-0.15, -0.259, 0.0]))
	u4 = mesh.add_vertex(np.array([ -0.3,    0.0, 0.0]))
	u5 = mesh.add_vertex(np.array([-0.15,  0.259, 0.0]))
	u6 = mesh.add_vertex(np.array([ 0.15,  0.259, 0.0])) 

	# tapa de abajo
	mesh.add_face([d2, d3 ,d1])
	mesh.add_face([d1, d3, d4])
	mesh.add_face([d1, d4, d6])
	mesh.add_face([d6, d4, d5])

	# laterales
	mesh.add_face([d1, u1, u2])
	mesh.add_face([u2, d2, d1])

	mesh.add_face([d2, u2, u3])
	mesh.add_face([u3, d3, d2])

	mesh.add_face([d3, u3, u4])
	mesh.add_face([u4, d4, d3])

	mesh.add_face([d4, u4, u5])
	mesh.add_face([u5, d5, d4])

	mesh.add_face([d5, u5, u6])
	mesh.add_face([u6, d6, d5])

	mesh.add_face([d6, u6, u1])
	mesh.add_face([u1, d1, d6])

	# tapa de arriba
	mesh.add_face([u3, u2, u1])
	mesh.add_face([u3, u1, u4])
	mesh.add_face([u4, u1, u6])
	mesh.add_face([u4, u6, u5])

	return mesh

def createBodyMesh(textured=False):

	mesh = openmesh.TriMesh()

	# abajo
	d1 = mesh.add_vertex(np.array([  0.3,   0.0,  -0.28]))
	d2 = mesh.add_vertex(np.array([ 0.15, -0.259, -0.28]))
	d3 = mesh.add_vertex(np.array([-0.15, -0.259, -0.28]))
	d4 = mesh.add_vertex(np.array([ -0.3,    0.0, -0.28]))
	d5 = mesh.add_vertex(np.array([-0.15,  0.259, -0.28]))
	d6 = mesh.add_vertex(np.array([ 0.15,  0.259, -0.28])) 

	# centro
	c1 = mesh.add_vertex(np.array([  0.5,   0.0,  0.0]))
	c2 = mesh.add_vertex(np.array([ 0.25, -0.433, 0.0]))
	c3 = mesh.add_vertex(np.array([-0.25, -0.433, 0.0]))
	c4 = mesh.add_vertex(np.array([ -0.5,    0.0, 0.0]))
	c5 = mesh.add_vertex(np.array([-0.25,  0.433, 0.0]))
	c6 = mesh.add_vertex(np.array([ 0.25,  0.433, 0.0])) 

	# arriba
	u1 = mesh.add_vertex(np.array([  0.3,   0.0,  0.28]))
	u2 = mesh.add_vertex(np.array([ 0.15, -0.259, 0.28]))
	u3 = mesh.add_vertex(np.array([-0.15, -0.259, 0.28]))
	u4 = mesh.add_vertex(np.array([ -0.3,    0.0, 0.28]))
	u5 = mesh.add_vertex(np.array([-0.15,  0.259, 0.28]))
	u6 = mesh.add_vertex(np.array([ 0.15,  0.259, 0.28])) 

	# tapa de abajo
	mesh.add_face([d2, d3 ,d1])
	mesh.add_face([d1, d3, d4])
	mesh.add_face([d1, d4, d6])
	mesh.add_face([d6, d4, d5])

	# laterales bajos
	mesh.add_face([d1, c1, c2])
	mesh.add_face([c2, d2, d1])
	mesh.add_face([d2, c2, c3])
	mesh.add_face([c3, d3, d2])
	mesh.add_face([d3, c3, c4])
	mesh.add_face([c4, d4, d3])
	mesh.add_face([d4, c4, c5])
	mesh.add_face([c5, d5, d4])
	mesh.add_face([d5, c5, c6])
	mesh.add_face([c6, d6, d5])
	mesh.add_face([d6, c6, c1])
	mesh.add_face([c1, d1, d6])

	# laterales altos
	mesh.add_face([c1, u1, u2])
	mesh.add_face([u2, c2, c1])
	mesh.add_face([c2, u2, u3])
	mesh.add_face([u3, c3, c2])
	mesh.add_face([c3, u3, u4])
	mesh.add_face([u4, c4, c3])
	mesh.add_face([c4, u4, u5])
	mesh.add_face([u5, c5, c4])
	mesh.add_face([c5, u5, u6])
	mesh.add_face([u6, c6, c5])
	mesh.add_face([c6, u6, u1])
	mesh.add_face([u1, c1, c6])
	

	# tapa de arriba
	mesh.add_face([u3, u2, u1])
	mesh.add_face([u3, u1, u4])
	mesh.add_face([u4, u1, u6])
	mesh.add_face([u4, u6, u5])

	return mesh

# funcion que modela el terreno
def terreno(x, y):
	return math.sin(10*(x**2 + y ** 2))/10

def terrenoMesh(N):

    # Creamos arreglos entre -5 y 5, de tamaño N
    xs = np.linspace(-1, 1, N)
    ys = np.linspace(-1, 1, N)

    # Creamos una malla de triangulos
    mesh = openmesh.TriMesh()

    # Generamos un vertice para cada x,y,z
    for i in range(len(xs)):
        for j in range(len(ys)):
            x = xs[i]
            y = ys[j]
            z = terreno(x, y)
            
            # Agregamos el vertice a la malla
            mesh.add_vertex([x, y, z])

    # Podemos calcular el indice de cada punto (i,j) de la siguiente manera
    index = lambda i, j: i*len(ys) + j 
    
    # Obtenemos los vertices
    vertexs = list(mesh.vertices())

    # Creamos caras para cada cuadrado de la malla
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):

            # Conseguimos los indices por cada cuadrado
            isw = index(i,j)
            ise = index(i+1,j)
            ine = index(i+1,j+1)
            inw = index(i,j+1)

            # añadimos las caras
            mesh.add_face(vertexs[isw], vertexs[ise], vertexs[ine])
            mesh.add_face(vertexs[ine], vertexs[inw], vertexs[isw])

    return mesh

def toShape(mesh, color=None, textured=False, verbose=False):
    assert isinstance(mesh, openmesh.TriMesh)
    assert (color != None) != textured, "The mesh will be colored or textured, only one of these need to be specified."

    # Requesting normals per face
    mesh.request_face_normals()

    # Requesting normals per vertex
    mesh.request_vertex_normals()

    # Computing all requested normals
    mesh.update_normals()

    # You can also update specific normals
    #mesh.update_face_normals()
    #mesh.update_vertex_normals()
    #mesh.update_halfedge_normals()

    # At this point, we are sure we have normals computed for each face.
    assert mesh.has_face_normals()

    vertices = []
    indices = []

    # To understand how iteraors and circulators works in OpenMesh, check the documentation at:
    # https://www.graphics.rwth-aachen.de:9000/OpenMesh/openmesh-python/-/blob/master/docs/iterators.rst

    def extractCoordinates(numpyVector3):
        assert len(numpyVector3) == 3
        x = vertex[0]
        y = vertex[1]
        z = vertex[2]
        return [x,y,z]

    # This is inefficient, but it works!
    # You can always optimize it further :)

    # Checking each face
    for faceIt in mesh.faces():
        faceId = faceIt.idx()
        if verbose: print("face: ", faceId)

        # Checking each vertex of the face
        for faceVertexIt in mesh.fv(faceIt):
            faceVertexId = faceVertexIt.idx()

            # Obtaining the position and normal of each vertex
            vertex = mesh.point(faceVertexIt)
            normal = mesh.normal(faceVertexIt)
            if verbose: print("vertex ", faceVertexId, "-> position: ", vertex, " normal: ", normal)

            x, y, z = extractCoordinates(vertex)
            nx, ny, nz = extractCoordinates(normal)

            if textured:
                assert mesh.has_vertex_texcoords2D()

                texcoords = mesh.texcoord2D(faceVertexIt)
                tx = texcoords[0]
                ty = texcoords[1]
                
                vertices += [x, y, z, tx, ty, nx, ny, nz]
                indices += [len(vertices)//8 - 1]
            else:
                assert color != None

                r = color[0]
                g = color[1]
                b = color[2]

                vertices += [x, y, z, r, g, b, nx, ny, nz]
                indices += [len(vertices)//9 - 1]
        
        if verbose: print()

    return bs.Shape(vertices, indices)    