import numpy as np
import glm

from src.model import Model

min_distance = .2
class Camera:
    def __init__(self, position: glm.vec3, rotation: glm.vec3, width = 1600, height = 900):
        self.position = position
        self.rotation = rotation
        self.width = width
        self.height = height

        self.models_to_check = []

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
        ds = self.direction_XZ * distance
        if self.violate_boundaries(ds):
            return
        # Move a câmera para frente na direção em que está olhando
        self.position += ds

    def move_backward(self, distance):
        ds = -self.direction_XZ * distance
        if self.violate_boundaries(ds):
            return
        # Move a câmera para trás na direção oposta à que está olhando
        self.position += ds

    def move_right(self, distance):
        ds = self.right * distance
        if self.violate_boundaries(ds):
            return

        # Move a câmera para a direita
        self.position += ds

    def move_left(self, distance):
        ds = -self.right * distance
        if self.violate_boundaries(ds):
            return

        # Move a câmera para a esquerda
        self.position += ds

    def set_boundaries(self, model: Model):
        # Define os limites da câmera com base no modelo
        self.boundaries = model.get_bounds()

    def violate_boundaries(self, ds: glm.vec3, check_models=True):
        # Verifica se a câmera viola os limites do modelo
        # ds é o vetor de deslocamento
        new_position = self.position + ds

        if new_position.x < self.boundaries['min_x'] + min_distance or new_position.x > self.boundaries['max_x'] - min_distance:
            return True
        if new_position.y < self.boundaries['min_y'] + min_distance or new_position.y > self.boundaries['max_y'] - min_distance:
            return True
        if new_position.z < self.boundaries['min_z'] + min_distance or new_position.z > self.boundaries['max_z'] - min_distance:
            return True

        if check_models:
            remainder_translation = self.check_model_collision(new_position)
            if remainder_translation:
                self.position += remainder_translation
                return True
        return False

    def check_model_collision(self, new_position):
        # Verifica se a câmera colide com algum dos modelos
        for model in self.models_to_check:
            if model.check_collision(new_position):
                remainder_translation = model.get_remainder_translation(new_position)
                return remainder_translation
        return False

    def add_model_to_check(self, model: Model):
        self.models_to_check.append(model)
