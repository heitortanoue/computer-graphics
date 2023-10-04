#ifndef CGSHAPES2D_H
#define CGSHAPES2D_H

#include "CGobject2D.h"

class CGtriangle : public CGObject2D
{
    using CGObject2D::CGObject2D;

public:
    CGtriangle() : CGObject2D(3) {}

    CGtriangle(Vec2 vertices[3], const char *name);
    CGtriangle(Vec2 vertices[3], const char *name, Vec2 initialPos);
    ~CGtriangle();

    void draw(GLuint program);

private:

};

#endif