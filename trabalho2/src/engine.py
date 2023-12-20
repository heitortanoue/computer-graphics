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
    # Obtém a instância da classe Engine
    engine = glfw.get_window_user_pointer(window)

    # Se a tecla ESC for pressionada, fecha a janela
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        printMessage("Closing window...", "red")
        glfw.set_window_should_close(window,True)

    # Se a tecla F for pressionada, alterna entre fullscreen e janela
    if key == glfw.KEY_F and action == glfw.PRESS:
        engine.toggleFullscreen()

    engine.keyEvent(window,key,scancode,action,mods)

def mouse_event(window, xpos, ypos):
    # Obtém a instância da classe Engine
    engine = glfw.get_window_user_pointer(window)
    sensitivity = 0.001  # Adjust as needed

    if not hasattr(engine, 'last_x'):
        engine.last_x = xpos
        engine.last_y = ypos

    # Calcula o deslocamento do mouse
    xoffset = xpos - engine.last_x
    yoffset = ypos - engine.last_y
    engine.last_x = xpos
    engine.last_y = ypos

    xoffset *= sensitivity
    yoffset *= sensitivity

    engine.camera.rotation.y += xoffset
    engine.camera.rotation.x -= yoffset

    # Limita o ângulo de rotação da câmera
    if engine.camera.rotation.x > 1.5:
        engine.camera.rotation.x = 1.5
    if engine.camera.rotation.x < -1.5:
        engine.camera.rotation.x = -1.5

# Lê o código do shader de um arquivo
vertex_code = readShaderFile('vertex.glsl')
fragment_code = readShaderFile('fragment.glsl')

