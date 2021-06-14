from OpenGL.GL import *
import numpy as np

# Componentes aportados por la fuente de luz
def setLightUniforms(pipeline, lights):

        light1 = lights[0]
        light2 = lights[1]
        light3 = lights[2]
        
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.25, 0.25, 0.25) # Componente ambiental de cada luz

        glUniformMatrix3fv(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1, GL_TRUE, \
        np.array([light1.Ld, light2.Ld, light3.Ld]).T) # Componente difusa de cada luz

        glUniformMatrix3fv(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1, GL_TRUE, \
        np.array([light1.Ls, light2.Ls, light3.Ls]).T) # Componente especular de cada luz

        glUniformMatrix3fv(glGetUniformLocation(pipeline.shaderProgram, "lightPos"), 1, GL_TRUE, \
        np.array([light1.position, light2.position, light3.position]).T) # Componente especular de cada luz

        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.05)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.03)

# Componentes aportadas por las especificaciones del material de cada objeto
def setMaterialUniforms(pipeline, Ka, Kd, Ks, shininess):

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), Ka[0], Ka[1], Ka[2]) # Componente ambiental
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), Kd[0], Kd[1], Kd[2]) # Componente difusa
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), Ks[0], Ks[1], Ks[2]) # Componente especular
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), shininess) # Coef de brillo

# Uniforms de la camara
def setCameraUniforms(pipeline, camera, projection, viewMatrix):
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)                