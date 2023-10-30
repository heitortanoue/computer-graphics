import glfw
from OpenGL.GL import *
import numpy as np
import math
import glm
from PIL import Image

from src.functions import *
from src.model import *


def key_event_static(window,key,scancode,action,mods):
    engine = glfw.get_window_user_pointer(window)

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window,True)

    engine.keyEvent(window,key,scancode,action,mods)

vertex_code = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        varying vec2 out_texture;

        uniform mat4 mat_transform;

        void main(){
            gl_Position = mat_transform * vec4(position,1.0);
            out_texture = vec2(texture_coord);
        }
        """

fragment_code = """
        uniform vec4 color;
        varying vec2 out_texture;
        uniform sampler2D samplerTexture;

        void main(){
            vec4 texture = texture2D(samplerTexture, out_texture);
            gl_FragColor = texture;
        }
        """

class Engine:
    boundaries = glm.vec4(0,0,0,0)
    position = glm.vec3(0,0,0)

    def __init__(self):
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")

        self.objects = []
        self.textures = []
        self.objectOnFocus = 1
        self.init()


    def init(self):
        print("Initializing Engine...")
        self.initWindow()
        self.initShaders()
        self.buildProgram()
        self.initTextures()

        self.loadModel("capsule")
        self.loadModel("monstro")
        self.loadModel("cat")
        self.loadModel("skull")
        self.loadModel("statue")

        self.showWindow()
        print("Engine initialized.")


    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glClearColor(1.0, 1.0, 1.0, 1.0)

            # seleciona o objeto a ser desenhado
            model = self.objects[self.objectOnFocus]

            # muda o buffer para o do objeto selecionado
            self.switchBuffers(model)

            model.applyTransformations()

            loc_mat_transform = glGetUniformLocation(self.program, "mat_transform")
            glUniformMatrix4fv(loc_mat_transform, 1, GL_FALSE, glm.value_ptr(model.mat_transform))
            self.drawModels(model)

            glfw.swap_buffers(self.window)

    glfw.terminate()


    def initWindow(self):
        print('Initializing Window...')
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
        altura = 1600
        largura = 1200
        self.window = glfw.create_window(largura, altura, "Trabalho 1", None, None)
        glfw.make_context_current(self.window)
        glfw.set_window_user_pointer(self.window, self)


    def initShaders(self):
        print('Initializing Shaders...')
        self.program = glCreateProgram()
        vertex = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        # Set shaders source
        glShaderSource(vertex, vertex_code)
        glShaderSource(fragment, fragment_code)

        # Compile shaders
        glCompileShader(vertex)
        if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Vertex Shader")

        glCompileShader(fragment)
        if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Fragment Shader")

        # Attach shader objects to the program
        glAttachShader(self.program, vertex)
        glAttachShader(self.program, fragment)


    def buildProgram(self):
        print('Building Program...')
        # Build program
        glLinkProgram(self.program)
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(self.program))
            raise RuntimeError('Linking error')

        # Make program the default program
        glUseProgram(self.program)


    def initTextures(self):
        print('Initializing Textures...')
        glEnable(GL_TEXTURE_2D)
        qtd_texturas = 5
        self.textures = glGenTextures(qtd_texturas)


    def showWindow(self):
        self.polygonal_mode = False
        self.texture_filter = False
        glfw.show_window(self.window)
        glfw.set_key_callback(self.window, key_event_static)
        glEnable(GL_DEPTH_TEST) ### importante para 3D


    def load_texture_from_file(self, texture_id, imagem):
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        img = Image.open(create_model_path(imagem, 'jpg'))
        img_width = img.size[0]
        img_height = img.size[1]
        image_data = img.tobytes("raw", "RGB", 0, -1)
        #image_data = np.array(list(img.getdata()), np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)


    def loadModel(self, model):
        print('Loading Model `' + model + '` ...')

        modelIndex = len(self.objects)
        modelo = Model(model)

        # Request a buffer slot from GPU
        modelo.buffer = glGenBuffers(2)

        ### inserindo vertices do modelo no vetor de vertices
        print('Processando modelo OBJ. Vertice inicial:',len(modelo.vertices))
        for face in modelo.model['faces']:
            for vertice_id in face[0]:
                modelo.vertices.append( modelo.model['vertices'][vertice_id-1] )
            for texture_id in face[1]:
                modelo.texture_coords.append( modelo.model['texture'][texture_id-1] )
        print('Processando modelo OBJ. Vertice final:',len(modelo.vertices))

        ### carregando textura equivalente e definindo um id (buffer): use um id por textura!
        self.load_texture_from_file(modelIndex, model)
        self.objects.append(modelo)


    def switchBuffers(self, modelo):
        vertices = np.zeros(len(modelo.vertices), [("position", np.float32, 3)])
        vertices['position'] = modelo.vertices

        # Upload data
        glBindBuffer(GL_ARRAY_BUFFER, modelo.buffer[0])
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)


        textures = np.zeros(len(modelo.texture_coords), [("position", np.float32, 2)]) # duas coordenadas
        textures['position'] = modelo.texture_coords

        # Upload data
        glBindBuffer(GL_ARRAY_BUFFER, modelo.buffer[1])
        glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
        stride = textures.strides[0]
        offset = ctypes.c_void_p(0)
        loc_texture_coord = glGetAttribLocation(self.program, "texture_coord")
        glEnableVertexAttribArray(loc_texture_coord)
        glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)


    def drawModels(self, model):
        #define id da textura do modelo
        glBindTexture(GL_TEXTURE_2D, self.objectOnFocus)

        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, 0, len(model.vertices))

    def keyEvent(self, window, key, scancode, action, mods):
        if key == glfw.KEY_P and action == glfw.PRESS:
            self.polygonal_mode = not self.polygonal_mode
            if self.polygonal_mode:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            return

        if key == glfw.KEY_V and action == glfw.PRESS:
            self.texture_filter = not self.texture_filter
            if self.texture_filter:
                print("Texture filter: GL_NEAREST")
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            else:
                print("Texture filter: GL_LINEAR")
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            return

        if key >= glfw.KEY_1 and key <= glfw.KEY_5 and action == glfw.PRESS:
            self.objectOnFocus = key - glfw.KEY_1
            print("Object on focus: ", self.objectOnFocus)
            return


        modelOnFocus = self.objects[self.objectOnFocus]
        rotationSpeed = 0.2 * math.pi / 10
        translationSpeed = .1 * abs(math.exp(modelOnFocus.scale))
        print(translationSpeed)
        scaleSpeed = 0.1

        if key == glfw.KEY_Z and action == glfw.PRESS:
            modelOnFocus.scale *= (1 + scaleSpeed)
            return

        if key == glfw.KEY_X and action == glfw.PRESS:
            modelOnFocus.scale *= (1 - scaleSpeed)
            return

        if key == glfw.KEY_W and action == glfw.PRESS:
            modelOnFocus.translation.y += +translationSpeed
            return

        if key == glfw.KEY_S and action == glfw.PRESS:
            modelOnFocus.translation.y += -translationSpeed
            return

        if key == glfw.KEY_A and action == glfw.PRESS:
            modelOnFocus.translation.x += -translationSpeed
            return

        if key == glfw.KEY_D and action == glfw.PRESS:
            modelOnFocus.translation.x += +translationSpeed
            return

        # rotation using the arrow keys
        if key == glfw.KEY_UP:
            modelOnFocus.rotation.x += +rotationSpeed
            return

        if key == glfw.KEY_DOWN:
            modelOnFocus.rotation.x += -rotationSpeed
            return

        if key == glfw.KEY_LEFT:
            modelOnFocus.rotation.y += +rotationSpeed
            return

        if key == glfw.KEY_RIGHT:
            modelOnFocus.rotation.y += -rotationSpeed
            return

        if key == glfw.KEY_M:
            modelOnFocus.rotation.z += +rotationSpeed
            return

        if key == glfw.KEY_N:
            modelOnFocus.rotation.z += -rotationSpeed
            return