from OpenGL.GL import *

# Componentes aportados por la fuente de luz
def setLightUniforms(pipeline, La = [0.25, 0.25, 0.25] , Ld = [0.5, 0.5, 0.5], Ls = [1.0, 1.0, 1.0]):
        
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), La[0], La[1], La[2]) # Componente ambiental
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), Ld[0], Ld[1], Ld[2]) # Componente difusa
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), Ls[0], Ls[2], Ls[2]) # Componente especular

        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.05)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.03)

# Componentes aportadas por las especificaciones del material de cada objeto
def setMaterialUniforms(pipeline):

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2) # Componente ambiental
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5) # Componente difusa
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.1, 0.1, 0.1) # Componente especular
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 50) # Coef de brillo

# Uniforms de la camara
def setCameraUniforms(pipeline, camera, projection, viewMatrix):
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)                