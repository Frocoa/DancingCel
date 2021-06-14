""" Pipeline con los shaders enunciados """

from OpenGL.GL import *
import OpenGL.GL.shaders
from grafica.gpu_shape import GPUShape
from PIL import Image
import numpy as np

def textureSimpleSetup(imgName, sWrapMode, tWrapMode, minFilterMode, maxFilterMode):
     # wrapMode: GL_REPEAT, GL_CLAMP_TO_EDGE
     # filterMode: GL_LINEAR, GL_NEAREST
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    # texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, sWrapMode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, tWrapMode)

    # texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilterMode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, maxFilterMode)
    
    image = Image.open(imgName)
    img_data = np.array(image, np.uint8)

    if image.mode == "RGB":
        internalFormat = GL_RGB
        format = GL_RGB
    elif image.mode == "RGBA":
        internalFormat = GL_RGBA
        format = GL_RGBA
    else:
        print("Image mode not supported.")
        raise Exception()

    glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, image.size[0], image.size[1], 0, format, GL_UNSIGNED_BYTE, img_data)

    return texture


class MultiplePhongShaderProgram:
    # Pipeline para multiples fuentes de luz, sin texturas

    def __init__(self):
        vertex_shader = """
            #version 330 core

            layout (location = 0) in vec3 position;
            layout (location = 1) in vec3 color;
            layout (location = 2) in vec3 normal;

            out vec3 fragPosition;
            out vec3 fragOriginalColor;
            out vec3 fragNormal;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main()
            {
                fragPosition = vec3(model * vec4(position, 1.0));
                fragOriginalColor = color;
                fragNormal = mat3(transpose(inverse(model))) * normal;  
                
                gl_Position = projection * view * vec4(fragPosition, 1.0);
            }
            """

        fragment_shader = """
            #version 330 core

            out vec4 fragColor;

            in vec3 fragNormal;
            in vec3 fragPosition;
            in vec3 fragOriginalColor;
            uniform vec3 viewPosition;
            uniform vec3 La;
            uniform mat3 Ld;
            uniform mat3 Ls;
            uniform mat3 lightPos;
            uniform vec3 Ka;
            uniform vec3 Kd;
            uniform vec3 Ks;
            uniform uint shininess;
            uniform float constantAttenuation;
            uniform float linearAttenuation;
            uniform float quadraticAttenuation;

            void main()
            {
                // ambient
                vec3 ambient = Ka * La;
                
                // diffuse
                // fragment normal has been interpolated, so it does not necessarily have norm equal to 1
                vec3 normalizedNormal = normalize(fragNormal);

                // Vector para sumar la contribucion de cada fuente de luz
                vec3 result = vec3(0.0f, 0.0f, 0.0f);

                // Se itera por cada fuente de luz para calcular su contribucion
                for (int i = 0; i < 3; i++)
                {   
                    // direccion a la fuente de luz de la iteacion actual
                    vec3 toLight = lightPos[i] - fragPosition;

                    // Lo demas es exactamente igual
                    vec3 lightDir = normalize(toLight);
                    float diff = max(dot(normalizedNormal, lightDir), 0.0);
                    vec3 diffuse = Kd * Ld[i] * diff;
                    
                    // specular
                    vec3 viewDir = normalize(viewPosition - fragPosition);
                    vec3 reflectDir = reflect(-lightDir, normalizedNormal);  
                    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
                    vec3 specular = Ks * Ls[i] * spec;

                    // attenuation
                    float distToLight = length(toLight);
                    float attenuation = constantAttenuation
                        + linearAttenuation * distToLight
                        + quadraticAttenuation * distToLight * distToLight;
                        
                    // Se suma la contribucion calculada en la iteracion actual
                    result += ((specular + diffuse) / attenuation) ;
                }

                // El calculo final es con la suma final
                result = (ambient + result ) * fragOriginalColor;
                fragColor = vec4(result, 1.0);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, OpenGL.GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, OpenGL.GL.GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color + 3d normals => 3*4 + 3*4 + 3*4 = 36 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        normal = glGetAttribLocation(self.shaderProgram, "normal")
        glVertexAttribPointer(normal, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(24))
        glEnableVertexAttribArray(normal)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

class MultipleCelShaderProgram:
    # Pipeline para multiples fuentes de luz, sin texturas

    def __init__(self):
        vertex_shader = """
            #version 330 core

            layout (location = 0) in vec3 position;
            layout (location = 1) in vec3 color;
            layout (location = 2) in vec3 normal;

            out vec3 fragPosition;
            out vec3 fragOriginalColor;
            out vec3 fragNormal;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main()
            {
                fragPosition = vec3(model * vec4(position, 1.0));
                fragOriginalColor = color;
                fragNormal = mat3(transpose(inverse(model))) * normal;  
                
                gl_Position = projection * view * vec4(fragPosition, 1.0);
            }
            """

        fragment_shader = """
            #version 330 core

            out vec4 fragColor;

            in vec3 fragNormal;
            in vec3 fragPosition;
            in vec3 fragOriginalColor;
            
            uniform vec3 viewPosition;
            uniform vec3 La;
            uniform mat3 Ld;
            uniform mat3 Ls;
            uniform mat3 lightPos;
            uniform vec3 Ka;
            uniform vec3 Kd;
            uniform vec3 Ks;
            uniform uint shininess;
            uniform float constantAttenuation;
            uniform float linearAttenuation;
            uniform float quadraticAttenuation;

            const int levels = 2;

            void main()
            {
                // ambient
                vec3 ambient = Ka * La;
                
                // diffuse
                // fragment normal has been interpolated, so it does not necessarily have norm equal to 1
                vec3 normalizedNormal = normalize(fragNormal);

                // Vector para sumar la contribucion de cada fuente de luz
                vec3 result = vec3(0.0f, 0.0f, 0.0f);

                // Se itera por cada fuente de luz para calcular su contribucion
                for (int i = 0; i < 3; i++)
                {   
                    // direccion a la fuente de luz de la iteacion actual
                    vec3 toLight = lightPos[i] - fragPosition;

                    // Lo demas es exactamente igual
                    vec3 lightDir = normalize(toLight);
                    float diff = max(dot(normalizedNormal, lightDir), 0.0);
                    float level = floor(diff * levels);
                    diff = level/levels;
                    vec3 diffuse = Kd * Ld[i] * diff;
                    
                    // specular
                    vec3 viewDir = normalize(viewPosition - fragPosition);
                    vec3 reflectDir = reflect(-lightDir, normalizedNormal);  
                    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
                    level = floor(spec* levels);
                    spec = level/levels;
                    vec3 specular = Ks * Ls[i] * spec;

                    // attenuation
                    float distToLight = length(toLight);
                    float attenuation = constantAttenuation
                        + linearAttenuation * distToLight
                        + quadraticAttenuation * distToLight * distToLight;
                        
                    // Se suma la contribucion calculada en la iteracion actual
                    result += ((specular + diffuse) / attenuation) ;
                }

                // El calculo final es con la suma final
                result = (ambient + result ) * fragOriginalColor;
                fragColor = vec4(result, 1.0);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, OpenGL.GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, OpenGL.GL.GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color + 3d normals => 3*4 + 3*4 + 3*4 = 36 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        normal = glGetAttribLocation(self.shaderProgram, "normal")
        glVertexAttribPointer(normal, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(24))
        glEnableVertexAttribArray(normal)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

class MultiplePhongSpotShaderProgram:
    # Pipeline para multiples fuentes de luz, sin texturas

    def __init__(self):
        vertex_shader = """
            #version 330 core

            layout (location = 0) in vec3 position;
            layout (location = 1) in vec3 color;
            layout (location = 2) in vec3 normal;

            out vec3 fragPosition;
            out vec3 fragOriginalColor;
            out vec3 fragNormal;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main()
            {
                fragPosition = vec3(model * vec4(position, 1.0));
                fragOriginalColor = color;
                fragNormal = mat3(transpose(inverse(model))) * normal;  
                
                gl_Position = projection * view * vec4(fragPosition, 1.0);
            }
            """

        fragment_shader = """
            #version 330 core

            out vec4 fragColor;

            in vec3 fragNormal;
            in vec3 fragPosition;
            in vec3 fragOriginalColor;
            
            uniform vec3 viewPosition;
            uniform vec3 La;
            uniform mat3 Ld;
            uniform mat3 Ls;
            uniform mat3 lightPos;
            uniform vec3 Ka;
            uniform vec3 Kd;
            uniform vec3 Ks;
            uniform uint shininess;
            uniform float constantAttenuation;
            uniform float linearAttenuation;
            uniform float quadraticAttenuation;

            void main()
            {
                // ambient
                vec3 ambient = Ka * La;
                
                // diffuse
                // fragment normal has been interpolated, so it does not necessarily have norm equal to 1
                vec3 normalizedNormal = normalize(fragNormal);

                // Vector para sumar la contribucion de cada fuente de luz
                vec3 result = vec3(0.0f, 0.0f, 0.0f);

                // Se itera por cada fuente de luz para calcular su contribucion
                for (int i = 0; i < 3; i++)
                {   
                    // direccion a la fuente de luz de la iteacion actual
                    vec3 toLight = lightPos[i] - fragPosition;

                    // Lo demas es exactamente igual
                    vec3 lightDir = normalize(toLight);
                    float diff = max(dot(normalizedNormal, lightDir), 0.0);
                    vec3 diffuse = Kd * Ld[i] * diff;
                    
                    // specular
                    vec3 viewDir = normalize(viewPosition - fragPosition);
                    vec3 reflectDir = reflect(-lightDir, normalizedNormal);  
                    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
                    vec3 specular = Ks * Ls[i] * spec;

                    // attenuation
                    vec3 spotDir = vec3(0,0,1);
                    vec3 L = normalize(-toLight);
                    float concentration = 40;
                    float numerador = pow(max(dot(-spotDir, L), 0.0), concentration);

                    float distToLight = length(toLight);
                    float denominador = constantAttenuation
                        + linearAttenuation * distToLight
                        + quadraticAttenuation * distToLight * distToLight;

                    float attenuation = numerador / denominador;    
                        
                    // Se suma la contribucion calculada en la iteracion actual
                    result += ((specular + diffuse) * attenuation) ;
                }

                // El calculo final es con la suma final
                result = (ambient + result ) * fragOriginalColor;
                fragColor = vec4(result, 1.0);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, OpenGL.GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, OpenGL.GL.GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color + 3d normals => 3*4 + 3*4 + 3*4 = 36 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        normal = glGetAttribLocation(self.shaderProgram, "normal")
        glVertexAttribPointer(normal, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(24))
        glEnableVertexAttribArray(normal)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

class MultipleSpotCelShaderProgram:
    # Pipeline para multiples fuentes de luz, sin texturas

    def __init__(self):
        vertex_shader = """
            #version 330 core

            layout (location = 0) in vec3 position;
            layout (location = 1) in vec3 color;
            layout (location = 2) in vec3 normal;

            out vec3 fragPosition;
            out vec3 fragOriginalColor;
            out vec3 fragNormal;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main()
            {
                fragPosition = vec3(model * vec4(position, 1.0));
                fragOriginalColor = color;
                fragNormal = mat3(transpose(inverse(model))) * normal;  
                
                gl_Position = projection * view * vec4(fragPosition, 1.0);
            }
            """

        fragment_shader = """
            #version 330 core

            out vec4 fragColor;

            in vec3 fragNormal;
            in vec3 fragPosition;
            in vec3 fragOriginalColor;
            
            uniform vec3 viewPosition;
            uniform vec3 La;
            uniform mat3 Ld;
            uniform mat3 Ls;
            uniform mat3 lightPos;
            uniform vec3 Ka;
            uniform vec3 Kd;
            uniform vec3 Ks;
            uniform uint shininess;
            uniform float constantAttenuation;
            uniform float linearAttenuation;
            uniform float quadraticAttenuation;

            const int levels = 4;

            void main()
            {
                // ambient
                vec3 ambient = Ka * La;
                
                // diffuse
                // fragment normal has been interpolated, so it does not necessarily have norm equal to 1
                vec3 normalizedNormal = normalize(fragNormal);

                // Vector para sumar la contribucion de cada fuente de luz
                vec3 result = vec3(0.0f, 0.0f, 0.0f);

                // Se itera por cada fuente de luz para calcular su contribucion
                for (int i = 0; i < 3; i++)
                {   
                    // direccion a la fuente de luz de la iteacion actual
                    vec3 toLight = lightPos[i] - fragPosition;

                    // Lo demas es exactamente igual
                    vec3 lightDir = normalize(toLight);
                    float diff = max(dot(normalizedNormal, lightDir), 0.0);
                    float level = floor(diff*levels);
                    diff = level/levels;
                    vec3 diffuse = Kd * Ld[i] * diff;
                    
                    // specular
                    vec3 viewDir = normalize(viewPosition - fragPosition);
                    vec3 reflectDir = reflect(-lightDir, normalizedNormal);  
                    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
                    level = floor(spec*levels);
                    spec = level/levels;
                    vec3 specular = Ks * Ls[i] * spec;

                    // attenuation
                    vec3 spotDir = vec3(0,0,1);
                    vec3 L = normalize(-toLight);
                    float concentration = 40;
                    float numerador = pow(max(dot(-spotDir, L), 0.0), concentration);
                    level = floor(numerador*levels);
                    numerador = level/levels;

                    float distToLight = length(toLight);
                    float denominador = constantAttenuation
                        + linearAttenuation * distToLight
                        + quadraticAttenuation * distToLight * distToLight;

                    float attenuation = numerador / denominador;    
                        
                    // Se suma la contribucion calculada en la iteracion actual
                    result += ((specular + diffuse) * attenuation) ;
                }

                // El calculo final es con la suma final
                result = (ambient + result ) * fragOriginalColor;
                fragColor = vec4(result, 1.0);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, OpenGL.GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, OpenGL.GL.GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color + 3d normals => 3*4 + 3*4 + 3*4 = 36 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        normal = glGetAttribLocation(self.shaderProgram, "normal")
        glVertexAttribPointer(normal, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(24))
        glEnableVertexAttribArray(normal)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)        

class MultipleTexturePhongShaderProgram:
    # Pipeline para multiples fuentes de luz, con texturas

    def __init__(self):
        vertex_shader = """
            #version 330 core
            
            in vec3 position;
            in vec2 texCoords;
            in vec3 normal;

            out vec3 fragPosition;
            out vec2 fragTexCoords;
            out vec3 fragNormal;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main()
            {
                fragPosition = vec3(model * vec4(position, 1.0));
                fragTexCoords = texCoords;
                fragNormal = mat3(transpose(inverse(model))) * normal;  
                
                gl_Position = projection * view * vec4(fragPosition, 1.0);
            }
            """

        fragment_shader = """
            #version 330 core

            in vec3 fragNormal;
            in vec3 fragPosition;
            in vec2 fragTexCoords;

            out vec4 fragColor;

            uniform vec3 viewPosition; 
            uniform vec3 La;
            uniform mat3 Ld;
            uniform mat3 Ls;
            uniform mat3 lightPos;
            uniform vec3 Ka;
            uniform vec3 Kd;
            uniform vec3 Ks;
            uniform uint shininess;
            uniform float constantAttenuation;
            uniform float linearAttenuation;
            uniform float quadraticAttenuation;

            uniform sampler2D samplerTex;

            void main()
            {
                // ambient
                vec3 ambient = Ka * La;
        
                // diffuse
                // fragment normal has been interpolated, so it does not necessarily have norm equal to 1
                vec3 normalizedNormal = normalize(fragNormal);
                vec4 fragOriginalColor = texture(samplerTex, fragTexCoords);

                if(fragOriginalColor.a < 0.1){
                    discard;
                }

                // Vector para sumar la contribucion de cada fuente de luz
                vec3 result = vec3(0.0f, 0.0f, 0.0f);


                // Se itera por cada fuente de luz para calcular su contribucion
                for (int i = 0; i < 3; i++)
                {
                    // direccion a la fuente de luz de la iteacion actual
                    vec3 toLight = lightPos[i] - fragPosition;

                    // Lo demas es exactamente igual
                    vec3 lightDir = normalize(toLight);
                    float diff = max(dot(normalizedNormal, lightDir), 0.0);
                    vec3 diffuse = Kd * Ld[i] * diff;
                    
                    // specular
                    vec3 viewDir = normalize(viewPosition - fragPosition);
                    vec3 reflectDir = reflect(-lightDir, normalizedNormal);  
                    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
                    vec3 specular = Ks * Ls[i] * spec;

                    // attenuation
                    float distToLight = length(toLight);
                    float attenuation = constantAttenuation
                        + linearAttenuation * distToLight
                        + quadraticAttenuation * distToLight * distToLight;
                    
                    // Se suma la contribucion calculada en la iteracion actual
                    result += ((diffuse + specular) / attenuation) ;
                }

                // El calculo final es con la suma final
                result = (ambient + result) * fragOriginalColor.rgb;
                fragColor = vec4(result, 1.0);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, OpenGL.GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, OpenGL.GL.GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color + 3d normals => 3*4 + 2*4 + 3*4 = 32 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "texCoords")
        glVertexAttribPointer(color, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        normal = glGetAttribLocation(self.shaderProgram, "normal")
        glVertexAttribPointer(normal, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
        glEnableVertexAttribArray(normal)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glBindTexture(GL_TEXTURE_2D, gpuShape.texture)

        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)


class MultipleTextureCelShaderProgram:
    # Pipeline para multiples fuentes de luz, con texturas

    def __init__(self):
        vertex_shader = """
            #version 330 core
            
            in vec3 position;
            in vec2 texCoords;
            in vec3 normal;

            out vec3 fragPosition;
            out vec2 fragTexCoords;
            out vec3 fragNormal;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main()
            {
                fragPosition = vec3(model * vec4(position, 1.0));
                fragTexCoords = texCoords;
                fragNormal = mat3(transpose(inverse(model))) * normal;  
                
                gl_Position = projection * view * vec4(fragPosition, 1.0);
            }
            """

        fragment_shader = """
            #version 330 core

            in vec3 fragNormal;
            in vec3 fragPosition;
            in vec2 fragTexCoords;

            out vec4 fragColor;
            uniform vec3 viewPosition; 
            uniform vec3 La;
            uniform mat3 Ld;
            uniform mat3 Ls;
            uniform mat3 lightPos;
            uniform vec3 Ka;
            uniform vec3 Kd;
            uniform vec3 Ks;
            uniform uint shininess;
            uniform float constantAttenuation;
            uniform float linearAttenuation;
            uniform float quadraticAttenuation;

            const int levels = 2;
            uniform sampler2D samplerTex;

            void main()
            {
                // ambient
                vec3 ambient = Ka * La;
        
                // diffuse
                // fragment normal has been interpolated, so it does not necessarily have norm equal to 1
                vec3 normalizedNormal = normalize(fragNormal);
                vec4 fragOriginalColor = texture(samplerTex, fragTexCoords);

                if(fragOriginalColor.a < 0.1){
                    discard;
                }

                // Vector para sumar la contribucion de cada fuente de luz
                vec3 result = vec3(0.0f, 0.0f, 0.0f);

                // Se itera por cada fuente de luz para calcular su contribucion
                for (int i = 0; i < 3; i++)
                {
                    // direccion a la fuente de luz de la iteacion actual
                    vec3 toLight = lightPos[i] - fragPosition;

                    // Lo demas es exactamente igual
                    vec3 lightDir = normalize(toLight);
                    float diff = max(dot(normalizedNormal, lightDir), 0.0);
                    float level = floor(diff*levels);
                    diff = level/levels;
                    vec3 diffuse = Kd * Ld[i] * diff;
                    
                    // specular
                    vec3 viewDir = normalize(viewPosition - fragPosition);
                    vec3 reflectDir = reflect(-lightDir, normalizedNormal);  
                    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
                    level = floor(spec*levels);
                    spec = level/levels;
                    vec3 specular = Ks * Ls[i] * spec;

                    // attenuation
                    float distToLight = length(toLight);
                    float attenuation = constantAttenuation
                        + linearAttenuation * distToLight
                        + quadraticAttenuation * distToLight * distToLight;
                    
                    // Se suma la contribucion calculada en la iteracion actual
                    result += ((diffuse + specular) / attenuation) ;
                }

                // El calculo final es con la suma final
                result = (ambient + result) * fragOriginalColor.rgb;
                fragColor = vec4(result, 1.0);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, OpenGL.GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, OpenGL.GL.GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color + 3d normals => 3*4 + 2*4 + 3*4 = 32 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "texCoords")
        glVertexAttribPointer(color, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        normal = glGetAttribLocation(self.shaderProgram, "normal")
        glVertexAttribPointer(normal, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
        glEnableVertexAttribArray(normal)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glBindTexture(GL_TEXTURE_2D, gpuShape.texture)

        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)        


class MultipleTexturePhongSpotShaderProgram:
    # Pipeline para multiples fuentes de luz, con texturas

    def __init__(self):
        vertex_shader = """
            #version 330 core
            
            in vec3 position;
            in vec2 texCoords;
            in vec3 normal;

            out vec3 fragPosition;
            out vec2 fragTexCoords;
            out vec3 fragNormal;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main()
            {
                fragPosition = vec3(model * vec4(position, 1.0));
                fragTexCoords = texCoords;
                fragNormal = mat3(transpose(inverse(model))) * normal;  
                
                gl_Position = projection * view * vec4(fragPosition, 1.0);
            }
            """

        fragment_shader = """
            #version 330 core

            in vec3 fragNormal;
            in vec3 fragPosition;
            in vec2 fragTexCoords;

            out vec4 fragColor;
            uniform vec3 viewPosition; 
            uniform vec3 La;
            uniform mat3 Ld;
            uniform mat3 Ls;
            uniform mat3 lightPos;
            uniform vec3 Ka;
            uniform vec3 Kd;
            uniform vec3 Ks;
            uniform uint shininess;
            uniform float constantAttenuation;
            uniform float linearAttenuation;
            uniform float quadraticAttenuation;

            uniform sampler2D samplerTex;

            void main()
            {
                // ambient
                vec3 ambient = Ka * La;
        
                // diffuse
                // fragment normal has been interpolated, so it does not necessarily have norm equal to 1
                vec3 normalizedNormal = normalize(fragNormal);
                vec4 fragOriginalColor = texture(samplerTex, fragTexCoords);

                if(fragOriginalColor.a < 0.1){
                    discard;
                }

                // Vector para sumar la contribucion de cada fuente de luz
                vec3 result = vec3(0.0f, 0.0f, 0.0f);

                // Se itera por cada fuente de luz para calcular su contribucion
                for (int i = 0; i < 3; i++)
                {
                    // direccion a la fuente de luz de la iteacion actual
                    vec3 toLight = lightPos[i] - fragPosition;

                    // Lo demas es exactamente igual
                    vec3 lightDir = normalize(toLight);
                    float diff = max(dot(normalizedNormal, lightDir), 0.0);
                    vec3 diffuse = Kd * Ld[i] * diff;
                    
                    // specular
                    vec3 viewDir = normalize(viewPosition - fragPosition);
                    vec3 reflectDir = reflect(-lightDir, normalizedNormal);  
                    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
                    vec3 specular = Ks * Ls[i] * spec;

                    // attenuation
                    vec3 spotDir = vec3(0,0,1);
                    vec3 L = normalize(-toLight);
                    float concentration = 40;
                    float numerador = pow(max(dot(-spotDir, L), 0.0), concentration);

                    float distToLight = length(toLight);
                    float denominador = constantAttenuation
                        + linearAttenuation * distToLight
                        + quadraticAttenuation * distToLight * distToLight;

                    float attenuation = numerador / denominador;   
                    
                    // Se suma la contribucion calculada en la iteracion actual
                    result += ((diffuse + specular) / attenuation) ;
                }

                // El calculo final es con la suma final
                result = (ambient + result) * fragOriginalColor.rgb;
                fragColor = vec4(result, 1.0);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, OpenGL.GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, OpenGL.GL.GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color + 3d normals => 3*4 + 2*4 + 3*4 = 32 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "texCoords")
        glVertexAttribPointer(color, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        normal = glGetAttribLocation(self.shaderProgram, "normal")
        glVertexAttribPointer(normal, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
        glEnableVertexAttribArray(normal)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glBindTexture(GL_TEXTURE_2D, gpuShape.texture)

        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)


class MultipleTextureSpotCelShaderProgram:
    # Pipeline para multiples fuentes de luz, con texturas

    def __init__(self):
        vertex_shader = """
            #version 330 core
            
            in vec3 position;
            in vec2 texCoords;
            in vec3 normal;

            out vec3 fragPosition;
            out vec2 fragTexCoords;
            out vec3 fragNormal;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main()
            {
                fragPosition = vec3(model * vec4(position, 1.0));
                fragTexCoords = texCoords;
                fragNormal = mat3(transpose(inverse(model))) * normal;  
                
                gl_Position = projection * view * vec4(fragPosition, 1.0);
            }
            """

        fragment_shader = """
            #version 330 core

            in vec3 fragNormal;
            in vec3 fragPosition;
            in vec2 fragTexCoords;

            out vec4 fragColor;
            uniform vec3 viewPosition; 
            uniform vec3 La;
            uniform mat3 Ld;
            uniform mat3 Ls;
            uniform mat3 lightPos;
            uniform vec3 Ka;
            uniform vec3 Kd;
            uniform vec3 Ks;
            uniform uint shininess;
            uniform float constantAttenuation;
            uniform float linearAttenuation;
            uniform float quadraticAttenuation;

            const int levels = 2;
            uniform sampler2D samplerTex;

            void main()
            {
                // ambient
                vec3 ambient = Ka * La;
        
                // diffuse
                // fragment normal has been interpolated, so it does not necessarily have norm equal to 1
                vec3 normalizedNormal = normalize(fragNormal);
                vec4 fragOriginalColor = texture(samplerTex, fragTexCoords);

                if(fragOriginalColor.a < 0.1){
                    discard;
                }

                // Vector para sumar la contribucion de cada fuente de luz
                vec3 result = vec3(0.0f, 0.0f, 0.0f);

                // Se itera por cada fuente de luz para calcular su contribucion
                for (int i = 0; i < 3; i++)
                {
                    // direccion a la fuente de luz de la iteacion actual
                    vec3 toLight = lightPos[i] - fragPosition;

                    // Lo demas es exactamente igual
                    vec3 lightDir = normalize(toLight);
                    float diff = max(dot(normalizedNormal, lightDir), 0.0);
                    float level = floor(diff*levels);
                    diff = level/levels;
                    vec3 diffuse = Kd * Ld * diff;
                    
                    // specular
                    vec3 viewDir = normalize(viewPosition - fragPosition);
                    vec3 reflectDir = reflect(-lightDir, normalizedNormal);  
                    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
                    level = floor(spec*levels);
                    spec = level/levels;
                    vec3 specular = Ks * Ls[i] * spec;

                    // attenuation
                    vec3 spotDir = vec3(0,0,1);
                    vec3 L = normalize(-toLight);
                    float concentration = 40;
                    float numerador = pow(max(dot(-spotDir, L), 0.0), concentration);
                    level = floor(numerador*levels);
                    numerador = level/levels;

                    float distToLight = length(toLight);
                    float denominador = constantAttenuation
                        + linearAttenuation * distToLight
                        + quadraticAttenuation * distToLight * distToLight;

                    float attenuation = numerador / denominador;    
                        
                    // Se suma la contribucion calculada en la iteracion actual
                    result += ((specular + diffuse) * attenuation) ;
                }

                // El calculo final es con la suma final
                result = (ambient + result) * fragOriginalColor.rgb;
                fragColor = vec4(result, 1.0);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, OpenGL.GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, OpenGL.GL.GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color + 3d normals => 3*4 + 2*4 + 3*4 = 32 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "texCoords")
        glVertexAttribPointer(color, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        normal = glGetAttribLocation(self.shaderProgram, "normal")
        glVertexAttribPointer(normal, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
        glEnableVertexAttribArray(normal)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glBindTexture(GL_TEXTURE_2D, gpuShape.texture)

        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)          