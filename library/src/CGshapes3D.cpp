#include "CGshapes3D.h"
#include <cmath>

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
// CYLINDER

CGcylinder::~CGcylinder()
{
}

Vec3 *CGcylinder::getVerticesMatrix()
{
}

void CGcylinder::draw(GLuint program)
{
    // Implementation of draw
    GLint loc_color = glGetUniformLocation(program, "color");
    glUniform4f(loc_color, 1.0, 0.0, 0.0, 1.0); // ### vermelho

    // Desenhe a base
    glDrawArrays(GL_TRIANGLE_FAN, 0, this->numSegments + 1);
    glDrawArrays(GL_TRIANGLE_FAN, this->numSegments + 1, this->numSegments + 1);
    glDrawArrays(GL_TRIANGLE_STRIP, 2 * (this->numSegments + 1), this->numSegments * 2 * 3);
}
