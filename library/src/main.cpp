#include "CGtypes.h"
#include "CGengine.h"
#include "CGshapes2D.h"
#include "CGshapes3D.h"

using namespace std;

const float velocity = .01f;
const float rotationSpeed = .02f;
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

    cylinder.setConstantMotion([&]() {
        (*cylinder.getTransformationMatrix()).rotate('x', rotationSpeed * .3f);
        (*cylinder.getTransformationMatrix()).rotate('y', rotationSpeed * .4f);
        (*cylinder.getTransformationMatrix()).rotate('z', rotationSpeed * .5f);
    });

    engine.addObject(cylinder);

    engine.run();

    exit(EXIT_SUCCESS);
}
