#ifndef CGSHAPES_H
#define CGSHAPES_H

#include "CGobjects.h"

class CGtriangle : public CGObject
{
using CGObject::CGObject;

public:
    CGtriangle() : CGObject(3) {}

    CGtriangle(Vec2 vertices[3], const char *name);
    CGtriangle(Vec2 vertices[3], const char *name, Vec2 initialPos);
    ~CGtriangle();

    void draw();

private:

};

#endif