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
    int faceIndices[this->getVerticesSize()];
    int i = 0;

    for (; i < numSegments; i++)
    {
        faceIndices[3*i] = 0; // origem de cima
        faceIndices[3*i + 1] = i + 1;
        if (i == numSegments - 1){
            faceIndices[3*i + 2] = 1;
            continue;
        }
        else{
            faceIndices[3*i + 2] = i + 2;
        }
    }

    for (; i < (2 * numSegments); i++)
    {
        faceIndices[3*i] = numSegments + 1; //origem de baixo
        faceIndices[3*i + 1] = i + 2;
        if (i == ((2 * numSegments) - 1)){
            faceIndices[3*i + 2] = numSegments + 2;
            continue;
        }
        else{
            faceIndices[3*i + 2] = i + 3;
        }
    }
    
    i = 3*i;
    for (int j = 1; j < numSegments + 1; j++, i=i+2)
    {
        faceIndices[i] = j;
        faceIndices[i + 1] = j + numSegments + 1;
        std::cout << faceIndices[i] << " " << faceIndices[i+1] << " ";
    }

    faceIndices[i] = 1;
    faceIndices[i+1] = numSegments + 2;
    
    Vec3 *verticesMatrix = new Vec3[this->getVerticesSize()];
    auto vertices = getVertices();

    for (int i = 0; i < this->getVerticesSize(); i++)
    {
        verticesMatrix[i] = vertices[faceIndices[i]];
        std::cout << i << " (" << verticesMatrix[i].x << "; " << verticesMatrix[i].y << "; " << verticesMatrix[i].z << ")" << std::endl;
    }

    return verticesMatrix;
}

void CGcylinder::draw(GLuint program)
{
    // Implementation of draw
    GLint loc_color = glGetUniformLocation(program, "color");
    glUniform4f(loc_color, 1.0, 0.0, 0.0, 1.0); // ### vermelho

    // Desenhe a base cima
    for (int i = 0; i < numSegments; i++)
    {
        glDrawArrays(GL_TRIANGLES, i * 3, 3);
    }

    glUniform4f(loc_color, 0.0, 0.0, 1.0, 1.0); // ### azul

    // Desenhe a base baixo
    for (int i = 0; i < numSegments; i++){
        glDrawArrays(GL_TRIANGLES, (numSegments + i) * 3, 3);
    }

    glUniform4f(loc_color, 0.0, 1.0, 0.0, 1.0); // ### verde

    // Desenhe a lateral
    // for (int i = 0; i < (2 * numSegments); i++)
    // {
        glDrawArrays(GL_TRIANGLE_STRIP, (6 * numSegments), (2 * numSegments + 2));
    //}
}
