import bpy
import os

for mat in bpy.data.materials:
    node_tree = bpy.data.materials[mat.name].node_tree
    links = bpy.data.materials[mat.name].node_tree.links
    albedo_node = mat.node_tree.nodes.get('Image Texture')
    bsdf_node = mat.node_tree.nodes.get('Principled BSDF')
    output_node = mat.node_tree.nodes.get('Material Output')
    albedo_filepath = albedo_node.image.filepath
    if "_hair" in albedo_filepath:
        print("Hair material has no ORM map")
        flow_filepath = albedo_filepath.replace("_alb.png","_flow.png")
        hrt_filepath = albedo_filepath.replace("_alb.png","_hrt.png")
        #check if [charname]_FLOW map exist
        flow_os_path = flow_filepath.replace("//textures",".\\textures")
        if os.path.isfile(flow_os_path) == False:
            print('Could not find [charname]_flow.png')
            flow_os_path = ".\\textures\\common_hair1_flow.png"
            if os.path.isfile(flow_os_path) == False:
                print('Could not find common_hair1_flow.png')
                flow_os_path = ".\\textures\\common_hair2_flow.png"
                if os.path.isfile(flow_os_path) == False:
                    "Could not find any FLOW file, no hair shader modified"
                else:
                    flow_filepath = '//textures\\common_hair2_flow.png'
                    hrt_filepath = '//textures\\common_hair2_hrt.png'
            else:
                 flow_filepath = '//textures\\common_hair1_flow.png'
                 hrt_filepath = '//textures\\common_hair1_hrt.png'
        else:
            hrt_os_path = hrt_filepath.replace("//textures",".\\textures")
            if os.path.isfile(hrt_os_path) == False:
                    "Could not find any HRT file, no hair shader modified"
        #create hair shader
        flow_node = node_tree.nodes.new('ShaderNodeTexImage')
        flow_node.image = bpy.data.images.load(flow_filepath)
        flow_node.image.colorspace_settings.name = 'Non-Color'
        hrt_node = node_tree.nodes.new('ShaderNodeTexImage')
        hrt_node.image = bpy.data.images.load(hrt_filepath)
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
    
    elif "_fur" in albedo_filepath:
        print("Fur material has no ORM map")
        flow_filepath = albedo_filepath.replace("_alb.png","_flow.png")
        hrt_filepath = albedo_filepath.replace("_alb.png","_hrt.png")
        #check if [charname]_FLOW map exist
        flow_os_path = flow_filepath.replace("//textures",".\\textures")
        if os.path.isfile(flow_os_path) == False:
            print('Could not find [charname]_flow.png')
            flow_os_path = ".\\textures\\common_fur_flow.png"
            if os.path.isfile(flow_os_path) == False:
                print('Could not find common_fur_flow.png, fur shader untouched')
            else:
                flow_filepath = '//textures\\common_fur_flow.png'
                hrt_filepath = '//textures\\common_fur_hrt.png'
        else:
              hrt_os_path = hrt_filepath.replace("//textures",".\\textures")
              if os.path.isfile(hrt_os_path) == False:
                  print('Could not find common_fur_flow.png, fur shader untouched')
        #create fur shader
        flow_node = node_tree.nodes.new('ShaderNodeTexImage')
        flow_node.image = bpy.data.images.load(flow_filepath)
        flow_node.image.colorspace_settings.name = 'Non-Color'
        hrt_node = node_tree.nodes.new('ShaderNodeTexImage')
        hrt_node.image = bpy.data.images.load(hrt_filepath)
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

    elif "_beard" in albedo_filepath:
        flow_filepath = albedo_filepath.replace("_alb.png","_flow.png")
        hrt_filepath = albedo_filepath.replace("_alb.png","_hrt.png")
        #check if [charname]_FLOW map exist
        flow_os_path = flow_filepath.replace("//textures",".\\textures")
        if os.path.isfile(flow_os_path) == False:
            print('Could not find [charname]_flow.png')
            flow_os_path = ".\\textures\\common_hair1_flow.png"
            if os.path.isfile(flow_os_path) == False:
                print('Could not find common_hair1_flow.png')
                flow_os_path = ".\\textures\\common_hair2_flow.png"
                if os.path.isfile(flow_os_path) == False:
                    "Could not find any FLOW file, no hair shader modified"
                else:
                    flow_filepath = '//textures\\common_hair2_flow.png'
                    hrt_filepath = '//textures\\common_hair2_hrt.png'
            else:
                 flow_filepath = '//textures\\common_hair1_flow.png'
                 hrt_filepath = '//textures\\common_hair1_hrt.png'
        else:
            hrt_os_path = hrt_filepath.replace("//textures",".\\textures")
            if os.path.isfile(hrt_os_path) == False:
                    "Could not find any HRT file, no beard shader modified"
        #create beard shader
        flow_node = node_tree.nodes.new('ShaderNodeTexImage')
        flow_node.image = bpy.data.images.load(flow_filepath)
        flow_node.image.colorspace_settings.name = 'Non-Color'
        hrt_node = node_tree.nodes.new('ShaderNodeTexImage')
        hrt_node.image = bpy.data.images.load(hrt_filepath)
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
            links.new(SSS_texture_node.outputs[0], bsdf_node.inputs[9])
            #global IOR for skin
            bsdf_node.inputs[3].default_value = 1.2
            #Subsurface weight
            bsdf_node.inputs[8].default_value = 1
            #Subsurface scatter distance in meters
            bsdf_node.inputs[10].default_value = 0.01
            bsdf_node.subsurface_method = "RANDOM_WALK_SKIN"
