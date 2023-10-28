from src.functions import *
import glm

class Model:
    def __init__(self, path):
        self.model = load_model_from_file(create_model_path(path, 'obj'))
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

        self.scale = .15
        self.rotation = glm.vec3(0,0,0)
        self.translation = glm.vec3(0,0,0)

    def applyTransformations(self):
        newMat = glm.mat4(1)

        newMat = glm.translate(newMat, -self.center * self.scale)
        newMat = glm.translate(newMat, self.translation)
        newMat = glm.scale(newMat, glm.vec3(self.scale, self.scale, self.scale))

        newMat = glm.rotate(newMat, self.rotation.x, glm.vec3(1, 0, 0))
        newMat = glm.rotate(newMat, self.rotation.y, glm.vec3(0, 1, 0))
        newMat = glm.rotate(newMat, self.rotation.z, glm.vec3(0, 0, 1))

        if not self.violateBounds():
            self.mat_transform = newMat
            return


    def violateBounds(self):
        scaled_width = self.width * self.scale
        scaled_height = self.height * self.scale
        scaled_depth = self.depth * self.scale

        maxScale = max(scaled_width, scaled_height, scaled_depth)

        leftPos = self.translation.x - scaled_width/2
        rightPos = self.translation.x + scaled_width/2
        topPos = self.translation.y + scaled_height/2
        bottomPos = self.translation.y - scaled_height/2

        remainderTranslation = glm.vec3(0,0,0)

        # saiu da tela pelos lados
        if rightPos >= 1:
            remainderTranslation.x = 1 - rightPos
        elif leftPos <= -1:
            remainderTranslation.x = -1 - leftPos

        # saiu da tela por cima ou por baixo
        if topPos >= 1:
            remainderTranslation.y = 1 - topPos
        elif bottomPos <= -1:
            remainderTranslation.y = -1 - bottomPos

        # passou da escala máxima
        if maxScale > 2:
            remainderTranslation.x = 0
            remainderTranslation.y = 0

            if maxScale == scaled_width:
                self.scale = 2/self.width
            elif maxScale == scaled_height:
                self.scale = 2/self.height
            elif maxScale == scaled_depth:
                self.scale = 2/self.depth

        if remainderTranslation.x == 0 and remainderTranslation.y == 0:
            return False

        self.translation += remainderTranslation
