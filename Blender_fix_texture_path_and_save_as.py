import bpy
import os


for mat in bpy.data.materials:
    alb_path = bpy.data.images["Diffuse Texture"].filepath

    blend_name = alb_path.split('\\')[-3]
    model_path = os.path.split(alb_path)[0].rsplit('textures',1)
    blend_path = model_path[0]+blend_name+'.blend'

    alb_name = os.path.split(alb_path)[1]
    alb_fixed = '//textures\\'+alb_name
    bpy.data.images["Diffuse Texture"].filepath = alb_fixed
    bpy.data.images["Diffuse Texture"].reload()
    
    alpha_path = bpy.data.images["Diffuse Texture.001"].filepath
    alpha_name = os.path.split(alpha_path)[1]
    alpha_fixed = '//textures\\'+alpha_name
    bpy.data.images["Diffuse Texture.001"].filepath = alpha_fixed
    bpy.data.images["Diffuse Texture.001"].reload()
    
    nrm_path = bpy.data.images["Normal Texture"].filepath
    nrm_name = os.path.split(nrm_path)[1]
    nrm_fixed = '//textures\\'+nrm_name
    bpy.data.images["Normal Texture"].filepath = nrm_fixed
    bpy.data.images["Normal Texture"].reload()

    print(alb_fixed)
    print(alpha_fixed)
    print(nrm_fixed)

bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    
