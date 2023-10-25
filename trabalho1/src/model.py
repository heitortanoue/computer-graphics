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


        self.scale = .15
        self.rotation = glm.vec3(0,0,0)
        self.translation = glm.vec3(0,0,0)

        self.mat_transform = glm.scale(self.mat_transform, glm.vec3(self.scale, self.scale, self.scale))
        self.mat_transform = glm.translate( self.mat_transform, -getAveragePosition(self) )


        self.scaleInc = 1
        self.rotationInc = glm.vec3(0,0,0)
        self.translationInc = glm.vec3(0,0,0)

    def applyTransformations(self):
        newMat = glm.mat4(1)
        newMat = glm.translate(newMat, self.translationInc)
        newMat = glm.rotate(newMat, self.rotationInc.x, glm.vec3(1, 0, 0))
        newMat = glm.rotate(newMat, self.rotationInc.y, glm.vec3(0, 1, 0))
        newMat = glm.rotate(newMat, self.rotationInc.z, glm.vec3(0, 0, 1))
        newMat = glm.scale(newMat, glm.vec3(self.scaleInc, self.scaleInc, self.scaleInc))

        if not self.violateBounds():
            self.mat_transform = newMat * self.mat_transform

            self.scale *= self.scaleInc
            self.rotation += self.rotationInc
            self.translation += self.translationInc

        self.translationInc = glm.vec3(0,0,0)
        self.rotationInc = glm.vec3(0,0,0)
        self.scaleInc = 1

        # print(self.mat_transform)

    def violateBounds(self):
        rightPos = (self.bounds['x_max'] * self.scale) + self.translation.x
        leftPos = (self.bounds['x_min'] * self.scale) + self.translation.x
        topPos = (self.bounds['y_max'] * self.scale) + self.translation.y
        bottomPos = (self.bounds['y_min'] * self.scale) + self.translation.y

        print("bounds: ", leftPos, rightPos, topPos, bottomPos)

        if rightPos > 1 or leftPos < -1 or topPos > 1 or bottomPos < -1:
            return True
        else:
            return False