class Engine:
    boundaries = glm.vec4(0,0,0,0)
    position = glm.vec3(0,0,0)

    # Construtor
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
        self.vCount = 0
        self.ka_multiplier = 0.8
        self.init()


    def init(self):
        printMessage("Initializing Engine...", "green")
        self.initWindow()
        self.initShaders()
        self.buildProgram()
        self.initTextures()

        # Carrega o skybox
        skybox_scale = 20
        skybox = self.loadModel('skybox', {
            "scale": skybox_scale,
            "light": {
                "ambient": 0.8,
                "diffuse": 0.1,
                "specular": 0,
            }
        })
        self.camera.set_boundaries(skybox)

        # Carrega os modelos
        skull = self.loadModel("skull", {
            "scale": 0.02,
            "rotation": glm.vec3(-1.57, 0, 0),
            "translation": glm.vec3(2, -0.293, 0.249),
            "light": {
                "ambient": 0.5,
                "diffuse": 1,
                "specular": 1,
            }
        })
        self.camera.add_model_to_check(skull)

        clock = self.loadModel("clock", {
            "scale": 0.1,
            "rotation": glm.vec3(0, 0, 0),
            "translation": glm.vec3(-0.5, 0, 0),
            "light": {
                "ambient": 0.8,
                "diffuse": 1,
                "specular": 1,
            }
        })
        self.camera.add_model_to_check(clock)

        cat = self.loadModel("cat", {
            "scale": 0.006,
            "rotation": glm.vec3(-1.57, 0, 0),
            "translation": glm.vec3(-1, -0.258, 0.018),
            "light": {
                "ambient": 0.5,
                "diffuse": 1,
                "specular": 0.15,
            }
        })
        self.camera.add_model_to_check(cat)

        raptor = self.loadModel("raptor", {
            "scale": 0.01,
            "rotation": glm.vec3(0, 0, 0),
            "translation": glm.vec3(2, 0, -1),
            "light": {
                "ambient": 0.5,
                "diffuse": 1,
                "specular": 0.2,
            }
        })
        self.camera.add_model_to_check(raptor)

        penguin = self.loadModel("penguin", {
            "scale": 0.2,
            "rotation": glm.vec3(0, 0, 0),
            "translation": glm.vec3(3, -0.115, 0),
            "light": {
                "ambient": 0.5,
                "diffuse": 1,
                "specular": 0.15,
            }
        })
        self.camera.add_model_to_check(penguin)

        self.loadModel("light", {
            "scale": 0.1,
            "rotation": glm.vec3(0, 0, 0),
            "translation": glm.vec3(0, 2, 0),
            "light": {
                "ambient": 1,
                "diffuse": 1,
                "specular": 1,
                "shininess": 1000,
                "is_light_source": True,
            }
        })

        # Carrega os buffers
        self.loadAllBuffers()

        self.showWindow()
        printMessage("Engine initialized.", "green")


    def run(self):
        # Define a função de callback de teclado
        glfw.set_cursor_pos_callback(self.window, mouse_event)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # Loop principal
        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            # Limpa a tela
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glClearColor(0.2, 0.2, 0.2, 1.0)

            # Desenha todos os modelos
            self.drawAllModels()

            # Configura a câmera para todos os modelos
            loc_view = glGetUniformLocation(self.program, "view")
            glUniformMatrix4fv(loc_view, 1, GL_FALSE, np.array(self.camera.view_matrix()).T)

            # Configura a projeção da câmera na GPU
            loc_projection = glGetUniformLocation(self.program, "projection")
            glUniformMatrix4fv(loc_projection, 1, GL_FALSE, np.array(self.camera.projection_matrix()).T)

            # Configura a posição da câmera na GPU
            loc_view_pos = glGetUniformLocation(self.program, "view_position")
            glUniform3f(loc_view_pos, self.camera.position.x, self.camera.position.y, self.camera.position.z)

            # Atualiza a posição da luz
            glfw.swap_buffers(self.window)

        glfw.terminate()

    def drawAllModels(self):
        for model in self.objects:
            # Aplica transformações ao modelo atual
            model.applyTransformations()

            # Configura a matriz de modelo
            loc_model = glGetUniformLocation(self.program, "model")
            glUniformMatrix4fv(loc_model, 1, GL_FALSE, np.array(model.mat_transform).T)

            # Aplica iluminação
            loc_ka = glGetUniformLocation(self.program, "ka")
            glUniform1f(loc_ka, model.ka * self.ka_multiplier)

            loc_kd = glGetUniformLocation(self.program, "kd")
            glUniform1f(loc_kd, model.kd)

            loc_ks = glGetUniformLocation(self.program, "ks")
            glUniform1f(loc_ks, model.ks)

            loc_ns = glGetUniformLocation(self.program, "ns")
            glUniform1f(loc_ns, model.ns)

            # Configura a posição da luz
            if model.is_light_source:
                loc_light_pos = glGetUniformLocation(self.program, "light_position")
                glUniform3f(loc_light_pos, model.translation.x, -model.translation.y, -model.translation.z)

            # Desenha o modelo
            self.drawModel(model)


    # Alterna entre modo janela e modo tela cheia
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


    # Inicializa a janela
    def initWindow(self):
        printMessage('Initializing Window...', 'green')
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

        # Obtém o monitor principal
        monitor = glfw.get_primary_monitor()

        # Obtém a resolução da tela do monitor
        largura, altura = glfw.get_video_mode (monitor)[0]

        # Cria a janela em modo janela
        self.window = glfw.create_window(largura, altura - 30, "Trabalho 2", None, None)

        # Centraliza a janela na tela
        glfw.make_context_current(self.window)
        glfw.set_window_user_pointer(self.window, self)


    # Inicializa os shaders
    def initShaders(self):
        printMessage('Initializing Shaders...', 'green')
        self.program = glCreateProgram()
        vertex = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        # Seta o código fonte dos shaders
        glShaderSource(vertex, vertex_code)
        glShaderSource(fragment, fragment_code)

        # Compila os shaders
        glCompileShader(vertex)
        if not glGetShaderiv(vertex, GL_COMPILE_STATUS): # se não compilou
            error = glGetShaderInfoLog(vertex).decode()
            printMessage(error, "red")
            raise RuntimeError("Erro de compilacao do Vertex Shader")

        glCompileShader(fragment)
        if not glGetShaderiv(fragment, GL_COMPILE_STATUS): # se não compilou
            error = glGetShaderInfoLog(fragment).decode()
            printMessage(error, "red")
            raise RuntimeError("Erro de compilacao do Fragment Shader")

        # Vincula os shaders ao programa
        glAttachShader(self.program, vertex)
        glAttachShader(self.program, fragment)

    # Compila e constrói o programa
    def buildProgram(self):
        printMessage('Building Program...', 'green')
        # Constrói o programa
        glLinkProgram(self.program)
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            printMessage(glGetProgramInfoLog(self.program), "red")
            raise RuntimeError('Linking error')
        
        glUseProgram(self.program)

    # Inicializa as texturas
    def initTextures(self):
        printMessage('Initializing Textures...', 'green')
        glEnable(GL_TEXTURE_2D)
        qtd_texturas = 20
        self.textures = glGenTextures(qtd_texturas)

    # Mostra a janela
    def showWindow(self):
        self.polygonal_mode = False
        self.texture_filter = False
        glfw.show_window(self.window)
        glfw.set_key_callback(self.window, key_event_static)
        glEnable(GL_DEPTH_TEST) ### importante para 3D

    # Carrega a textura a partir de um arquivo
    def load_texture_from_file(self, texture_id, imagem):
        glBindTexture(GL_TEXTURE_2D, texture_id)
        # Define os filtros de textura (minificação e magnificação)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Carrega a imagem
        img = Image.open(create_model_path(imagem, 'jpg'))
        img_width = img.size[0]
        img_height = img.size[1]
        image_data = img.tobytes("raw", "RGB", 0, -1)

        # Envia a imagem para a GPU
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

    # Carrega um modelo a partir de um arquivo
    def loadModel(self, filename, initial_values = None):
        printMessage(f'Loading Model `{filename}` ...', 'yellow')

        # Carrega o modelo
        modelo = Model(self.last_index, filename, initial_values)
        self.last_index += 1
        modelData = modelo.model

        printMessage(f'Processing OBJ Model. Initial vertex count: {len(modelo.vertices)}', 'grey')

        # Processa os dados do modelo
        for face_data in modelData['faces']:
            face, texture, normal, materials = face_data

            # Adiciona os vértices do modelo
            for vert_idx in face:
                modelo.vertices.append(modelData['vertices'][vert_idx - 1])

            # Adiciona as coordenadas de textura do modelo
            for tex_idx in texture:
                if tex_idx > 0:  # Garante que não seja um valor negativo, ou seja, válido
                    modelo.texture_coords.append(modelData['texture'][tex_idx - 1])
                else:
                    modelo.texture_coords.append([0.0, 0.0])  # textura padrão

            # Adiciona as normais do modelo
            for norm_idx in normal:
                if norm_idx > 0: # Garante que não seja um valor negativo, ou seja, válido
                    modelo.normals.append(modelData['normals'][norm_idx - 1])
                else:
                    modelo.normals.append([0.0, 0.0, 0.0]) # normal padrão

        printMessage(f'Processing OBJ Model. Final vertex count: {len(modelo.vertices)}', 'grey')

        # Carrega a textura do modelo
        self.load_texture_from_file(modelo.id, filename)
        self.objects.append(modelo)

        return modelo

    # Carrega todos os buffers
    def loadAllBuffers(self):
        allVertices = []
        allTextures = []
        allNormals = []

        # Concatena todos os vértices, texturas e normais de todos os modelos
        for model in self.objects:
            allVertices += model.vertices
            allTextures += model.texture_coords
            allNormals += model.normals

        self.buffers = glGenBuffers(3)

        # Vértices
        vertices = np.zeros(len(allVertices), [("position", np.float32, 3)])
        vertices['position'] = allVertices

        # Upload data
        glBindBuffer(GL_ARRAY_BUFFER, self.buffers[0])
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)

        # Texturas
        textures = np.zeros(len(allTextures), [("position", np.float32, 2)]) # duas coordenadas
        textures['position'] = allTextures

        # Upload data
        glBindBuffer(GL_ARRAY_BUFFER, self.buffers[1])
        glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
        stride = textures.strides[0]
        offset = ctypes.c_void_p(0)
        loc_texture_coord = glGetAttribLocation(self.program, "texture_coord")
        glEnableVertexAttribArray(loc_texture_coord)
        glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)

        # Normais
        normals = np.zeros(len(allNormals), [("position", np.float32, 3)]) # três coordenadas
        normals['position'] = allNormals

        # Upload data
        glBindBuffer(GL_ARRAY_BUFFER, self.buffers[2])
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        stride = normals.strides[0]
        offset = ctypes.c_void_p(0)
        loc_normals = glGetAttribLocation(self.program, "normals")
        glEnableVertexAttribArray(loc_normals)
        glVertexAttribPointer(loc_normals, 3, GL_FLOAT, False, stride, offset)

    # Desenha um modelo
    def drawModel(self, model):
        glBindTexture(GL_TEXTURE_2D, model.id)

        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, self.vCount, len(model.vertices))

        # atualiza o contador de vértices, se é o último modelo, zera
        if model.id == self.objects[-1].id:
            self.vCount = 0
        else:
            self.vCount += len(model.vertices)

        edges = [
            (0, 1), (1, 3), (3, 2), (2, 0),  # Borda superior
            (4, 5), (5, 7), (7, 6), (6, 4),  # Borda inferior
            (0, 4), (1, 5), (2, 6), (3, 7)   # Bordas laterais (conectam superior e inferior)
        ]

        # Desenha a bounding box do objeto
        if self.drawBB:
            glBegin(GL_LINES)
            for edge in edges:
                for vertex_index in edge:
                    vertex = model.bounding_box[vertex_index]  # vertex é glm.vec4
                    glVertex3f(vertex.x, vertex.y, vertex.z)  # Usando x, y, z componentes
            glEnd()

    # Evento de teclado
    def keyEvent(self, window, key, scancode, action, mods):
        # Alterna entre modo poligonal e modo preenchido
        if key == glfw.KEY_P and action == glfw.PRESS:
            self.polygonal_mode = not self.polygonal_mode
            if self.polygonal_mode:
                printMessage("Polygonal mode: GL_LINE", 'blue')
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            else:
                printMessage("Polygonal mode: GL_FILL", 'blue')
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            return

        # Alterna entre filtro de textura linear e nearest
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

        translationSpeed = 0.05 # Velocidade de translação da câmera

        # Movimenta a câmera
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

        # Altera a intensidade da luz ambiente
        if key == glfw.KEY_J:
            if self.ka_multiplier > 0:
                self.ka_multiplier -= 0.1
        if key == glfw.KEY_K:
            if self.ka_multiplier < 1:
                self.ka_multiplier += 0.1

        # Movimenta a luz
        lightObj = self.objects[-1]

        if key == glfw.KEY_UP:
            lightObj.translation.y += translationSpeed
        if key == glfw.KEY_DOWN:
            lightObj.translation.y -= translationSpeed
        if key == glfw.KEY_LEFT:
            lightObj.translation.x -= translationSpeed
        if key == glfw.KEY_RIGHT:
            lightObj.translation.x += translationSpeed
        if key == glfw.KEY_M:
            lightObj.translation.z += translationSpeed
        if key == glfw.KEY_N:
            lightObj.translation.z -= translationSpeed

        lightObj.haveMoved = True