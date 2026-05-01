# This script wil generate a Noesis scene for every animation track (0, Nstr-1)
# The mesh and anims are small and MUST BE scaled upon export by a factor of 80
# Do not export anims from Noesis using scale parameter, it will break them.
# Instead use scale 80 when importing fbx in Blender
# Usable only for models that crash Noesis when trying to export animations due to too many rpgContexts
# You have to copy the skeleton from its folder to character's folder and rename it as "skel.model"
# Change fmt_GR2Reader.py options to ANIMATION_MODE = 1 and SKELETON_LOAD = 0
# You will get only the skeleton with the animation applied

import glob
import ntpath
import os

Nstr = input("Enter the number of animation tracks to load: ")
number_of_anims = int(Nstr)
for i in range (0, number_of_anims):
    if (i in range(0,10)):
        anim_name = "anim_00"
    elif (i in range(10,100)):
        anim_name = "anim_0"
    else:
        anim_name = "anim_"
    outputfile = open('d:\\'+anim_name+str(i)+'.noesis', 'w')
    outputfile.write('NOESIS_SCENE_FILE)\n')
    outputfile.write('version 1\n')
    outputfile.write('physicslib		""\n')
    outputfile.write('defaultAxis		"0"\n')
    outputfile.write('\n')
    outputfile.write('object\n')
    outputfile.write('{\n')
    outputfile.write('    	name			"'+anim_name+str(i)+'"\n')
    outputfile.write('    	model			"skel.model"\n')
    outputfile.write('    	loadOptions		"-animtrack '+str(i)+'"\n')
    outputfile.write('\n')
    outputfile.write('}\n')
outputfile.close()
