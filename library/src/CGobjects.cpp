#include "CGobjects.h"
#include "CGengine.h"
#include "CGtypes.h"

CGObject::CGObject(const char* name)
{
    this->name = std::string(name);
}

TransformationMatrix* CGObject::getTransformationMatrix()
{
    return &transformation;
}