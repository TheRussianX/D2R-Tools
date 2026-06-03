import os
import glob

modelfiles = glob.glob ('d:\\Download\\D2R_test\\items\\_anims\\**\\*.model', recursive=True)
outputfile = open('d:\\blender_anims_jobs.bat', 'w')
for f_file in modelfiles:
    fbxpath = os.path.split(f_file)[0]
    blend_path = fbxpath+'\\New_testfile.blend'
    print(blend_path)
    outputfile.write('"d:\\Portable x64\\Blender\\blender.exe" -b "'+blend_path+'" -P "d:\\Blender_import_anims_rename_save.py"\n')



outputfile.close()
    
        


