from src.functions import *
import glm

min_distance = .05
class Model:
    def __init__(self, id, path, initial_values=None):
        if initial_values is None:
            initial_values = {}

        self.id = id
        self.name = path
        self.model = load_model_from_file(create_model_path(path, 'obj'))  # Assuming this is a valid OBJ path
        self.mat_transform = glm.mat4(1)
        self.buffer = None
        self.haveMoved = True # Começa como True para que o objeto seja renderizado na primeira vez

        self.vertices = []
        self.texture_coords = []
        self.normals = []
        self.bounds = {}

        proportions = getModelProportions(self)
        self.center = proportions['center']
        self.width = proportions['width']
        self.height = proportions['height']
        self.depth = proportions['depth']

        # Default values
        self.scale = initial_values.get("scale", 1)
        self.rotation = glm.vec3(*initial_values.get("rotation", [0, 0, 0]))
        self.translation = glm.vec3(*initial_values.get("translation", [0, 0, 0]))

        lightInitialValues = initial_values.get("light", {})

        self.ka = lightInitialValues.get("ambient", 0.2)
        self.kd = lightInitialValues.get("diffuse", 1)
        self.ks = lightInitialValues.get("specular", 1)
        self.ns = lightInitialValues.get("shininess", 32)
        self.is_light_source = lightInitialValues.get("is_light_source", False)

        self.applyTransformations() # aplica valores iniciais

        # Set bounding box
        self.get_bounds()

    def applyTransformations(self):
        if not self.haveMoved:
            return

        newMat = glm.mat4(1)

        # Primeiro, translada o objeto para a origem
        newMat = glm.translate(newMat, self.translation - self.center * self.scale)

        # Aplica as rotações em torno da origem (que agora é o centro do objeto)
        newMat = glm.rotate(newMat, self.rotation.x, glm.vec3(1, 0, 0))
        newMat = glm.rotate(newMat, self.rotation.y, glm.vec3(0, 1, 0))
        newMat = glm.rotate(newMat, self.rotation.z, glm.vec3(0, 0, 1))

        # Aplica a escala
        newMat = glm.scale(newMat, glm.vec3(self.scale, self.scale, self.scale))

        # Translada de volta para a posição original
        newMat = glm.translate(newMat, self.center * self.scale)

        self.mat_transform = newMat
        self.get_bounds()
        self.haveMoved = False

        # Verifica se viola os limites
        # if not self.violateBounds(newMat):
        #     self.mat_transform = newMat
        #     return

    def get_bounds(self, mat_transformation=None):
        if not mat_transformation:
            mat_transformation = self.mat_transform

        # Define the eight corners of the bounding box based on the unscaled and unrotated object
        bbox_corners = [
            glm.vec3(self.bounds['x_min'], self.bounds['y_min'], self.bounds['z_min']),  # bottom-front-left corner
            glm.vec3(self.bounds['x_max'], self.bounds['y_min'], self.bounds['z_min']),  # bottom-front-right corner
            glm.vec3(self.bounds['x_min'], self.bounds['y_max'], self.bounds['z_min']),  # top-front-left corner
            glm.vec3(self.bounds['x_max'], self.bounds['y_max'], self.bounds['z_min']),  # top-front-right corner
            glm.vec3(self.bounds['x_min'], self.bounds['y_min'], self.bounds['z_max']),  # bottom-back-left corner
            glm.vec3(self.bounds['x_max'], self.bounds['y_min'], self.bounds['z_max']),  # bottom-back-right corner
            glm.vec3(self.bounds['x_min'], self.bounds['y_max'], self.bounds['z_max']),  # top-back-left corner
            glm.vec3(self.bounds['x_max'], self.bounds['y_max'], self.bounds['z_max']),  # top-back-right corner
        ]

        # Transform the bounding box corners
        self.bounding_box = [glm.vec4(corner, 1) for corner in bbox_corners]
        bounding_box = [mat_transformation * corner for corner in self.bounding_box]

        # Find min and max x, y, and z from the transformed bounding box corners
        min_x = min(corner.x for corner in bounding_box)
        max_x = max(corner.x for corner in bounding_box)
        min_y = min(corner.y for corner in bounding_box)
        max_y = max(corner.y for corner in bounding_box)
        min_z = min(corner.z for corner in bounding_box)
        max_z = max(corner.z for corner in bounding_box)

        return {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y,
            'min_z': min_z,
            'max_z': max_z
        }

    def check_collision(self, objPosition: glm.vec3):
        # Verifica se o objeto colide com o objeto passado
        # objPosition é a posição do objeto
        # Retorna True se houver colisão, False caso contrário

        # Verifica se o objeto está dentro dos limites do modelo usando self.bounding_box
        # Se estiver, retorna True
        # Se não estiver, retorna False
        bounds = self.get_bounds()
        min_x = bounds['min_x']
        max_x = bounds['max_x']
        min_y = bounds['min_y']
        max_y = bounds['max_y']
        min_z = bounds['min_z']
        max_z = bounds['max_z']

        condition_x_with_min_distance = min_x - min_distance <= objPosition.x <= max_x + min_distance
        condition_y_with_min_distance = min_y - min_distance <= objPosition.y <= max_y + min_distance
        condition_z_with_min_distance = min_z - min_distance <= objPosition.z <= max_z + min_distance

        if condition_x_with_min_distance and condition_y_with_min_distance and condition_z_with_min_distance:
            return True
        return False

    def get_remainder_translation(self, new_position):
        # Retorna o vetor de translação que falta para o objeto não colidir mais com o modelo
        # new_position é a nova posição do objeto
        # Retorna um vetor de translação
        bounds = self.get_bounds()
        min_x = bounds['min_x']
        max_x = bounds['max_x']
        min_y = bounds['min_y']
        max_y = bounds['max_y']
        min_z = bounds['min_z']
        max_z = bounds['max_z']

        remainder_translation = glm.vec3(0.0, 0.0, 0.0)

        if new_position.x < min_x:
            remainder_translation.x = min_x - new_position.x - min_distance
        elif new_position.x > max_x:
            remainder_translation.x = max_x - new_position.x + min_distance

        if new_position.y < min_y:
            remainder_translation.y = min_y - new_position.y - min_distance
        elif new_position.y > max_y:
            remainder_translation.y = max_y - new_position.y + min_distance

        if new_position.z < min_z:
            remainder_translation.z = min_z - new_position.z - min_distance
        elif new_position.z > max_z:
            remainder_translation.z = max_z - new_position.z + min_distance

        return remainder_translation

    def violateBounds(self, mat_transformation):
        min_x, max_x, min_y, max_y, min_z, max_z = self.get_bounds(mat_transformation)

        # Initialize the remainder translation to zero
        remainder_translation = glm.vec3(0.0, 0.0, 0.0)

        # Check boundaries and adjust translation if necessary
        if max_x > 1.0:
            remainder_translation.x = 1.0 - max_x
        elif min_x < -1.0:
            remainder_translation.x = -1.0 - min_x
        if max_y > 1.0:
            remainder_translation.y = 1.0 - max_y
        elif min_y < -1.0:
            remainder_translation.y = -1.0 - min_y
        if max_z > 1.0:
            remainder_translation.z = 1.0 - max_z
        elif min_z < -1.0:
            remainder_translation.z = -1.0 - min_z

        # Apply the translation remainder if needed
        if glm.length(remainder_translation) > 0:
            self.translation += remainder_translation
            return True

        return False
