#include "CGshapes2D.h"
#include "CGengine.h"
#include "CGtypes.h"
#include "CGobject2D.h"

CGtriangle::CGtriangle(Vec2 vertices[3], const char* newName) : CGObject2D(3, newName)
{
    for (size_t i = 0; i < 3; i++)
    {
        pushVertex(vertices[i]);
    }
}

CGtriangle::CGtriangle(Vec2 vertices[3], const char *newName, Vec2 initialPos) : CGObject2D(3, newName, initialPos)
{
    for (size_t i = 0; i < 3; i++)
    {
        pushVertex(vertices[i]);
    }
}

CGtriangle::~CGtriangle()
{

}

void CGtriangle::draw(GLuint program)
{
    glDrawArrays(GL_TRIANGLES, 0, 3);
}