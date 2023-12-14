import glfw
from OpenGL.GL import *
import numpy as np
import math
import glm
from PIL import Image

from src.functions import *
from src.model import *
from src.camera import *


def key_event_static(window,key,scancode,action,mods):
    engine = glfw.get_window_user_pointer(window)

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        printMessage("Closing window...", "red")
        glfw.set_window_should_close(window,True)

    if key == glfw.KEY_F and action == glfw.PRESS:
        engine.toggleFullscreen()

    engine.keyEvent(window,key,scancode,action,mods)

def mouse_event(window, xpos, ypos):
    engine = glfw.get_window_user_pointer(window)
    sensitivity = 0.001  # Adjust as needed

    if not hasattr(engine, 'last_x'):
        engine.last_x = xpos
        engine.last_y = ypos

    xoffset = xpos - engine.last_x
    yoffset = ypos - engine.last_y
    engine.last_x = xpos
    engine.last_y = ypos

    xoffset *= sensitivity
    yoffset *= sensitivity

    engine.camera.rotation.y += xoffset
    engine.camera.rotation.x -= yoffset

    # Constraint the pitch
    if engine.camera.rotation.x > 1.5:
        engine.camera.rotation.x = 1.5
    if engine.camera.rotation.x < -1.5:
        engine.camera.rotation.x = -1.5

vertex_code = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        varying vec2 out_texture;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
        }
