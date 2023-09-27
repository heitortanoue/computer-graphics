#ifndef CGObject3D_H
#define CGObject3D_H

#include "CGtypes.h"
#include "CGobjects.h"

#include <iostream>
#include <functional>

class CGObject3D : public CGObject
{
public:
    CGObject3D();
    CGObject3D(const char *name);
    CGObject3D(const int &maxVer) : CGObject(maxVer)
    {
        this->vertices = std::vector<Vec3>();
        this->vertices.reserve(maxVer);
    }
    CGObject3D(const int &maxVer, const char *name) : CGObject(maxVer, name)
    {
        this->vertices = std::vector<Vec3>();
        this->vertices.reserve(maxVer);
    }
    CGObject3D(const int &maxVer, const char *name, Vec3 initalPos) : CGObject(maxVer, name)
    {
        this->vertices = std::vector<Vec3>();
        this->vertices.reserve(maxVer);
        this->transformation.translate(initalPos);
    }

    ~CGObject3D();

    std::vector<Vec3> getVertices();

    Vec3 *getVerticesArray() override;
    float *getVerticesMatrix() override;
    size_t getVerticesSize() override;
    void printData() override;

    void pushVertex(Vec3 vertex);

private:
    std::vector<Vec3> vertices;
};

#endif