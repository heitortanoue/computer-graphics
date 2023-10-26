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
    CGengine engine;

/*    CGcube cube = CGcube({-.1f, -.1f, 0}, .1f, "Cubo");

    cube.setConstantMotion([&]() {
        (*cube.getTransformationMatrix()).rotate('x', rotationSpeed * .3f);
        (*cube.getTransformationMatrix()).rotate('y', rotationSpeed * .4f);
        (*cube.getTransformationMatrix()).rotate('z', rotationSpeed * .5f);
    });

    engine.addObject(cube);

    CGpyramid pyramid = CGpyramid({.4f,.4f,0}, .2f, .3f, "Pyramid");

    pyramid.setConstantMotion([&]() {
        (*pyramid.getTransformationMatrix()).rotate('x', rotationSpeed * .3f);
        (*pyramid.getTransformationMatrix()).rotate('y', rotationSpeed * .4f);
        (*pyramid.getTransformationMatrix()).rotate('z', rotationSpeed * .5f);
    });

    engine.addObject(pyramid);
*/
    // cria um cilindro
    CGcylinder cylinder = CGcylinder({0, 0, 0}, .5f, .8f, "Cylinder");

    cylinder.setKeyEventCallback([&](int key, int scancode, int action, int mods) {
        // rotation
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

        // movement
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
        
        // scale
        if (key == GLFW_KEY_Z){
            (*cylinder.getTransformationMatrix()).scaleTransform3D(-scaleSpeed);
        }
        if (key == GLFW_KEY_X){
            (*cylinder.getTransformationMatrix()).scaleTransform3D(scaleSpeed);
        }
    });

    engine.addObject(cylinder);

    engine.run();

    exit(EXIT_SUCCESS);
}
