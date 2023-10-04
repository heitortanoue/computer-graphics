#include "CGobject3D.h"

CGObject3D::~CGObject3D()
{
    vertices.clear();
}

Vec3 *CGObject3D::getVerticesMatrix()
{
    return vertices.data();
}

std::vector<Vec3> CGObject3D::getVertices()
{
    return vertices;
}

GLVec3 *CGObject3D::verticesToGLVec3() {
    GLVec3* glVertices = new GLVec3[this->getVerticesSize()];
    Vec3* vertices = getVerticesMatrix();

    for (size_t i = 0; i < this->getVerticesSize(); i++)
    {
        glVertices[i].x = vertices[i].x;
        glVertices[i].y = vertices[i].y;
        glVertices[i].z = vertices[i].z;
    }

    return glVertices;
}

size_t CGObject3D::getVerticesSize()
{
    return neededVertices;
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