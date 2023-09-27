#include "CGobject2D.h"

CGObject2D::~CGObject2D()
{
    vertices.clear();
}

float *CGObject2D::getVerticesMatrix()
{
    float *verticesMatrix = new float[vertices.size() * 2];
    for (size_t i = 0; i < vertices.size(); i++)
    {
        verticesMatrix[i * 2] = vertices[i].x;
        verticesMatrix[i * 2 + 1] = vertices[i].y;
    }
    return verticesMatrix;
}

std::vector<Vec2> CGObject2D::getVertices()
{
    return vertices;
}

Vec2* CGObject2D::getVerticesArray()
{
    return vertices.data();
}

size_t CGObject2D::getVerticesSize()
{
    return vertices.size() * sizeof(Vec2);
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