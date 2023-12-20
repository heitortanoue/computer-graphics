import os
import glm
import math
from termcolor import colored

# Leitura de arquivos de shader
def readShaderFile(filename):
    """Reads a shader file and returns the file contents"""
    path = create_path('shaders/' + filename)
    with open(path, 'r') as file:
        return file.read()

# Retorna as proporções do modelo
def getModelProportions(modelo):
    x_max = -math.inf
    x_min = math.inf
    y_max = -math.inf
    y_min = math.inf
    z_max = -math.inf
    z_min = math.inf

    # Percorre todos os vértices do modelo
    for obj in modelo.model['vertices']:
        # obj str to float
        obj[0] = float(obj[0])
        obj[1] = float(obj[1])
        obj[2] = float(obj[2])

        # Verifica se o vértice é o maior ou menor em cada eixo
        if obj[0] < x_min:
            x_min = obj[0]
        elif obj[0] > x_max:
            x_max = obj[0]

        if obj[1] < y_min:
            y_min = obj[1]
        elif obj[1] > y_max:
            y_max = obj[1]

        if obj[2] < z_min:
            z_min = obj[2]
        elif obj[2] > z_max:
            z_max = obj[2]

    # Calcula os valores médios de cada eixo
    x_med = (x_max + x_min)/2
    y_med = (y_max + y_min)/2
    z_med = (z_max + z_min)/2

    # Salva os valores de limite
    modelo.bounds = {
        'x_max': x_max,
        'x_min': x_min,
        'y_max': y_max,
        'y_min': y_min,
        'z_max': z_max,
        'z_min': z_min
    }

    averageVector = glm.vec3(x_med, y_med, z_med)
    width = x_max - x_min
    height = y_max - y_min
    depth = z_max - z_min

    # Retorna um dicionário com os valores
    return {
        "center": averageVector,
        "height": height,
        "width": width,
        "depth": depth,
    }

# Cria o caminho para o arquivo
def create_path(path):
    # Pegar o diretório do script atual
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Pegar o diretório pai do script
    parent_directory = os.path.dirname(script_directory)
    # Junta o diretório pai com "objs/model/model.obj"
    full_path = os.path.join(parent_directory, path)
    return full_path

# Cria o caminho para o arquivo do modelo
def create_model_path(model, extension):
    return create_path('objs/' + model + '/' + model + '.' + extension)

# Carrega o modelo a partir do arquivo
def load_model_from_file(filename):
    """Loads a Wavefront OBJ file."""
    # Inicializa as listas de vértices, texturas, faces e normais
    vertices = []
    texture_coords = []
    faces = []
    normals = []

    material = None

    # Abre o arquivo e percorre todas as linhas
    for line in open(filename, "r"):
        if line.startswith('#'): continue  # Ignora comentários

        values = line.split() # Divide a linha em valores
        if not values: continue

        # Verifica o tipo de valor
        if values[0] == 'v': # Vertices
            vertices.append(list(map(float, values[1:4])))

        elif values[0] == 'vt': # Texturas
            texture_coords.append(list(map(float, values[1:3])))

        elif values[0] == 'vn': # Normais
            normals.append(list(map(float, values[1:4])))

        elif values[0] in ('usemtl', 'usemat'): # Material
            material = values[1]

        elif values[0] == 'f':
            # Lidar com faces com mais de 3 vértices
            verts = values[1:]
            v0 = verts[0]

            # Processa os vértices
            for i in range(1, len(verts) - 1):
                v1 = verts[i]
                v2 = verts[i + 1]
                face = [int(v0.split('/')[0]), int(v1.split('/')[0]), int(v2.split('/')[0])]

                # Processa texturas se disponíveis
                if len(v0.split('/')) > 1 and v0.split('/')[1]:
                    texture = [int(v0.split('/')[1]), int(v1.split('/')[1]), int(v2.split('/')[1])]
                else:
                    texture = [0, 0, 0]  # 0s representam a falta de textura

                # Processa normais se disponíveis
                if len(v0.split('/')) > 2 and v0.split('/')[2]:
                    normal = [int(v0.split('/')[2]), int(v1.split('/')[2]), int(v2.split('/')[2])]
                else:
                    normal = [0, 0, 0] # 0s representam a falta de normais

                faces.append((face, texture, normal, material)) # Adiciona a face à lista de faces

    # Retorna um dicionário com os valores
    return {'vertices': vertices, 'texture': texture_coords, 'normals': normals, 'faces': faces}

def printMessage(message, color=None):
    if color is None:
        print(message)
    else:
        print(colored(message, color))
