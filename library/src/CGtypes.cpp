#include <cmath>

#include "CGtypes.h"
#include <iostream>
#include <iomanip>

void TransformationMatrix::translate(Vec2 tl)
{
    translation.x += tl.x;
    translation.y += tl.y;
    updateMatrix();
}

void TransformationMatrix::rotate(float angle)
{
    rotation.z += angle;
    updateMatrix();
}

void TransformationMatrix::rotate(char axis, float angle)
{
    switch (axis)
    {
    case 'x':
        rotation.x += angle;
        break;
    case 'y':
        rotation.y += angle;
        break;
    case 'z':
        rotation.z += angle;
        break;
    default:
        break;
    }
    updateMatrix();
}

void TransformationMatrix::scaleTransform2D(float scaleFactor)
{
    scale2D += scaleFactor;
    scale3D = 1.0f;

    updateMatrix();
}

void TransformationMatrix::scaleTransform3D(float scaleFactor)
{
    scale3D += scaleFactor;
    scale2D = 1.0f;

    updateMatrix();
}

void TransformationMatrix::multiply(TransformationMatrix &other)
{
    translation.x += other.translation.x;
    translation.y += other.translation.y;
    translation.z += other.translation.z;

    rotation.x += other.rotation.x;
    rotation.y += other.rotation.y;
    rotation.z += other.rotation.z;

    scale3D += other.scale3D;
    scale2D += other.scale2D;

    updateMatrix();
}

Vec2 TransformationMatrix::getTranslation2D()
{
    return Vec2({translation.x, translation.y});
}

Vec3 TransformationMatrix::getTranslation3D()
{
    return Vec3({translation.x, translation.y, translation.z});
}

float TransformationMatrix::getRotation2D()
{
    return rotation.z;
}

Vec3 TransformationMatrix::getRotation3D()
{
    return Vec3({rotation.x, rotation.y, rotation.z});
}

float TransformationMatrix::getScale()
{
    if (scale2D != 1.0f)
        return scale2D;
    else
        return scale3D;
}

float *TransformationMatrix::getMatrix()
{
    return transformationMatrix;
}

void TransformationMatrix::addVelocity(Vec2 vel)
{
    velocity.x += vel.x;
    velocity.y += vel.y;
}

void TransformationMatrix::addVelocity(Vec3 vel)
{
    velocity.x += vel.x;
    velocity.y += vel.y;
    velocity.z += vel.z;
}

Vec2 TransformationMatrix::getVelocity2D()
{
    return Vec2({velocity.x, velocity.y});
}

Vec3 TransformationMatrix::getVelocity3D()
{
    return Vec3({velocity.x, velocity.y, velocity.z});
}

void multiplica(float *m1, float *m2, float *m_resultado)
{

    // OpenGL lida recebe vetores de 16 elementos e interpreta como matrizes 4x4.
    // Nessa funcao, transformamos as matrizes de volta para float[4][4] para facilitar a multiplicacao

    float m_a[4][4];
    float m_b[4][4];
    float m_c[4][4]; // m_c = m_a * m_b

    int n = 0;
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            m_a[i][j] = m1[n];
            m_b[i][j] = m2[n];
            n += 1;
        }
    }

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            m_c[i][j] = 0.0;
            for (int k = 0; k < 4; k++)
            {
                m_c[i][j] += m_a[i][k] * m_b[k][j];
            }
        }
    }

    // voltando a resposta para o formato do OpenGL
    n = 0;
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            m_resultado[n] = m_c[i][j];
            n += 1;
        }
    }
}

void TransformationMatrix::updateMatrix()
{
    Vec3 cosAngle = {(float)cos(rotation.x), (float)cos(rotation.y), (float)cos(rotation.z)};
    Vec3 sinAngle = {(float)sin(rotation.x), (float)sin(rotation.y), (float)sin(rotation.z)};

    translation.x += velocity.x;
    translation.y += velocity.y;
    translation.z += velocity.z;

    float scale = scale2D * scale3D;

    float rotationX[16] = {
        1.0f, 0.0f, 0.0f, 0.0f,
        0.0f, cosAngle.x, -sinAngle.x, 0.0f,
        0.0f, sinAngle.x, cosAngle.x, 0.0f,
        0.0f, 0.0f, 0.0f, 1.0f};

    float rotationY[16] = {
        cosAngle.y, 0.0f, sinAngle.y, 0.0f,
        0.0f, 1.0f, 0.0f, 0.0f,
        -sinAngle.y, 0.0f, cosAngle.y, 0.0f,
        0.0f, 0.0f, 0.0f, 1.0f};

    float rotationZ[16] = {
        cosAngle.z, -sinAngle.z, 0.0f, 0.0f,
        sinAngle.z, cosAngle.z, 0.0f, 0.0f,
        0.0f, 0.0f, 1.0f, 0.0,
        0.0f, 0.0f, 0.0f, 1.0f};

    float translationMatrix[16] = {
        1.0f, 0.0f, 0.0f, translation.x,
        0.0f, 1.0f, 0.0f, translation.y,
        0.0f, 0.0f, 1.0f, translation.z,
        0.0f, 0.0f, 0.0f, 1.0f};

    float scaleMatrix[16] = {
        scale, 0.0f, 0.0f, 0.0f,
        0.0f, scale, 0.0f, 0.0f,
        0.0f, 0.0f, scale3D, 0.0f,
        0.0f, 0.0f, 0.0f, 1.0f};

    float finalMatrix[16] = {
        0.0f, 0.0f, 0.0f, 0.0f,
        0.0f, 0.0f, 0.0f, 0.0f,
        0.0f, 0.0f, 0.0f, 0.0f,
        0.0f, 0.0f, 0.0f, 0.0f};

    multiplica(rotationZ, rotationX, this->getMatrix());
    multiplica(rotationY, this->getMatrix(), this->getMatrix());
    multiplica(translationMatrix, this->getMatrix(), this->getMatrix());
    multiplica(scaleMatrix, this->getMatrix(), this->getMatrix());
}


void TransformationMatrix::print()
{
    std::cout << "Transformation Matrix:" << std::endl;
    std::cout << std::fixed << std::setprecision(1);

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            std::cout << transformationMatrix[i * 4 + j] << " ";
        }
        std::cout << std::endl;
    }
}
