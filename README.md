Sometimes a .model file will include 2 meshes instead of one, so to export the character without missing components I use the following parameters:  
A.Noesis GR2 plugin settings:  
ANIMATION_MODE = 2 (only the animations from the model file, which are none)  
SKELETON_LOAD = 1  
MERGE_SCENE = 1 (to merge all meshes in the same scene)  

B.Noesis batch export:  
Input extension: model  
Output extension: fbx  
Additional parameters -fbxtexext .png -scale 80 -fbxmultitake  
Output path $inpath$\$inname$.$outext$  
Recursive  

I used scale 80 to have in Blender models between 1.65m-1.9m (humans) and 4m high (monsters)  

To batch export the animations:  
A.Generate for each animation track a Noesis scene file using the Python script, you have to know the total number of tracks  
B.Put the Noesis scene files in the same folder as the "torso_lod0.model"/"torso_lit_lod0.model"/"torso_stp_lod0.model" is  
C.Noesis GR2 plugin settings:  
ANIMATION_MODE = 1 (paired file)  
SKELETON_LOAD = 1  
MERGE_SCENE = 0  

D.Noesis batch export:  
input: noesis  
output: fbx  
output path: $inpath$\$inname$.$outext$  
Recursive

When you import the FBX with animations in Blender always set scale to 80. I always load all the animations in the same Blender scene and rename the actions using the exported animation name list and Blender script.  

Change log for Noesis GR2 plugin for version 136:  
1. Automatically loads the skeleton and animation file if the folder structure and naming is respected :  
\[characterName]\torso_lod0.model  
\[characterName]\skeleton\[characterName].skeleton  
\[characterName]\animation\combined.animations  
2.Prompt to ask user the track number for the animations  
3.Option to specifiy argument "-animtrack x" where x is integer smaller than total number of tracks, useful for Noesis batch processing.  
4.Automatically creates a text file with the total number of animation tracks - after the user specify a track number (the prompt will tell you the max number of tracks).
5.Automatically creates a list of loaded animations names the way they were stored in combined.animations ; the list will continuously append new loaded animations until you delete the file.
