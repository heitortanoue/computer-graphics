#include "CGtypes.h"
#include "CGobjects.h"
#include "CGengine.h"
#include "CGshapes2D.h"

using namespace std;

const float velocity = .01f;
const float rotationSpeed = .05f;
const float scaleSpeed = .02f;

int main(void)
{
    CGengine engine;

    Vec2 vertices[3] = {
        {0.00f, +0.05f},
        {-0.05f, -0.05f},
        {+0.05f, -0.05f}};

    CGtriangle triangle = CGtriangle(vertices, "Triangulo1");
    triangle.setKeyEventCallback([&triangle](int key, int scancode, int action, int mods)
    {
        if (key == 262)
            (*triangle.getTransformationMatrix()).addVelocity({velocity, 0}); // tecla para direita
        if (key == 263)
            (*triangle.getTransformationMatrix()).addVelocity({-velocity, 0}); // tecla para esquerda
        if (key == 265)
            (*triangle.getTransformationMatrix()).translate({0, velocity}); // tecla para cima
        if (key == 264)
            (*triangle.getTransformationMatrix()).translate({0, -velocity}); // tecla para baixo

        if (key == 81)
            (*triangle.getTransformationMatrix()).rotate(rotationSpeed); // tecla Q
        if (key == 69)
            (*triangle.getTransformationMatrix()).rotate(-rotationSpeed); // tecla E

        if (key == 90)
            (*triangle.getTransformationMatrix()).scaleTransform2D(scaleSpeed); // tecla Z
        if (key == 88)
            (*triangle.getTransformationMatrix()).scaleTransform2D(-scaleSpeed); // tecla X
    });

    CGtriangle triangle2 = CGtriangle(vertices, "Triangulo2", {0.5f, 0.5f});
    triangle2.setKeyEventCallback([&triangle2](int key, int scancode, int action, int mods) {
        if (key == 80) {
            (*triangle2.getTransformationMatrix()).rotate('y', 0.05f); // tecla P
        }

        if (key == 79) {
            (*triangle2.getTransformationMatrix()).rotate('y', -0.05f); // tecla O
        }
    });

    engine.addObject(triangle);
    engine.addObject(triangle2);

    engine.run();

    exit(EXIT_SUCCESS);
}
