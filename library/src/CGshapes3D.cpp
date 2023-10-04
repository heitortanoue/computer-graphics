#include "CGshapes3D.h"

CGcube::~CGcube()
{
}

Vec3* CGcube::getVerticesMatrix()
{
    Vec3* verticesMatrix = new Vec3[24];
    auto vertices = getVertices();

    float order[24] = {
        0, 1, 3, 2,
        0, 1, 7, 6,
        2, 3, 5, 4,
        0, 3, 7, 4,
        1, 2, 6, 5,
        4, 5, 7, 6
    };

    for (int i = 0; i < 24; i++) {
        verticesMatrix[i] = vertices[order[i]];
    }

    return verticesMatrix;
}

void CGcube::draw(GLuint program)
{

    // glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    GLint loc_color = glGetUniformLocation(program, "color");

    glUniform4f(loc_color, 1.0, 0.0, 0.0, 1.0); // ### vermelho
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

    glUniform4f(loc_color, 0.0, 0.0, 1.0, 1.0); // ### azul
    glDrawArrays(GL_TRIANGLE_STRIP, 4, 4);

    glUniform4f(loc_color, 0.0, 1.0, 0.0, 1.0); // ### verde
    glDrawArrays(GL_TRIANGLE_STRIP, 8, 4);

    glUniform4f(loc_color, 1.0, 1.0, 0.0, 1.0); // ### amarela
    glDrawArrays(GL_TRIANGLE_STRIP, 12, 4);

    glUniform4f(loc_color, 0.5, 0.5, 0.5, 1.0); // ### cinza
    glDrawArrays(GL_TRIANGLE_STRIP, 16, 4);

    glUniform4f(loc_color, 0.5, 0.0, 0.0, 1.0); // ### marrom
    glDrawArrays(GL_TRIANGLE_STRIP, 20, 4);
}


// ====================================
// PYRAMID

CGpyramid::~CGpyramid()
{
}

Vec3 *CGpyramid::getVerticesMatrix()
{
    Vec3 *verticesMatrix = new Vec3[this->getVerticesSize()];
    auto vertices = getVertices();

    // Defina os índices dos vértices para as faces da pirâmide
    int faceIndices[this->getVerticesSize()] = {
        0, 1, 2, // Base
        0, 2, 3,
        0, 3, 4,
        0, 4, 1,
        1, 2, 4, 3
    };

    for (int i = 0; i < 16; i++)
    {
        verticesMatrix[i] = vertices[faceIndices[i]];
    }

    return verticesMatrix;
}

void CGpyramid::draw(GLuint program)
{
    GLint loc_color = glGetUniformLocation(program, "color");

    glUniform4f(loc_color, 1.0, 0.0, 0.0, 1.0); // ### vermelho
    glDrawArrays(GL_TRIANGLES, 0, 3);           // Desenhe a primeira face da base

    glUniform4f(loc_color, 0.0, 0.0, 1.0, 1.0); // ### azul
    glDrawArrays(GL_TRIANGLES, 3, 3);           // Desenhe a segunda face da base

    glUniform4f(loc_color, 0.0, 1.0, 0.0, 1.0); // ### verde
    glDrawArrays(GL_TRIANGLES, 6, 3);           // Desenhe a terceira face da base

    glUniform4f(loc_color, 1.0, 1.0, 0.0, 1.0); // ### amarela
    glDrawArrays(GL_TRIANGLES, 9, 3);           // Desenhe a quarta face da base

    glUniform4f(loc_color, 0.5, 0.5, 0.5, 1.0); // ### cinza
    glDrawArrays(GL_TRIANGLE_STRIP, 12, 4);          // Desenhe a face superior
}


// ====================================
// SPHERE

CGsphere::~CGsphere()
{
}

Vec3 *CGsphere::getVerticesMatrix()
{
    Vec3 *verticesMatrix = new Vec3[sphereVertices.size()];
    for (size_t i = 0; i < sphereVertices.size(); ++i)
    {
        verticesMatrix[i] = sphereVertices[i];
    }
    return verticesMatrix;
}

void CGsphere::draw(GLuint program)
{
    // Recupere a localização da variável de cor do programa GLSL
    GLint loc_color = glGetUniformLocation(program, "color");

    // Defina a cor da esfera (por exemplo, vermelho)
    glUniform4f(loc_color, 1.0, 0.0, 0.0, 1.0);

    // Desenhe a esfera usando triângulos (GL_TRIANGLES)
    glDrawArrays(GL_TRIANGLES, 0, sphereVertices.size());
}