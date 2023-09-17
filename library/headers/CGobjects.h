#ifndef CGOBJECTS_H
#define CGOBJECTS_H

#include "CGtypes.h"
#include <iostream>
#include <functional>

class CGObject
{
public:
    CGObject();
    CGObject(const char* name);
    CGObject(const int &maxVer) : maxVertices(maxVer) {
        this->vertices = std::vector<Vec2>();
        this->vertices.reserve(maxVer);
    }
    CGObject(const int &maxVer, const char* name) : maxVertices(maxVer), name(name) {
        this->vertices = std::vector<Vec2>();
        this->vertices.reserve(maxVer);
    }
    CGObject(const int &maxVer, const char *name, Vec2 initalPos) : maxVertices(maxVer), name(name)
    {
        this->vertices = std::vector<Vec2>();
        this->vertices.reserve(maxVer);
        this->transformation.translate(initalPos);
    }

    inline int getMaxVertices() { return maxVertices; }

    ~CGObject();

    float* getVerticesMatrix();
    std::vector<Vec2> getVertices();
    Vec2* getVerticesArray();
    size_t getVerticesSize();

    void pushVertex(Vec2 vertex);

    TransformationMatrix* getTransformationMatrix();

    std::string getName() { return name; }
    void printData();

    virtual void keyEvent(int key, int scancode, int action, int mods)
    {
        if (keyEventCallback)
        {
            keyEventCallback(key, scancode, action, mods);
        }
    }
    virtual void draw() = 0;

    void setKeyEventCallback(std::function<void(int, int, int, int)> callback)
    {
        keyEventCallback = callback;
    }

    GLuint buffer;
    GLint loc;

private:
    std::string name;

    std::vector<Vec2> vertices;

    TransformationMatrix transformation;

    std::function<void(int, int, int, int)> keyEventCallback;
protected:
    const int maxVertices = 0;
};

#endif