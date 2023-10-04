#include "CGobject2D.h"

CGObject2D::~CGObject2D()
{
    vertices.clear();
}

Vec2 *CGObject2D::getVerticesMatrix()
{
    return vertices.data();
}

std::vector<Vec2> CGObject2D::getVertices()
{
    return vertices;
}

size_t CGObject2D::getVerticesSize()
{
    return vertices.size();
}

GLVec3 *CGObject2D::verticesToGLVec3()
{
    GLVec3 *glVertices = new GLVec3[vertices.size()];

    for (size_t i = 0; i < vertices.size(); i++)
    {
        glVertices[i].x = vertices[i].x;
        glVertices[i].y = vertices[i].y;
        glVertices[i].z = 0;
    }

    return glVertices;
}

void CGObject2D::pushVertex(Vec2 vertex)
{
    if (vertices.size() >= (size_t)maxVertices)
    {
        std::cout << "Max vertices reached" << std::endl;
        return;
    }

    vertices.push_back(vertex);
}

void CGObject2D::printData()
{
    std::cout << "Object name: " << name << std::endl;
    std::cout << "Object vertices: " << std::endl;
    for (size_t i = 0; i < vertices.size(); i++)
    {
        std::cout << vertices[i].x << " " << vertices[i].y << std::endl;
    }

    TransformationMatrix *transformation = getTransformationMatrix();
    std::cout << "Object translation: " << transformation->getTranslation2D().x << " " << transformation->getTranslation2D().y << std::endl;
    std::cout << "Object rotation: " << transformation->getRotation2D() << std::endl;
    std::cout << "Object scale: " << transformation->getScale() << std::endl;
}