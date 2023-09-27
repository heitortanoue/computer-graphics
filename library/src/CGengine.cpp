#include "CGengine.h"
#include "CGtypes.h"
#include "CGobjects.h"

using namespace std;

void CGengine::keyEventMaker(int key, int scancode, int action, int mods)
{
    std::cout << "Pressionando tecla: " << key << std::endl;

    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
        closeEngine();
        return;
    }

    for (auto &object : objects) {
        object->keyEvent(key, scancode, action, mods);
    }
}

static void keyEvent(GLFWwindow *window, int key, int scancode, int action, int mods)
{
    CGengine *engine = (CGengine *)glfwGetWindowUserPointer(window);

    if (engine == nullptr) {
        std::cerr << "Erro ao obter ponteiro para CGengine no keyEvent" << std::endl;
        return;
    }

    engine->keyEventMaker(key, scancode, action, mods);
}

CGengine::CGengine()
{
    init();
}

CGengine::~CGengine()
{
    closeEngine();
}

void CGengine::closeEngine()
{
    glfwWindowShouldClose(window);
    glfwDestroyWindow(window);
    glfwTerminate();

    exit(EXIT_SUCCESS);
}

void CGengine::run()
{
    while (!glfwWindowShouldClose(window))
    {
        update();
        render();
    }
}

void CGengine::init()
{
    initWindow();
    initGL();
    initShaders();

    glfwSetKeyCallback(window, keyEvent);
    glfwShowWindow(window);
}

void CGengine::initWindow()
{
    cout << "Inicializando Janela" << endl;

    if (!glfwInit())
    {
        std::cerr << "Erro ao inicializar o GLFW" << std::endl;
        exit(EXIT_FAILURE);
    }

    glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE);

    window = glfwCreateWindow(800, 800, "Minha Janela", NULL, NULL);

    if (!window)
    {
        std::cerr << "Erro ao criar a janela GLFW" << std::endl;
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    glfwSetWindowUserPointer(window, this);
    glfwMakeContextCurrent(window);

    cout << "Janela inicializada" << endl;
}

void CGengine::initGL()
{
    cout << "Inicializando OpenGL" << endl;

    GLenum err = glewInit();

    if (err != GLEW_OK)
    {
        std::cerr << "Erro ao inicializar o GLEW" << std::endl;
        exit(EXIT_FAILURE);
    }

    cout << "OpenGL inicializado" << endl;
}

void CGengine::initShaders()
{
    cout << "Inicializando Shaders" << endl;

    // GLSL para Vertex Shader
    const char *vertex_code =
        "attribute vec2 position;\n"
        "uniform mat4 mat_transformation;\n"
        "void main()\n"
        "{\n"
        "    gl_Position = mat_transformation * vec4(position, 0.0, 1.0);\n"
        "}\n";

    // GLSL para Fragment Shader
    const char *fragment_code =
        "uniform vec4 color;\n"
        "void main()\n"
        "{\n"
        "    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);\n"
        "}\n";

    program = glCreateProgram();
    GLuint vertex = glCreateShader(GL_VERTEX_SHADER);
    GLuint fragment = glCreateShader(GL_FRAGMENT_SHADER);

    glShaderSource(vertex, 1, &vertex_code, NULL);
    glShaderSource(fragment, 1, &fragment_code, NULL);

    glCompileShader(vertex);

    GLint isCompiled = 0;
    glGetShaderiv(vertex, GL_COMPILE_STATUS, &isCompiled);
    if (isCompiled == GL_FALSE)
    {
        int infoLength = 512;
        glGetShaderiv(vertex, GL_INFO_LOG_LENGTH, &infoLength);
        char info[infoLength];
        glGetShaderInfoLog(vertex, infoLength, NULL, info);
        std::cerr << "Erro de compilacao no Vertex Shader.\n"
                  << "--> " << info << std::endl;
    }

    glCompileShader(fragment);

    isCompiled = 0;
    glGetShaderiv(fragment, GL_COMPILE_STATUS, &isCompiled);
    if (isCompiled == GL_FALSE)
    {
        int infoLength = 512;
        glGetShaderiv(fragment, GL_INFO_LOG_LENGTH, &infoLength);
        char info[infoLength];
        glGetShaderInfoLog(fragment, infoLength, NULL, info);
        std::cerr << "Erro de compilacao no Fragment Shader.\n"
                  << "--> " << info << std::endl;
    }

    glAttachShader(program, vertex);
    glAttachShader(program, fragment);

    glLinkProgram(program);
    glUseProgram(program);

    cout << "Shaders inicializados" << endl;
}

void CGengine::update() {
    glfwPollEvents();

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glClearColor(1.0, 1.0, 1.0, 1.0);
}

void CGengine::render() {
    for (auto &object : objects) {
        object->loc = glGetUniformLocation(program, "mat_transformation");
        glUniformMatrix4fv(object->loc, 1, GL_TRUE, (*object->getTransformationMatrix()).getMatrix());

        object->draw();
        object->getTransformationMatrix()->updateMatrix();
    }

    glfwSwapBuffers(window);
}

void CGengine::addObject(CGObject &obj) {
    auto vertices = obj.getVerticesMatrix();

    glGenBuffers(1, &obj.buffer);
    glBindBuffer(GL_ARRAY_BUFFER, obj.buffer);

    glBufferData(GL_ARRAY_BUFFER, obj.getVerticesSize(), vertices, GL_DYNAMIC_DRAW);

    obj.loc = glGetAttribLocation(program, "position");
    glEnableVertexAttribArray(obj.loc);
    glVertexAttribPointer(obj.loc, 2, GL_FLOAT, GL_FALSE, sizeof(vertices[0]), (void *)0);

    objects.push_back(shared_ptr<CGObject>(&obj));
}

CGObject& CGengine::getObject(string name) {
    for (auto &object : objects) {
        if (object->getName() == name) {
            return *object;
        }
    }

    return *objects[0];
}