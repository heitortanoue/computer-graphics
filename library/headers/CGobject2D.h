#ifndef CGObject2D_H
#define CGObject2D_H

#include "CGtypes.h"
#include "CGobjects.h"

#include <iostream>
#include <functional>

class CGObject2D : public CGObject
{
public:
    CGObject2D();
    CGObject2D(const char *name) : CGObject(name){};

    CGObject2D(const int &maxVer) : CGObject(maxVer)
    {
        this->vertices = std::vector<Vec2>();
        this->vertices.reserve(maxVer);
    }
    CGObject2D(const int &maxVer, const char *name) : CGObject(maxVer, name)
    {
        this->vertices = std::vector<Vec2>();
        this->vertices.reserve(maxVer);
    }
    CGObject2D(const int &maxVer, const char *name, Vec2 initalPos) : CGObject(maxVer, name)
    {
        this->vertices = std::vector<Vec2>();
        this->vertices.reserve(maxVer);
        this->transformation.translate(initalPos);
    }

    ~CGObject2D();

    std::vector<Vec2> getVertices();

    Vec2 *getVerticesMatrix() override;
    size_t getVerticesSize() override;
    void printData() override;
    GLVec3 *verticesToGLVec3() override;

    void pushVertex(Vec2 vertex);

private:
    std::vector<Vec2> vertices;
};

#endif