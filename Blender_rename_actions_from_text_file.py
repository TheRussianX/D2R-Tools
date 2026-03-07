# root|Anim|Anim Layer
import bpy
from bpy import context as C

def rename_actions():
    number_of_track_repeats=2 # the imported model has sometimes 2-6 meshes and the anim list will have 2-6 times the same animation
    filelist = open('..//animations_list.txt', 'r')
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

first_action = bpy.data.actions.get("root|Noesis Frames|Noesis Layer")
if first_action != None:
    print("Renaming the first action")
    first_action.name = "root.000|Noesis Frames|Noesis Layer"
    rename_actions()
elif bpy.data.actions.get("root.000|Noesis Frames|Noesis Layer") != None:
    print("First action is already renamed")
    rename_actions()
else:
    print("First action does not exist.")
    exit
