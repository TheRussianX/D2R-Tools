import glob
import ntpath
import os

models = glob.glob ('d:\\Download\\D2R_test\\data\\hd\\items\\**\\*.model', recursive=True)
for model in models:
    modelpath = os.path.split(model)[0]
    #print(modelpath)
    all_files_in_folder = glob.glob(modelpath+'\\*.*')
    for filename in all_files_in_folder:
        if ".texture" in filename:
            tex_path = os.path.split(filename)[0]
            tex_name = os.path.split(filename)[1]
            if os.path.exists(tex_path+'\\textures'):
                print(tex_path+'\\textures\n')
                os.replace(filename, tex_path+'\\textures\\'+tex_name)
                print('Texture moved')
            else:
                os.mkdirs(tex_path+'\\textures')
                os.replace(filename, tex_path+'\\textures\\'+tex_name)
