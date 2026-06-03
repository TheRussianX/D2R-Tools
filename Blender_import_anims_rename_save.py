import bpy
import os
import glob
from bpy import context as C

def rename_actions(anim_list):
    number_of_track_repeats=1 # the imported model has sometimes 2-6 meshes and the anim list wil have 2-6 times the same animation
    filelist = open(anim_list, 'r')
    if filelist != FileNotFoundError:
        data = filelist.readlines()
        actions = bpy.data.actions
        i = 1 #first line from anim list is empty
        for act in actions:
           act.name = data[i]
           print(act.name)
           i += number_of_track_repeats #increment i by 2 when are duplicate anim names due to multiple meshes in the same model file
           if ((i > len(actions)*number_of_track_repeats)):
               break
    else:
        print("Animation list not found")

workdir = os.path.split(bpy.data.filepath)[0]
animspath = workdir+'\\anims'
animsfiles = glob.glob (animspath+'\\*.fbx')
anim_list = workdir+'\\animations_list.txt'
for anim in animsfiles:
    print(anim)
    bpy.ops.import_scene.fbx(filepath=anim, global_scale=80)

first_action = bpy.data.actions.get("root|Noesis Frames|Noesis Layer")
if first_action != None:
    print("Renaming the first action")
    first_action.name = "root.000|Noesis Frames|Noesis Layer"
    rename_actions(anim_list)
elif bpy.data.actions.get("root.000|Noesis Frames|Noesis Layer") != None:
    print("First action is already renamed")
    rename_actions(anim_list)
else:
    print("First action does not exist.")
    exit



blendpath = workdir+'\\anims.blend'

print(blendpath)

#bpy.ops.wm.open_mainfile(filepath=workdir+'\\'+'New_testfile.blend')
bpy.ops.wm.save_as_mainfile(filepath=blendpath)