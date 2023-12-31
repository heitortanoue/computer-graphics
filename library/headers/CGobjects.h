#ifndef CGOBJECTS_H
#define CGOBJECTS_H

#include "CGtypes.h"
#include <iostream>
#include <cmath>
#include <functional>

class CGObject
{
public:
    CGObject(const char* name);

    CGObject(const int& maxVer) : maxVertices(maxVer)
    {
        this->name = std::string("Object");
    }

    CGObject(const int& maxVer, const char* name) : maxVertices(maxVer), name(name) {}

    inline int getMaxVertices() { return maxVertices; }

    TransformationMatrix* getTransformationMatrix();

    std::string getName() { return name; }

    virtual void keyEvent(int key, int scancode, int action, int mods)
    {
        if (keyEventCallback)
        {
            keyEventCallback(key, scancode, action, mods);
        }
    }
    virtual void draw(GLuint program) = 0;

    virtual VecBase *getVerticesMatrix() = 0;
    virtual size_t getVerticesSize() = 0;
    virtual void printData() = 0;
    virtual GLVec3* verticesToGLVec3() = 0;

    void setKeyEventCallback(std::function<void(int, int, int, int)> callback)
    {
        keyEventCallback = callback;
    }

    void setConstantMotion(std::function<void()> callback)
    {
        constantMotionCallback = callback;
    }

    void executeConstantMotion()
    {
        if (constantMotionCallback)
        {
            constantMotionCallback();
        }
    }

    GLuint buffer;
    GLint loc;

protected:
    const int maxVertices = 0;

    std::string name;

    TransformationMatrix transformation;

    std::function<void(int, int, int, int)> keyEventCallback;
    std::function<void()> constantMotionCallback;
};

#endif