import bpy
import os
import glob

workdir = os.path.split(bpy.data.filepath)[0]
modelfiles = glob.glob (workdir+'\\*.model')
modelname = os.path.split(modelfiles[0])[1].split(".")[0]
fbxpath = workdir+'\\'+modelname+'.fbx'
blendpath = workdir+'\\'+modelname+'.blend'
#print(modelname)
print(fbxpath)
print(blendpath)

#bpy.ops.wm.open_mainfile(filepath=workdir+'\\'+'New_testfile.blend')
bpy.ops.import_scene.fbx(filepath=fbxpath)

for image in bpy.data.images:
    oldpath = bpy.path.abspath(image.filepath)
    if "_alb.png" in oldpath:
        full_os_path = bpy.path.abspath(oldpath)
        abs_tex_path = os.path.split(full_os_path)[0]

for mat in bpy.data.materials:
    node_tree = bpy.data.materials[mat.name].node_tree
    links = bpy.data.materials[mat.name].node_tree.links
    albedo_node = mat.node_tree.nodes.get('Image Texture')
    bsdf_node = mat.node_tree.nodes.get('Principled BSDF')
    output_node = mat.node_tree.nodes.get('Material Output')

    albedo_filepath = bpy.path.abspath(albedo_node.image.filepath)
    # if it's relative path - can't be because of bpy.path.abspath
    if ("//textures\\") in albedo_filepath:
        albedo_filename = albedo_filepath.replace("//textures\\","")
    #if it's absolute path
    else:
        albedo_filename = os.path.split(albedo_filepath)[1]

    albedo_os_path = abs_tex_path + '\\'+albedo_filename
    print('---------------------------------------------------')
    print(albedo_os_path)
    print('---------------------------------------------------')

    if ("_hair" or "_beard") in albedo_os_path:
        print("Hair material has no ORM map")

        #check if [charname]_FLOW map exist
        flow_os_path = albedo_os_path.replace("_alb.png","_flow.png")
        if os.path.isfile(flow_os_path) == False:
            print('Could not find [charname]_flow.png')
            flow_os_path = abs_tex_path+"\\common_hair1_flow.png"
            if os.path.isfile(flow_os_path) == False:
                print('Could not find common_hair1_flow.png')
                flow_os_path = abs_tex_path+"\\common_hair2_flow.png"
                if os.path.isfile(flow_os_path) == False:
                    print("Could not find any FLOW file, no hair shader modified")
                else:

                    flow_os_path = abs_tex_path+"\\common_hair2_flow.png"
                    hrt_os_path = abs_tex_path+"\\common_hair2_hrt.png"
            else:

                 flow_os_path = abs_tex_path+"\\common_hair1_flow.png"
                 hrt_os_path = abs_tex_path+"\\common_hair1_hrt.png"
        else:
            hrt_os_path = albedo_os_path.replace("_alb.png","_hrt.png")
            if os.path.isfile(hrt_os_path) == False:
                print("Could not find any HRT file, no hair shader modified")
        #create hair shader
        if ((os.path.isfile(flow_os_path) != False) and (os.path.isfile(hrt_os_path) != False)):
            flow_node = node_tree.nodes.new('ShaderNodeTexImage')
            flow_node.image = bpy.data.images.load(flow_os_path)
            flow_node.image.colorspace_settings.name = 'Non-Color'
            hrt_node = node_tree.nodes.new('ShaderNodeTexImage')
            hrt_node.image = bpy.data.images.load(hrt_os_path)
            hrt_node.image.colorspace_settings.name = 'Non-Color'
            ColorDarken_node = node_tree.nodes.new('ShaderNodeMixRGB')
            ColorDarken_node.blend_type = "DARKEN"
            ColorRamp_node = node_tree.nodes.new('ShaderNodeValToRGB')
            links.new(hrt_node.outputs[0], ColorRamp_node.inputs[0])
            links.new(ColorRamp_node.outputs[0], ColorDarken_node.inputs[2])
            links.new(albedo_node.outputs[0], ColorDarken_node.inputs[1])  
            links.new(ColorDarken_node.outputs[0], bsdf_node.inputs[0]) 
            links.new(flow_node.outputs[0], bsdf_node.inputs[17])
            #Anisotropic
            bsdf_node.inputs[15].default_value = 0.9 
            flow_node.location.x = -600
            flow_node.location.y = -600
            hrt_node.location.x = -600
            hrt_node.location.y = 0
            ColorDarken_node.location.x = -40
            ColorDarken_node.location.y = 300
            ColorRamp_node.location.x = -300
            ColorRamp_node.location.y = 100
            bsdf_node.location.x = 150
            bsdf_node.location.y = 200
            output_node.location.x = 450
    
    elif "fur" in albedo_os_path:
        print("Fur material has no ORM map")

        #check if [charname]_FLOW map exist                
        flow_os_path = albedo_os_path.replace("_alb.png","_flow.png")
        if os.path.isfile(flow_os_path) == False:
            print('Could not find [charname]_flow.png')
            flow_os_path = abs_tex_path+"\\common_fur_flow.png"
            if os.path.isfile(flow_os_path) == False:
                print('Could not find common_fur_flow.png, fur shader untouched')
            else:

                flow_os_path = abs_tex_path+"\\common_fur_flow.png"
                hrt_os_path = abs_tex_path+"\\common_fur_hrt.png"
        else:
              hrt_os_path = albedo_os_path.replace("_alb.png","_hrt.png")
              if os.path.isfile(hrt_os_path) == False:
                  print('Could not find common_fur_flow.png, fur shader untouched')
        #create fur shader
        if ((os.path.isfile(flow_os_path) != False) and (os.path.isfile(hrt_os_path) != False)):
            flow_node = node_tree.nodes.new('ShaderNodeTexImage')
            flow_node.image = bpy.data.images.load(flow_os_path)
            flow_node.image.colorspace_settings.name = 'Non-Color'
            hrt_node = node_tree.nodes.new('ShaderNodeTexImage')
            hrt_node.image = bpy.data.images.load(hrt_os_path)
            hrt_node.image.colorspace_settings.name = 'Non-Color'
            ColorDarken_node = node_tree.nodes.new('ShaderNodeMixRGB')
            ColorDarken_node.blend_type = "DARKEN"
            ColorRamp_node = node_tree.nodes.new('ShaderNodeValToRGB')
            links.new(hrt_node.outputs[0], ColorRamp_node.inputs[0])
            links.new(ColorRamp_node.outputs[0], ColorDarken_node.inputs[2])
            links.new(albedo_node.outputs[0], ColorDarken_node.inputs[1])  
            links.new(ColorDarken_node.outputs[0], bsdf_node.inputs[0]) 
            links.new(flow_node.outputs[0], bsdf_node.inputs[17])
            #Anisotropic
            bsdf_node.inputs[15].default_value = 0.9 
            flow_node.location.x = -600
            flow_node.location.y = -600
            hrt_node.location.x = -600
            hrt_node.location.y = 0
            ColorDarken_node.location.x = -40
            ColorDarken_node.location.y = 300
            ColorRamp_node.location.x = -300
            ColorRamp_node.location.y = 100
            bsdf_node.location.x = 150
            bsdf_node.location.y = 200
            output_node.location.x = 450

        
    else:

        #check if ORM and SSS files exists
        orm_os_path = albedo_os_path.replace("_alb.png","_orm.png")
        sss_os_path = albedo_os_path.replace("_alb.png","_sss.png")
        if os.path.isfile(orm_os_path) == False:
            print('ORM file missing')
        else:
            print(orm_os_path)
            #create nodes
            ORM_texture_node = node_tree.nodes.new('ShaderNodeTexImage')
            ORM_texture_node.image = bpy.data.images.load(orm_os_path)
            ORM_texture_node.image.colorspace_settings.name = 'Non-Color'
            SeparateColor_node = node_tree.nodes.new('ShaderNodeSeparateColor')
            ColorMultiply_node = node_tree.nodes.new('ShaderNodeMixRGB')
            #create links
            links.new(ORM_texture_node.outputs[0], SeparateColor_node.inputs[0])
            links.new(SeparateColor_node.outputs[0], ColorMultiply_node.inputs[2])
            links.new(SeparateColor_node.outputs[1], bsdf_node.inputs[2])
            links.new(SeparateColor_node.outputs[2], bsdf_node.inputs[1])
            links.new(ColorMultiply_node.outputs[0], bsdf_node.inputs[0])
            links.new(albedo_node.outputs[0], ColorMultiply_node.inputs[1])
            #golbal IOR
            bsdf_node.inputs[3].default_value = 1.2
            ColorMultiply_node.blend_type = "MULTIPLY"
            #tweak nodes positions
            bsdf_node.location.x = -50
            bsdf_node.location.y = 200
            ORM_texture_node.location.x = -600
            ORM_texture_node.location.y = 0
            SeparateColor_node.location.x = -300
            SeparateColor_node.location.y = 100
            ColorMultiply_node.location.x = -240
            ColorMultiply_node.location.y = 448
        if os.path.isfile(sss_os_path) == False:
            print('SSS file missing')
        else:
            print(sss_os_path)
            #create nodes
            SSS_texture_node = node_tree.nodes.new('ShaderNodeTexImage')
            SSS_texture_node.image = bpy.data.images.load(sss_os_path)
            SSS_texture_node.image.colorspace_settings.name = 'Non-Color'
            SSS_texture_node.location.x = -900
            SSS_texture_node.location.y = -200
            links.new(SSS_texture_node.outputs[0], bsdf_node.inputs[9])
            #global IOR for skin
            bsdf_node.inputs[3].default_value = 1.2
            #Subsurface weight
            bsdf_node.inputs[8].default_value = 1
            #Subsurface scatter distance in meters
            bsdf_node.inputs[10].default_value = 0.01
            bsdf_node.subsurface_method = "RANDOM_WALK_SKIN"

# make texture paths relative for the new shaders
for image in bpy.data.images:
    oldpath = image.filepath
    tex_name = os.path.split(oldpath)[1]
    if tex_name == '':
        print('No image name here or already relative path '+oldpath)
    else:
        newpath = '//textures\\'+tex_name
        print(newpath)
        image.filepath = newpath
        image.reload()


bpy.ops.wm.save_as_mainfile(filepath=blendpath)
