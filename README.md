Sometimes a .model file will include 2 meshes instead of one, so to export the character without missing components I use the following parameters:  
a.Noesis GR2 plugin settings:  
ANIMATION_MODE = 2 (only the animations from the model file, which are none)  
SKELETON_LOAD = 1  
MERGE_SCENE = 1 (to merge all meshes in the same scene)  

b.Noesis batch export:  
Input extension: model  
Output extension: fbx  
Additional parameters -fbxtexext .png -scale 80 -fbxmultitake  
Output path $inpath$\$inname$.$outext$  
Recursive  

I used scale 80 to have in Blender models between 1.65m-1.9m (humans) and 4m high (monsters). Always keep at least the Normal maps exported along model, because they will also have the blue channel (that is missing if you only convert the textures).  

To batch export the animations:  
a.Generate for each animation track a Noesis scene file using the Python script, you have to know the total number of tracks  
b.Put the Noesis scene files in the same folder as the "torso_lod0.model"/"torso_lit_lod0.model"/"torso_stp_lod0.model" is  
c.Noesis GR2 plugin settings:  
ANIMATION_MODE = 1 (paired file)  
SKELETON_LOAD = 1  
MERGE_SCENE = 0  

d.Noesis batch export:  
input: noesis  
output: fbx  
output path: $inpath$\$inname$.$outext$  
Recursive

Some models, as regurgitator1, bloodgolem, minionspawner, swarm, etc have too many meshes and Noesis will crash when attempting to load mesh + skeleton + animation for each mesh. The workaround is to copy the skeleton file from its folder to the character's main folder, rename it as skel.model and use generate_Noesis_scene_D2R_skel.py to generate a Noesis scene for each animation. This will include only the skeleton and animation, no mesh and no crash. You have to change Change fmt_GR2Reader.py options to ANIMATION_MODE = 1 and SKELETON_LOAD = 0  

When you import the FBX with animations in Blender always set scale to 80. I always load all the animations in the same Blender scene and rename the actions using the exported animation name list and Blender script.  
If you only convert texture files to PNG using Noesis it will break the Normal maps (missing blue channel). When exporting model and texture at the same time the Normal maps will be fine, but there will be no ORM and SSS maps.  
Noesis will export FBX with materials containing only diffuse map, aplha map and normal map. To fix the shaders in Blender use "Blender_fix_D2R_Noesis_shaders.py". This Blender script will add SubsurfaceScattering and OcclusionRoughnessMetalness maps to material, but only if the ORM and SSS texture files are present in subfolder "textures" relative to the Blender scene file.  

Change log for Noesis GR2 plugin for version 136:  
a) Automatically loads the skeleton and animation file if the folder structure and naming is respected :  
\[characterName]\torso_lod0.model  
\[characterName]\skeleton\[characterName].skeleton  
\[characterName]\animation\combined.animations  
b) Prompt to ask user the track number for the animations - inform user what is the total number of tracks  
c) Option to specifiy argument "-animtrack x" where x is integer smaller than total number of tracks, useful for Noesis batch processing.  
d) Automatically creates a text file with the total number of animation tracks - after the user specify a track number (the prompt will tell you the max number of tracks).  
e) Automatically creates a list of loaded animations names the way they were stored in combined.animations ; the list will continuously append new loaded animations until you delete the file.

The Barbarian player character has broken animations due to incorrect armature rotation and translation, and the Blender script will fix the animations if you have installed and active Animation Auto Offset add-on ("Relative editing" in Dope Sheet) and all the keyframes are selected. Just run the script with all the armatures holding animations in the same Blender file and this will fix it, so you can apply the resulting Blender action to the Barbarian player character.
