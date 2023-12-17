#version 400

attribute vec3 position;
attribute vec2 texture_coord;
attribute vec3 normals;

out vec2 out_texture;
out vec3 out_fragPos;
out vec3 out_normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main(){
    gl_Position = projection * view * model * vec4(position, 1.0);
    out_fragPos = vec3(model * vec4(position, 1.0));
    out_texture = texture_coord;
    out_normal = (vec4(normals, 1.0) * model).xyz;
}