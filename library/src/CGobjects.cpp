#include "CGobjects.h"
#include "CGengine.h"

CGObject::CGObject()
{
    this->name = std::string("Object");
    this->vertices = std::vector<Vec2>();
    this->transformation = TransformationMatrix();
}

CGObject::CGObject(const char* name)
{
    this->name = std::string(name);
}

CGObject::~CGObject()
{
    vertices.clear();
}

float* CGObject::getVerticesMatrix() {
    float* verticesMatrix = new float[vertices.size() * 2];
    for (size_t i = 0; i < vertices.size(); i++) {
        verticesMatrix[i * 2] = vertices[i].x;
        verticesMatrix[i * 2 + 1] = vertices[i].y;
    }
    return verticesMatrix;
}

std::vector<Vec2> CGObject::getVertices()
{
    return vertices;
}

Vec2* CGObject::getVerticesArray()
{
    return vertices.data();
}

size_t CGObject::getVerticesSize()
{
    return vertices.size() * sizeof(Vec2);
}

void CGObject::pushVertex(Vec2 vertex)
{
    if (vertices.size() >= (size_t)maxVertices)
    {
        std::cout << "Max vertices reached" << std::endl;
        return;
    }

    vertices.push_back(vertex);
}

TransformationMatrix* CGObject::getTransformationMatrix()
{
    return &transformation;
}

void CGObject::printData() {
    std::cout << "Object name: " << name << std::endl;
    std::cout << "Object vertices: " << std::endl;
    for (size_t i = 0; i < vertices.size(); i++) {
        std::cout << vertices[i].x << " " << vertices[i].y << std::endl;
    }

    TransformationMatrix *transformation = getTransformationMatrix();
    std::cout << "Object translation: " << transformation->getTranslation().x << " " << transformation->getTranslation().y << std::endl;
    std::cout << "Object rotation: " << transformation->getRotation() << std::endl;
    std::cout << "Object scale: " << transformation->getScale() << std::endl;
}