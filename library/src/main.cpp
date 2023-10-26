#include "CGtypes.h"
#include "CGengine.h"
#include "CGshapes2D.h"
#include "CGshapes3D.h"

using namespace std;

const float velocity = .05f;
const float rotationSpeed = .04f;
const float scaleSpeed = .02f;

int main(void)
{
    CGengine engine; // cria a engine

    // cria um cilindro
    CGcylinder cylinder = CGcylinder({0, 0, 0}, .5f, .8f, "Cylinder");

    cylinder.setKeyEventCallback([&](int key, int scancode, int action, int mods) {
        // rotação
        if (key == GLFW_KEY_UP){
            (*cylinder.getTransformationMatrix()).rotate('x', rotationSpeed);
        }
        if (key == GLFW_KEY_DOWN){
            (*cylinder.getTransformationMatrix()).rotate('x', -rotationSpeed);
        }
        if (key == GLFW_KEY_RIGHT){
            (*cylinder.getTransformationMatrix()).rotate('y', rotationSpeed);
        }
        if (key == GLFW_KEY_LEFT){
            (*cylinder.getTransformationMatrix()).rotate('y', -rotationSpeed);
        }
        if (key == GLFW_KEY_M){
            (*cylinder.getTransformationMatrix()).rotate('z', rotationSpeed);
        }
        if (key == GLFW_KEY_N){
            (*cylinder.getTransformationMatrix()).rotate('z', -rotationSpeed);
        }

        // movimento
        if (key == GLFW_KEY_W){
            (*cylinder.getTransformationMatrix()).translate(Vec3(0, velocity, 0));
        }
        if (key == GLFW_KEY_S){
            (*cylinder.getTransformationMatrix()).translate(Vec3(0, -velocity, 0));
        }
        if (key == GLFW_KEY_D){
            (*cylinder.getTransformationMatrix()).translate(Vec3(velocity, 0, 0));
        }
        if (key == GLFW_KEY_A){
            (*cylinder.getTransformationMatrix()).translate(Vec3(-velocity, 0, 0));
        }
        
        // escala
        if (key == GLFW_KEY_Z){
            (*cylinder.getTransformationMatrix()).scaleTransform3D(-scaleSpeed);
        }
        if (key == GLFW_KEY_X){
            (*cylinder.getTransformationMatrix()).scaleTransform3D(scaleSpeed);
        }

        // encerra o programa
        if (key == GLFW_KEY_ESCAPE){
            exit(EXIT_SUCCESS);
        }
    });

    engine.addObject(cylinder);

    engine.run();

    exit(EXIT_SUCCESS);
}
