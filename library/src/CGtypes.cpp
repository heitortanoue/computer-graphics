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

void TransformationMatrix::updateMatrix()
{
    Vec3 cosAngle = {(float)cos(rotation.x), (float)cos(rotation.y), (float)cos(rotation.z)};
    Vec3 sinAngle = {(float)sin(rotation.x), (float)sin(rotation.y), (float)sin(rotation.z)};

    translation.x += velocity.x;
    translation.y += velocity.y;
    translation.z += velocity.z;

    float scale = scale2D * scale3D;

    transformationMatrix[0] = scale * cosAngle.z * cosAngle.y;
    transformationMatrix[1] = scale * sinAngle.z;
    transformationMatrix[2] = scale3D * -sinAngle.y;
    transformationMatrix[3] = translation.x;

    transformationMatrix[4] = scale * -sinAngle.z;
    transformationMatrix[5] = scale * cosAngle.z * cosAngle.x;
    transformationMatrix[6] = scale3D * sinAngle.x;
    transformationMatrix[7] = translation.y;

    transformationMatrix[8] = scale3D * sinAngle.y;
    transformationMatrix[9] = scale3D * -sinAngle.x;
    transformationMatrix[10] = scale3D * cosAngle.x * cosAngle.y;
    transformationMatrix[11] = translation.z;

    transformationMatrix[12] = 0.0f;
    transformationMatrix[13] = 0.0f;
    transformationMatrix[14] = 0.0f;
    transformationMatrix[15] = 1.0f;
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
