import json
import os
import shutil
import glob

absolute_path_to_workfolder = 'd://Games//D2R//Work//data//'
#json_folder_path = 'd:\\Download\\D2R_dump\\'
list_tex_list = glob.glob ('d:\\Download\\D2R_dump\\**\\*.tex_list', recursive=True)
for tex_list in list_tex_list:
    model_name_noext = os.path.split(tex_list)[1].split('.')[0]
    #print(tex_list+'\n')
    source_model_path = tex_list.split('.')[0] + '.model'
    destination_model_path = tex_list.split('.')[0] +'\\'+ model_name_noext+'.model'
    new_tex_path = tex_list.split('.')[0] +'\\textures\\'
    if os.path.isfile(source_model_path) == True :
        os.makedirs(os.path.dirname(destination_model_path), exist_ok=True)
        shutil.copyfile(source_model_path, destination_model_path)
        print('Model copied')
    else:
        print('Missing model '+source_model_path+'\n')
    
    jfile = open(tex_list, 'r')
    data = jfile.readlines()
    for line in data:
        tex_rel_path = str(line).strip().replace('/','//')
        source_tex_path = os.path.abspath(absolute_path_to_workfolder + tex_rel_path)
        tex_name = os.path.split(source_tex_path)[1]
        destination_tex_path = (new_tex_path+tex_name).replace('\\','\\\\')
        
        if os.path.isfile(source_tex_path) == True :
            os.makedirs(os.path.dirname(destination_tex_path), exist_ok=True)
            shutil.copyfile(source_tex_path, destination_tex_path)
            print('Texture copied')
        else:
            print('Missing texture '+source_tex_path+'\n')
        #print(source_tex_path)
        #print(destination_tex_path)

        
    jfile.close()
