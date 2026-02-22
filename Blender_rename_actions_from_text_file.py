import bpy
from bpy import context as C

filelist = open('d:\\Download\\bpy\\animations_list.txt ', 'r')
data = filelist.readlines()
actions = bpy.data.actions
i = 0
for act in actions:
   act.name = data[i]
   print(act.name)
   i += 1
