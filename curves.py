# coding=utf-8
"""Hermite and Bezier curves using python, numpy and matplotlib"""

import numpy as np
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D

__author__ = "Daniel Calderon"
__license__ = "MIT"


def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T


def hermiteMatrix(P1, P2, T1, T2):
    
    # Generate a matrix concatenating the columns
    G = np.concatenate((P1, P2, T1, T2), axis=1)
    
    # Hermite base matrix is a constant
    Mh = np.array([[1, 0, -3, 2], [0, 0, 3, -2], [0, 1, -2, 1], [0, 0, -1, 1]])    
    
    return np.matmul(G, Mh)


def bezierMatrix(P0, P1, P2, P3):
    
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

# M is the cubic curve matrix, N is the number of samples between 0 and 1
def evalTripleCurve(P0, P1, P2, P3, P4, P5, N):

    # Matrices
    Mc1 = catMatrix(P0, P1, P2, P3)
    Mc2 = catMatrix(P1, P2, P3, P4)
    Mc3 = catMatrix(P2, P3, P4, P5)

    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N//3)
    offset = N//3
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts)*3, 3), dtype=float)
    
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(Mc1, T).T
        curve[i + offset, 0:3] = np.matmul(Mc2, T).T
        curve[i + offset*2, 0:3] = np.matmul(Mc3, T).T
        
    return curve