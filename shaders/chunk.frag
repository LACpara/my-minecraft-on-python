#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2DArray u_texture_array_0;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

in vec3 voxel_color;
in vec2 uv;
in float shading;


flat in int is_transparency;
flat in int voxel_id;
flat in int face_id;

void main(){
    float alpha = 1.0;
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;
    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, voxel_id-1)).rgb;

    tex_col = pow(tex_col, gamma);
    //tex_col.rgb *= voxel_color;
    //tex_col = tex_col * 0.001 + vec3(1.0);

    tex_col *= shading;
    tex_col = pow(tex_col, inv_gamma);

    alpha = (is_transparency == 1) && (tex_col.r + tex_col.g + tex_col.b == 0.0) ? 0.0 : 1.0;

    fragColor = vec4(tex_col, alpha);
}