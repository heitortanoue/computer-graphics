import os
import glm
import math
from termcolor import colored

def getModelProportions(modelo):
    x_max = -math.inf
    x_min = math.inf
    y_max = -math.inf
    y_min = math.inf
    z_max = -math.inf
    z_min = math.inf

    for obj in modelo.model['vertices']:
        # obj str to float
        obj[0] = float(obj[0])
        obj[1] = float(obj[1])
        obj[2] = float(obj[2])

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

    x_med = (x_max + x_min)/2
    y_med = (y_max + y_min)/2
    z_med = (z_max + z_min)/2

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

    return {
        "center": averageVector,
        "height": height,
        "width": width,
        "depth": depth,
    }

def create_model_path(model, extension):
    # Get the current directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the parent directory (i.e., go up one level)
    parent_directory = os.path.dirname(script_directory)
    # Join the parent directory with "objs/model/model.obj"
    full_path = os.path.join(parent_directory, "objs", model, model + '.' + extension)
    return full_path

def load_model_from_file(filename):
    vertices = []
    normals_coords = []
    texture_coords = []
    faces = []

    material = None

    # abre o arquivo obj para leitura
    for line in open(filename, "r"): ## para cada linha do arquivo .obj
        if line.startswith('#'): continue ## ignora comentarios
        values = line.split() # quebra a linha por espaço
        if not values: continue


        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(list(map(float, values[1:4])))

        ### recuperando vertices
        if values[0] == 'vn':
            normals_coords.append(list(map(float, values[1:4])))

        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(list(map(float, values[1:3])))

        ### recuperando faces 
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            verts = values[1:]
            v0 = verts[0]
            for i in range(1, len(verts) - 1):
                v1 = verts[i]
                v2 = verts[i + 1]
                face = [int(v0.split('/')[0]), int(v1.split('/')[0]), int(v2.split('/')[0])]
                
                if len(v0.split('/')) > 1 and v0.split('/')[1]:
                    texture = [int(v0.split('/')[1]), int(v1.split('/')[1]), int(v2.split('/')[1])]
                else:
                    texture = [0, 0, 0]
                
                if len(v0.split('/')) > 2 and v0.split('/')[2]:
                    normals = [int(v0.split('/')[2]), int(v1.split('/')[2]), int(v2.split('/')[2])]
                else:
                    normals = [0, 0, 0]

            faces.append((face, texture, normals, material))


    return {'vertices': vertices, 'texture': texture_coords, 'normals': normals_coords, 'faces': faces}

def printMessage(message, color=None):
    if color is None:
        print(message)
    else:
        print(colored(message, color))

