#version 400

in vec3 out_fragPos;
in vec3 out_normal;
in vec2 out_texture;

uniform sampler2D samplerTexture;
uniform vec3 light_position;
vec3 light_color = vec3(1.0, 1.0, 1.0);
uniform vec3 view_position;

uniform float ka;
uniform float kd;
uniform float ks;
uniform float ns;

void main(){
    vec3 normal = normalize(out_normal);
    vec3 light_direction = normalize(light_position - out_fragPos);

    float diff = max(dot(normal, light_direction), 0.0);

    vec3 view_direction = normalize(view_position - out_fragPos);
    vec3 reflect_direction = normalize(reflect(-light_direction, normal));

    float specular = pow(max(dot(view_direction, reflect_direction), 0.0), ns);

    vec3 ambient_light = ka * light_color;
    vec3 diffuse_light = kd * diff * light_color;
    vec3 specular_light = ks * specular * light_color;

    gl_FragColor = vec4(ambient_light + diffuse_light + specular_light, 1.0) * texture(samplerTexture, out_texture);
}
