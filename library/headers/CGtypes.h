#ifndef CGTYPES_H
#define CGTYPES_H

#include <vector>
#include <GL/glew.h>

typedef struct
{
    float x, y;
} Vec2;

class TransformationMatrix
{
public:
    TransformationMatrix() : translation({0.0f, 0.0f}), rotation(0.0f), scale(1.0f) {}

    void translate(Vec2 tl);
    void rotate(float angle);
    void scaleTransform(float scaleFactor);

    void multiply(TransformationMatrix &other);

    Vec2 getTranslation();
    float getRotation();
    float getScale();

    float *getMatrix();
    void print();

    void updateMatrix();

    size_t size() { return sizeof(transformationMatrix); }

private:
    Vec2 translation;
    float rotation;
    float scale;
    float transformationMatrix[16];
};

#endif