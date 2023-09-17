#ifndef CGENGINE_H
#define CGENGINE_H

#include <GL/glew.h>
#define GLFW_INCLUDE_NONE
#include <GLFW/glfw3.h>
#include <vector>
#include "CGtypes.h"
#include "CGobjects.h"
#include <memory>

class CGengine
{
public:
    CGengine();
    ~CGengine();

    void run();

    void addObject(CGObject &obj);
    CGObject &getObject(std::string name);

    void keyEventMaker(int key, int scancode, int action, int mods);

    void closeEngine();

private:
    GLFWwindow *window;
    GLuint program;

    std::vector<std::shared_ptr<CGObject>> objects;

    void init();

    void initWindow();
    void initGL();
    void initShaders();

    void render();
    void update();
};

#endif