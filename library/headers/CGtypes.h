#ifndef CGTYPES_H
#define CGTYPES_H

#include <vector>
#include <GL/glew.h>

typedef struct
{
    float x, y, z;
} GLVec3;

class VecBase
{
public:
    virtual ~VecBase() {}

    float* getMatrix() { return (float*)this; }
};

class Vec2 : public VecBase
{
public:
    float x, y;
    Vec2() : x(0), y(0){}
    Vec2(float _x, float _y) : x(_x), y(_y) {}
};

class Vec3 : public VecBase
{
public:
    float x, y, z;
    Vec3(): x(0), y(0), z(0) {}
    Vec3(float _x, float _y, float _z) : x(_x), y(_y), z(_z) {}
};

class TransformationMatrix
{
public:
    TransformationMatrix() :
        translation({0.0f, 0.0f, 0.0f}),
        rotation({0.0f, 0.0f, 0.0f}),
        scale2D(1.0f),
        scale3D(1.0f),
        velocity({0.0f, 0.0f, 0.0f}) {}

    void translate(Vec2 tl);
    void translate(Vec3 tl);

    void addVelocity(Vec2 vel);
    void addVelocity(Vec3 vel);

    void rotate(float angle);
    void rotate(char axis, float angle);

    void scaleTransform2D(float scaleFactor);
    void scaleTransform3D(float scaleFactor);

    void multiply(TransformationMatrix &other);

    Vec2 getTranslation2D();
    Vec3 getTranslation3D();

    float getRotation2D();
    Vec3 getRotation3D();

    float getScale();

    Vec2 getVelocity2D();
    Vec3 getVelocity3D();

    float *getMatrix();
    void print();

    void updateMatrix();

    size_t size() { return sizeof(transformationMatrix); }

protected:
    Vec3 translation;
    Vec3 velocity;
    Vec3 rotation;
    float scale2D;
    float scale3D;
    float transformationMatrix[16];
};

#endif