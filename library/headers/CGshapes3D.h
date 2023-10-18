#ifndef CGSHAPES3D_H
#define CGSHAPES3D_H

#include "CGobject3D.h"

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

// SPHERE
class CGsphere : public CGObject3D
{
    using CGObject3D::CGObject3D;

public:
    CGsphere() : CGObject3D(0, (int)pow(divisions, 2)) {}

    CGsphere(Vec3 center, float radius, const char *name) : CGObject3D(0, (int)pow(divisions, 2), name)
    {
        generateSphere(center, radius);
        this->name = name;
    }

    ~CGsphere();

    Vec3* getVerticesMatrix() override;
    void draw(GLuint program);

private:
    void generateSphere(Vec3 center, float radius)
    {
        // Define o número de divisões da esfera para obter uma representação mais suave
        int qnt = 0;
        for (int i = 0; i < divisions; ++i)
        {
            float theta = i * M_PI / divisions; // Ângulo polar
            for (int j = 0; j <= divisions; ++j)
            {
                float phi = j * 2 * M_PI / divisions; // Ângulo azimutal

                // Calcula as coordenadas dos vértices da esfera
                float x = radius * sin(theta) * cos(phi) + center.x;
                float y = radius * sin(theta) * sin(phi) + center.y;
                float z = radius * cos(theta) + center.z;

                qnt++;
                std::cout << qnt << " " << x << " " << y << " " << z << std::endl;
                pushVertex({x, y, z});
            }
        }
    }

    const int divisions = 20;
};

#endif