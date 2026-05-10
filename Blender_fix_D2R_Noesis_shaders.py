import bpy
import os

for mat in bpy.data.materials:
    node_tree = bpy.data.materials[mat.name].node_tree
    links = bpy.data.materials[mat.name].node_tree.links
    albedo_node = mat.node_tree.nodes.get('Image Texture')
    bsdf_node = mat.node_tree.nodes.get('Principled BSDF')
    albedo_filepath = albedo_node.image.filepath
    if "_hair" in albedo_filepath:
        print("Hair material has no ORM map")
    elif "_fur" in albedo_filepath:
        print("Fur material has no ORM map")
    elif "_beard" in albedo_filepath:
        print("Beard material has no ORM map")
    else:
        orm_filepath = albedo_filepath.replace("_alb.png","_orm.png")
        sss_filepath = albedo_filepath.replace("_alb.png","_sss.png")
        
        #check if ORM and SSS files exists
        orm_os_path = orm_filepath.replace("//textures",".\\textures")
        sss_os_path = sss_filepath.replace("//textures",".\\textures")
        if os.path.isfile(orm_os_path) == False:
            print('ORM file missing')
        else:
            print(orm_os_path)
            #create nodes
            ORM_texture_node = node_tree.nodes.new('ShaderNodeTexImage')
            ORM_texture_node.image = bpy.data.images.load(orm_filepath)
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
            SSS_texture_node.image = bpy.data.images.load(sss_filepath)
            SSS_texture_node.image.colorspace_settings.name = 'Non-Color'
            SSS_texture_node.location.x = -900
            SSS_texture_node.location.y = -200
            links.new(SSS_texture_node.outputs[0], bsdf_node.inputs[10])
            #global IOR for skin
            bsdf_node.inputs[3].default_value = 1.2
            #Subsurface weight
            bsdf_node.inputs[8].default_value = 1
            #Subsurface IOR
            bsdf_node.inputs[10].default_value = 1.4
            bsdf_node.subsurface_method = "RANDOM_WALK_SKIN"