"""

fragment_code = """
        uniform vec4 color;
        varying vec2 out_texture;
        uniform sampler2D samplerTexture;

        const vec3 ambientColor = vec3(1, 1, 1); // White ambient light
        uniform float ambientIntensity; // Intensity of ambient light

        void main(){
            vec4 texture = texture2D(samplerTexture, out_texture);
            vec4 ambient = vec4(ambientColor, 1.0) * ambientIntensity;
            gl_FragColor = texture * ambient;
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
        self.drawBB = False
        self.last_index = 0
        self.camera = Camera(
            position = glm.vec3(0, 0, 0),
            rotation = glm.vec3(0, 0, 0),
        )
        self.ambientIntensity = 0.5
        self.init()


    def init(self):
        printMessage("Initializing Engine...", "green")
        self.initWindow()
        self.initShaders()
        self.buildProgram()
        self.initTextures()

        glUniform1f(glGetUniformLocation(self.program, "ambientIntensity"), self.ambientIntensity)

        skybox_scale = 20
        skybox = self.loadModel('skybox', {
            "scale": skybox_scale,
        })
        self.camera.set_boundaries(skybox)

        skull = self.loadModel("skull", {
            "scale": 0.02,
            "rotation": glm.vec3(-1.57, 0, 0),
            "translation": glm.vec3(2, -0.293, 0.249),
        })
        self.camera.add_model_to_check(skull)

        statue = self.loadModel("statue", {
            "scale": 0.005,
            "rotation": glm.vec3(-1.57, 0, 0),
            "translation": glm.vec3(-0.5, -0.63, 0),
        })
        self.camera.add_model_to_check(statue)

        cat = self.loadModel("cat", {
            "scale": 0.006,
            "rotation": glm.vec3(-1.57, 0, 0),
            "translation": glm.vec3(-1, -0.258, 0.018),
        })
        self.camera.add_model_to_check(cat)

        raptor = self.loadModel("raptor", {
            "scale": 0.01,
            "rotation": glm.vec3(0, 0, 0),
            "translation": glm.vec3(2, 0, -1),
        })
        self.camera.add_model_to_check(raptor)

        monster = self.loadModel("monster", {
            "scale": 0.1,
            "rotation": glm.vec3(0, 0, 0),
            "translation": glm.vec3(3, -0.115, 0),
        })
        self.camera.add_model_to_check(monster)

        self.showWindow()
        printMessage("Engine initialized.", "green")


    def run(self):
        glfw.set_cursor_pos_callback(self.window, mouse_event)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glClearColor(1.0, 1.0, 1.0, 1.0)

            # Configura a câmera para todos os modelos
            loc_view = glGetUniformLocation(self.program, "view")
            glUniformMatrix4fv(loc_view, 1, GL_FALSE, np.array(self.camera.view_matrix()).T)

            loc_projection = glGetUniformLocation(self.program, "projection")
            glUniformMatrix4fv(loc_projection, 1, GL_FALSE, np.array(self.camera.projection_matrix()).T)

            # Desenha todos os modelos
            self.drawAllModels()

            glfw.swap_buffers(self.window)

        glfw.terminate()

    def drawAllModels(self):
        for model in self.objects:
            # Aplica transformações ao modelo atual
            model.applyTransformations()

            # Configura a matriz de modelo
            loc_model = glGetUniformLocation(self.program, "model")
            glUniformMatrix4fv(loc_model, 1, GL_FALSE, np.array(model.mat_transform).T)

            # Desenha o modelo
            self.drawModel(model)


    def toggleFullscreen(self):
        monitor = glfw.get_primary_monitor()
        largura, altura = glfw.get_video_mode (monitor)[0]
        alturaBarraFerramentas = 30

        alturaTotal = altura
        if glfw.get_window_monitor(self.window) is not None:
            # Se estiver em modo de tela cheia, mude para modo janela
            glfw.set_window_monitor(self.window, None, 0, alturaBarraFerramentas, largura, altura - alturaBarraFerramentas, glfw.DONT_CARE)
            alturaTotal = altura - alturaBarraFerramentas
        else:
            # Se estiver em modo janela, mude para modo tela cheia
            glfw.set_window_monitor(self.window, monitor, 0, 0, largura, altura, glfw.DONT_CARE)

        # Atualiza a câmera
        self.camera.set_width_height(largura, alturaTotal)


    def initWindow(self):
        printMessage('Initializing Window...', 'green')
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

        # Obtém o monitor principal
        monitor = glfw.get_primary_monitor()

        # Obtém a resolução da tela do monitor
        largura, altura = glfw.get_video_mode (monitor)[0]

        # Cria a janela em tela cheia
        self.window = glfw.create_window(largura, altura, "Trabalho 1", monitor, None)

        glfw.make_context_current(self.window)
        glfw.set_window_user_pointer(self.window, self)


    def initShaders(self):
        printMessage('Initializing Shaders...', 'green')
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
            printMessage(error, "red")
            raise RuntimeError("Erro de compilacao do Vertex Shader")

        glCompileShader(fragment)
        if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment).decode()
            printMessage(error, "red")
            raise RuntimeError("Erro de compilacao do Fragment Shader")

        # Attach shader objects to the program
        glAttachShader(self.program, vertex)
        glAttachShader(self.program, fragment)


    def buildProgram(self):
        printMessage('Building Program...', 'green')
        # Build program
        glLinkProgram(self.program)
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            printMessage(glGetProgramInfoLog(self.program), "red")
            raise RuntimeError('Linking error')

        # Make program the default program
        glUseProgram(self.program)


    def initTextures(self):
        printMessage('Initializing Textures...', 'green')
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


    def loadModel(self, filename, initial_values = None):
        printMessage(f'Loading Model `{filename}` ...', 'yellow')

        modelo = Model(self.last_index, filename, initial_values)
        self.last_index += 1
        modelData = modelo.model

        # Request a buffer slot from GPU
        modelo.buffer = glGenBuffers(2)

        printMessage(f'Processing OBJ Model. Initial vertex count: {len(modelo.vertices)}', 'grey')

        for face_data in modelData['faces']:
            face, texture, materials = face_data

            for vert_idx in face:
                modelo.vertices.append(modelData['vertices'][vert_idx - 1])

            for tex_idx in texture:
                if tex_idx > 0:  # Ensure that the texture index is valid
                    modelo.texture_coords.append(modelData['texture'][tex_idx - 1])
                else:
                    modelo.texture_coords.append([0.0, 0.0])  # Default texture coordinate

        printMessage(f'Processing OBJ Model. Final vertex count: {len(modelo.vertices)}', 'grey')

        # Load the texture for the model and define a buffer ID
        self.load_texture_from_file(modelo.id, filename)
        self.setModelBuffers(modelo)
        self.objects.append(modelo)

        return modelo


    def setModelBuffers(self, modelo):
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


    def drawModel(self, model):
        # Ativa o buffer de vértices para o modelo atual
        glBindBuffer(GL_ARRAY_BUFFER, model.buffer[0])
        loc_vertices = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, 0, None)

        # Ativa o buffer de coordenadas de textura para o modelo atual
        glBindBuffer(GL_ARRAY_BUFFER, model.buffer[1])
        loc_texture_coord = glGetAttribLocation(self.program, "texture_coord")
        glEnableVertexAttribArray(loc_texture_coord)
        glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, 0, None)

        glBindTexture(GL_TEXTURE_2D, model.id)

        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, 0, len(model.vertices))

        edges = [
            (0, 1), (1, 3), (3, 2), (2, 0),  # Top edges
            (4, 5), (5, 7), (7, 6), (6, 4),  # Bottom edges
            (0, 4), (1, 5), (2, 6), (3, 7)   # Side edges connecting top and bottom
        ]

        if self.drawBB:
            glBegin(GL_LINES)
            for edge in edges:
                for vertex_index in edge:
                    vertex = model.bounding_box[vertex_index]  # vertex is a glm.vec4
                    glVertex3f(vertex.x, vertex.y, vertex.z)  # Using x, y, z components
            glEnd()


    def keyEvent(self, window, key, scancode, action, mods):
        if key == glfw.KEY_P and action == glfw.PRESS:
            self.polygonal_mode = not self.polygonal_mode
            if self.polygonal_mode:
                printMessage("Polygonal mode: GL_LINE", 'blue')
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            else:
                printMessage("Polygonal mode: GL_FILL", 'blue')
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            return

        if key == glfw.KEY_V and action == glfw.PRESS:
            self.texture_filter = not self.texture_filter
            if self.texture_filter:
                printMessage("Texture filter: GL_NEAREST", 'blue')
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            else:
                printMessage("Texture filter: GL_LINEAR", 'blue')
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            return

        # Desenha a bounding box do objeto
        if key == glfw.KEY_B and action == glfw.PRESS:
            self.drawBB = not self.drawBB
            printMessage("Draw bounding box: " + str(self.drawBB), 'blue')
            return

        translationSpeed = 0.05

        if key == glfw.KEY_W:
            self.camera.move_forward(translationSpeed)
            return

        if key == glfw.KEY_S:
            self.camera.move_backward(translationSpeed)
            return

        if key == glfw.KEY_A:
            self.camera.move_left(translationSpeed)
            return

        if key == glfw.KEY_D:
            self.camera.move_right(translationSpeed)
            return
