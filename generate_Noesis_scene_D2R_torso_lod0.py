# This script wil generate a Noesis scene for every animation track (0, Nstr-1)
# The mesh and anims are small and MUST BE scaled upon export by a factor of 80
# Usable only for models with a single "torso_lod0.model"
# For direct export of master model from Noesis (without scene file) get
# the max number of anims, input 0 for animation track and -fbxtexext .png
# -scale 80 -fbxmultitake as export parameters

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
    outputfile.write('    	model			"torso_lod0.model"\n')
    outputfile.write('    	loadOptions		"-animtrack '+str(i)+'"\n')
    outputfile.write('\n')
    outputfile.write('}\n')
outputfile.close()
