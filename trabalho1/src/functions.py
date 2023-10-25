import os
import glm
import math

def getAveragePosition(modelo):
    x_max = -math.inf
    x_min = math.inf
    y_max = -math.inf
    y_min = math.inf

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

    x_med = (x_max + x_min)/2
    y_med = (y_max + y_min)/2

    modelo.bounds = {
        'x_max': x_med,
        'x_min': -x_med,
        'y_max': y_med,
        'y_min': -y_med
    }

    averageVector = glm.vec3(x_med, y_med, 0)

    return averageVector

def create_model_path(model, extension):
    # Get the current directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the parent directory (i.e., go up one level)
    parent_directory = os.path.dirname(script_directory)
    # Join the parent directory with "objs/model/model.obj"
    full_path = os.path.join(parent_directory, "objs", model, model + '.' + extension)
    return full_path

def load_model_from_file(model):
    """Loads a Wavefront OBJ file. """
    vertices = []
    texture_coords = []
    faces = []

    material = None

    # abre o arquivo obj para leitura
    for line in open(model, "r"): ## para cada linha do arquivo .obj
        if line.startswith('#'): continue ## ignora comentarios
        values = line.split() # quebra a linha por espaço
        if not values: continue


        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(values[1:4])


        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces

    return model
