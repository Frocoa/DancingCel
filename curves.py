# coding=utf-8
"""Catmull-Rom , Hermite and Bezier curves using python and numpy """

import numpy as np
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D

def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T


def hermiteMatrix(P1, P2, T1, T2):

    P1 = np.array([P1]).T
    P2 = np.array([P2]).T
    T1 = np.array([T1]).T
    T2 = np.array([T2]).T
    
    # Generate a matrix concatenating the columns
    G = np.concatenate((P1, P2, T1, T2), axis=1)
    
    # Hermite base matrix is a constant
    Mh = np.array([[1, 0, -3, 2], [0, 0, 3, -2], [0, 1, -2, 1], [0, 0, -1, 1]])    
    
    return np.matmul(G, Mh)


def bezierMatrix(P0, P1, P2, P3):

    P0 = np.array([P0]).T
    P1 = np.array([P1]).T
    P2 = np.array([P2]).T
    P3 = np.array([P3]).T
    
    # Generate a matrix concatenating the columns
    G = np.concatenate((P0, P1, P2, P3,), axis=1)

    # Bezier base matrix is a constant
    Mb = np.array([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]])
    
    return np.matmul(G, Mb)

def catMatrix(P0, P1, P2, P3):

    # Los puntos se transponen para generar una matriz
    P0 = np.array([P0]).T
    P1 = np.array([P1]).T
    P2 = np.array([P2]).T
    P3 = np.array([P3]).T

    #Generate a matrix concatenatig the colums
    G = np.concatenate((P0, P1, P2 ,P3), axis=1)

    #Cat base matrix is a constant
    Mc = (1/2)*np.array([[0, -1, 2, -1], [2, 0, -5, 3], [0, 1, 4, -3], [0, 0, -1, 1]])

    return np.matmul(G,Mc)
   

# M is the cubic curve matrix, N is the number of samples between 0 and 1
def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T
        
    return curve


# Este metodo evalua curvas de Catmull-Rom de una cantidad arbitraria de puntos y las conecta
def evalMultiCatCurve(points, N):
    assert len(points) >= 4, "Se necesitan al menos 4 puntos para Catmull-Rom"

    matrices = []
    counter = 0
    curvesAmount = len(points) - 3
    

    # Matrices
    while counter <= curvesAmount - 1:
        matrices.append(
                    catMatrix(
                        points[counter],
                        points[counter + 1],
                        points[counter + 2],
                        points[counter + 3]))
        counter += 1


    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N//curvesAmount)
    offset = N//curvesAmount
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts) * curvesAmount, 3), dtype=float)
    
    for i in range(len(ts)):
        T = generateT(ts[i])

        

        # se va llenando la matriz curve
        counter = 0
        for matrix in matrices:
            curve[i + offset * counter, 0:3] = np.matmul(matrix, T).T
            counter += 1
        
    return curve    