#include "CGobject3D.h"

CGObject3D::~CGObject3D()
{
    vertices.clear();
}

float *CGObject3D::getVerticesMatrix()
{
    float *verticesMatrix = new float[vertices.size() * 3];
    for (size_t i = 0; i < vertices.size(); i++)
    {
        verticesMatrix[i * 3] = vertices[i].x;
        verticesMatrix[i * 3 + 1] = vertices[i].y;
        verticesMatrix[i * 3 + 2] = vertices[i].z;

    }
    return verticesMatrix;
}

std::vector<Vec3> CGObject3D::getVertices()
{
    return vertices;
}

Vec3 *CGObject3D::getVerticesArray()
{
    return vertices.data();
}

size_t CGObject3D::getVerticesSize()
{
    return vertices.size() * sizeof(Vec3);
}

void CGObject3D::pushVertex(Vec3 vertex)
{
    if (vertices.size() >= (size_t)maxVertices)
    {
        std::cout << "Max vertices reached" << std::endl;
        return;
    }

    vertices.push_back(vertex);
}

void CGObject3D::printData()
{
    std::cout << "Object name: " << name << std::endl;
    std::cout << "Object vertices: " << std::endl;
    for (size_t i = 0; i < vertices.size(); i++)
    {
        std::cout << vertices[i].x << " " << vertices[i].y << " " << vertices[i].z << std::endl;
    }

    TransformationMatrix *transformation = getTransformationMatrix();
    std::cout << "Object translation: " <<
        transformation->getTranslation3D().x << " " <<
        transformation->getTranslation3D().y << " " <<
        transformation->getTranslation3D().z << std::endl;
    std::cout << "Object rotation: " <<
        transformation->getRotation3D().x << " " <<
        transformation->getRotation3D().y << " " <<
        transformation->getRotation3D().z << std::endl;
    std::cout << "Object scale: " << transformation->getScale() << std::endl;
}