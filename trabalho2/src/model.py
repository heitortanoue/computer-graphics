from src.functions import *
import glm

class Model:
    def __init__(self, id, path, initial_values=None):
        if initial_values is None:
            initial_values = {}

        self.id = id
        self.name = path
        self.model = load_model_from_file(create_model_path(path, 'obj'))  # Assuming this is a valid OBJ path
        self.mat_transform = glm.mat4(1)
        self.buffer = None

        self.vertices = []
        self.texture_coords = []
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

    def applyTransformations(self):
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

        # Verifica se viola os limites
        if not self.violateBounds(newMat):
            self.mat_transform = newMat
            return


    def violateBounds(self, mat_transformation):
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
