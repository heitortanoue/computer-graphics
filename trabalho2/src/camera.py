import numpy as np
import glm

class Camera:
    def __init__(self, position: glm.vec3, rotation: glm.vec3, width = 1600, height = 900):
        self.position = position
        self.rotation = rotation
        self.width = width
        self.height = height

    @property
    def direction(self):
        # Retorna a direção atual da câmera com base na sua rotação
        return glm.normalize(glm.vec3(
            np.cos(self.rotation.y) * np.cos(self.rotation.x),
            np.sin(self.rotation.x),
            np.sin(self.rotation.y) * np.cos(self.rotation.x)
        ))

    @property
    def direction_XZ(self):
        return glm.normalize(glm.vec3(
            self.direction.x,
            0,
            self.direction.z
        ))

    @property
    def right(self):
        # Calcula e retorna o vetor "para a direita" da câmera
        return glm.normalize(glm.cross(self.direction_XZ, glm.vec3(0, 1, 0)))

    def view_matrix(self):
        # Calcular o vetor lookat
        lookat = self.position + self.direction

        # Calcular a matriz de visualização
        mat_view = glm.lookAt(self.position, lookat, glm.vec3(0, 1, 0))
        return mat_view

    def projection_matrix(self):
        near = 0.1
        far = 100
        fov = 50

        # Calcular a matriz de projeção
        mat_projection = glm.perspective(glm.radians(fov), self.width / self.height, near, far)
        return mat_projection

    def set_width_height(self, width, height):
        self.width = width
        self.height = height

    def move_forward(self, distance):
        # Move a câmera para frente na direção em que está olhando
        self.position += self.direction_XZ * distance

    def move_backward(self, distance):
        # Move a câmera para trás na direção oposta à que está olhando
        self.position -= self.direction_XZ * distance

    def move_right(self, distance):
        # Move a câmera para a direita
        self.position += self.right * distance

    def move_left(self, distance):
        # Move a câmera para a esquerda
        self.position -= self.right * distance
