import os
import glob

modelfiles = glob.glob ('d:\\Download\\D2R_test\\items\\_with_skeleton\\**\\*.model', recursive=True)
outputfile = open('d:\\blender_import_jobs.bat', 'w')
for f_file in modelfiles:
    fbxpath = os.path.split(f_file)[0]
    blend_path = fbxpath+'\\New_testfile.blend'
    print(blend_path)
    outputfile.write('"d:\\Portable x64\\Blender\\blender.exe" -b "'+blend_path+'" -P "d:\\Blender_import_fbx_fix_shader_rel_path_save.py"\n')



outputfile.close()
    
        


