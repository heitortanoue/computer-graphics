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
    rotation += angle;
    updateMatrix();
}

void TransformationMatrix::scaleTransform(float scaleFactor)
{
    scale += scaleFactor;
    updateMatrix();
}

void TransformationMatrix::multiply(TransformationMatrix &other)
{
    translation.x += other.translation.x;
    translation.y += other.translation.y;
    rotation += other.rotation;
    scale += other.scale;
    updateMatrix();
}

Vec2 TransformationMatrix::getTranslation()
{
    return translation;
}

float TransformationMatrix::getRotation()
{
    return rotation;
}

float TransformationMatrix::getScale()
{
    return scale;
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

Vec2 TransformationMatrix::getVelocity()
{
    return velocity;
}

void TransformationMatrix::updateMatrix()
{
    float cosAngle = cos(rotation);
    float sinAngle = sin(rotation);

    translation.x += velocity.x;
    translation.y += velocity.y;

    transformationMatrix[0] = scale * cosAngle;
    transformationMatrix[1] = scale * sinAngle;
    transformationMatrix[2] = 0.0f;
    transformationMatrix[3] = translation.x;

    transformationMatrix[4] = -scale * sinAngle;
    transformationMatrix[5] = scale * cosAngle;
    transformationMatrix[6] = 0.0f;
    transformationMatrix[7] = translation.y;

    transformationMatrix[8] = 0.0f;
    transformationMatrix[9] = 0.0f;
    transformationMatrix[10] = 1.0f;
    transformationMatrix[11] = 0.0f;

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
