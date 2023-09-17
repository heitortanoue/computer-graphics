#include "CGshapes.h"
#include "CGengine.h"
#include "CGtypes.h"

CGtriangle::CGtriangle(Vec2 vertices[3], const char* newName) : CGObject(3, newName)
{
    for (size_t i = 0; i < 3; i++)
    {
        pushVertex(vertices[i]);
    }
}

CGtriangle::CGtriangle(Vec2 vertices[3], const char* newName, Vec2 initialPos) : CGObject(3, newName, initialPos)
{
    for (size_t i = 0; i < 3; i++)
    {
        pushVertex(vertices[i]);
    }
}

CGtriangle::~CGtriangle()
{

}

void CGtriangle::draw()
{
    glDrawArrays(GL_TRIANGLES, 0, 3);
}