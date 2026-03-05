# root|Anim|Anim Layer will be the first imported action that will get into the last position because all other actions will be named root.001, etc
import bpy
from bpy import context as C

def rename_actions():
    filelist = open('d:\\Download\\bpy\\animations_list.txt ', 'r')
    if filelist != FileNotFoundError:
        data = filelist.readlines()
        actions = bpy.data.actions
        i = 0
        for act in actions:
           act.name = data[i]
           print(act.name)
           i += 1
           if (i > len(actions)):
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
