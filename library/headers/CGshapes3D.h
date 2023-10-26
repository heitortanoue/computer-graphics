#ifndef CGSHAPES3D_H
#define CGSHAPES3D_H

#include "CGobject3D.h"
#define numSegments 360

class CGcube : public CGObject3D
{
    using CGObject3D::CGObject3D;

public:
    CGcube() : CGObject3D(8, 24) {}

    CGcube(Vec3 vertices[8], const char *name) : CGObject3D(8, 24, name)
    {
        for (int i = 0; i < 8; i++)
        {
            pushVertex(vertices[i]);
        }

        this->name = name;
    }

    CGcube(Vec3 origin, float side_length, const char *name) : CGObject3D(8, 24, name)
    {
        float half_side = side_length / 2;

        Vec3 vertices[8] = {
            {origin.x - half_side, origin.y - half_side, origin.z - half_side}, // 0
            {origin.x - half_side, origin.y + half_side, origin.z - half_side}, // 1
            {origin.x + half_side, origin.y + half_side, origin.z - half_side}, // 2
            {origin.x + half_side, origin.y - half_side, origin.z - half_side}, // 3

            {origin.x + half_side, origin.y - half_side, origin.z + half_side}, // 4
            {origin.x + half_side, origin.y + half_side, origin.z + half_side}, // 5
            {origin.x - half_side, origin.y + half_side, origin.z + half_side}, // 6
            {origin.x - half_side, origin.y - half_side, origin.z + half_side}  // 7
        };

        for (int i = 0; i < 8; i++)
        {
            pushVertex(vertices[i]);
        }

        this->name = name;
    }
    ~CGcube();

    Vec3* getVerticesMatrix() override;
    void draw(GLuint program);
};

// PYRAMID
class CGpyramid : public CGObject3D
{
    using CGObject3D::CGObject3D;

public:
    CGpyramid() : CGObject3D(5, 18) {}

    CGpyramid(Vec3 vertices[5], const char *name) : CGObject3D(5, 16, name)
    {
        for (int i = 0; i < 5; i++)
        {
            pushVertex(vertices[i]);
        }

        this->name = name;
    }

    CGpyramid(Vec3 origin, float side_length, float height, const char *name) : CGObject3D(5, 16, name)
    {
        float half_side = side_length / 2;
        float half_height = height / 2;

        Vec3 vertices[5] = {
            {origin.x, origin.y + half_height, origin.z},                         // 5
            {origin.x - half_side, origin.y - half_height, origin.z - half_side}, // 1
            {origin.x - half_side, origin.y - half_height, origin.z + half_side}, // 2
            {origin.x + half_side, origin.y - half_height, origin.z + half_side}, // 3
            {origin.x + half_side, origin.y - half_height, origin.z - half_side}, // 4
        };

        for (int i = 0; i < 5; i++)
        {
            pushVertex(vertices[i]);
            std::cout << vertices[i].x << " " << vertices[i].y << " " << vertices[i].z << std::endl;
        }

        this->name = name;
    }

    ~CGpyramid();

    Vec3* getVerticesMatrix() override;
    void draw(GLuint program);
};

// CYLINDER

class CGcylinder : public CGObject3D
{
    using CGObject3D::CGObject3D;

public:
    CGcylinder(Vec3 origin, float radius, float height, const char* name) : CGObject3D(2*numSegments + 2, numSegments * 8 + 2, name)
    {
        float theta; // angulo de cada triângulo
        Vec3 vertices[(2*numSegments)+2]; // todos os vértices que compõem o cilindro (circulo de cima + debaixo + centro de cima + debaixo)

        Vec3 originUpper = origin;
        originUpper.z += height/2;
        vertices[0] = originUpper; // centro superior do cilindro
        
        Vec3 originDown = origin;
        originDown.z -= height/2;
        vertices[numSegments+1] = originDown; // centro inferior do cilindro

        for (int i = 1; i <= numSegments; i++)
        {
            theta = 2 * M_PI * (i / float(numSegments)); // angulo do vértice

            vertices[i] = {origin.x + radius * cos(theta), origin.y + radius * sin(theta), origin.z + height/2}; // vértice superior
            vertices[i + numSegments + 1] = {origin.x + radius * cos(theta), origin.y + radius * sin(theta), origin.z - height/2}; // vértice inferior
        }

        for (int i = 0; i < (2*numSegments + 2); i++)
        {
            pushVertex(vertices[i]); // adiciona os vértices ao vetor de vértices
        }

        this->name = name;
    }

    ~CGcylinder();

    Vec3* getVerticesMatrix() override;
    void draw(GLuint program);

};

#endif