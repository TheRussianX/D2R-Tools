#to work this requires "Relative editing" plugin to be active in the dope sheet
import bpy
from math import *  # It's considered bad practice to import everything from a library, especially when you're not using any (or just a few) of its function
import mathutils

item='EMPTY'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='ARMATURE')
selected_armatures = bpy.context.selected_objects
for armature in selected_armatures:
    print(armature.name)
    # If you want to move your object, simply set its location thus:
    armature.location = ( 0, 0, 0 )
    # And you can rotate the object the same way
    armature.rotation_euler = (1.5708,0,0)  # Note that you need to use radians rather than angles here