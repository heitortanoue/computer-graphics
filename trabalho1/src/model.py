from src.functions import *
import glm

class Model:
    def __init__(self, path):
        self.model = load_model_from_file(create_model_path(path, 'obj'))
        self.mat_transform = glm.mat4(1)
        self.buffer = None

        self.vertices = []
        self.texture_coords = []

        self.scale = .1
        self.rotation = glm.vec3(0,0,0)
        avgPos = getAveragePosition(self.model)
        self.translation = glm.vec3(-avgPos.x, -avgPos.y, -avgPos.z)
        self.mat_transform = glm.translate(self.mat_transform, self.translation)

    def applyTransformations(self, scale, rotation, translation):
        self.scale = scale
        self.rotation = rotation
        self.translation = translation

        self.mat_transform = glm.mat4(1)
        self.mat_transform = glm.translate(self.mat_transform, translation)
        self.mat_transform = glm.rotate(self.mat_transform, rotation.x, glm.vec3(1, 0, 0))
        self.mat_transform = glm.rotate(self.mat_transform, rotation.y, glm.vec3(0, 1, 0))
        self.mat_transform = glm.rotate(self.mat_transform, rotation.z, glm.vec3(0, 0, 1))
        self.mat_transform = glm.scale(self.mat_transform, glm.vec3(scale, scale, scale))
