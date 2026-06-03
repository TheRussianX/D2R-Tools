import json
import os
import shutil
import glob

absolute_path_to_workfolder = 'd://Games//D2R//Work//data//'
json_folder_path = 'd:\\Download\\D2R_dump\\json\\'
json_list = glob.glob (json_folder_path+'*.json')
for json_path in json_list:
    jname = os.path.split(json_path)[1].split('.')[0]
    jfile = open(json_path, 'r')
    data = json.loads(jfile.read())

    if 'skeletons' not in data['dependencies']:
        rigged = False
    else:
        if len(data['dependencies']['skeletons']) == 0:
            rigged = False
        else:
            for skeleton in data['dependencies']['skeletons']:
                if "path" in skeleton:
                    skeleton_path = skeleton['path']
                    if os.path.isfile(absolute_path_to_workfolder+skeleton_path) == True :
                        rigged = True
                    else:
                        rigged = False
                else:
                    rigged = False
    print(rigged)

    if 'models' not in data['dependencies']:
        mesh = False
    else:
        mesh = True

    if 'textures' not in data['dependencies']:
        tex = False
    else:
        tex = True

    if mesh != False:
        if "path" in data['dependencies']['models'][0]:
            base_path = os.path.split(data['dependencies']['models'][0]['path'])[0].replace('/', '//')
            if '//model' in base_path:
                    base_path = base_path.replace('//model','')
       # print(base_path)
        counter = 0
        for model in data['dependencies']['models']:
            if "path" in model:
                model_path = model['path']
                model_name = os.path.split(model_path)[1]
                model_name_noext = model_name.split('.')[0]

                if rigged == True:
                    model_full_path = 'd://Download//D2R_dump//rigged//'+jname+'//'+model_name_noext+'_lod0.model'
                else:
                    model_full_path = 'd://Download//D2R_dump//static//'+jname+'//'+model_name_noext+'_lod0.model'

            #prevent overwriting of models with the same name
                if os.path.isfile(model_full_path):
                    model_full_path = model_full_path.replace('.model', '_'+str(counter)+'.model')
                    counter = counter+1
               # print (model_full_path)
                print(counter)
                model_path = model_path.replace('/', '//')
                model_path = model_path.replace('.model','_lod0.model')
               # print(absolute_path_to_workfolder+model_path)
                if os.path.isfile(absolute_path_to_workfolder+model_path) == True :
                    os.makedirs(os.path.dirname(model_full_path), exist_ok=True)
                    shutil.copyfile(absolute_path_to_workfolder+model_path, model_full_path)
                else:
                    print('Missing model '+absolute_path_to_workfolder+model_path+'\n')
    if rigged != False:
        for skeleton in data['dependencies']['skeletons']:
            if "path" in skeleton:
                skeleton_path = skeleton['path']
                skel_fname = os.path.split(skeleton_path)[1]
                skel_fname_noext = skel_fname.split('.')[0]
                if skel_fname_noext != jname:
                    skel_fname = jname+'.skeleton'
                new_skel_path = 'd://Download//D2R_dump//rigged//'+jname+'//skeleton//'+skel_fname
               # print(new_skel_path)
                skeleton_path = skeleton_path.replace('/', '//')
                if os.path.isfile(absolute_path_to_workfolder+skeleton_path) == True :
                    os.makedirs(os.path.dirname(new_skel_path), exist_ok=True)
                    shutil.copyfile(absolute_path_to_workfolder+skeleton_path, new_skel_path)
                else:
                    print('Missing skeleton '+absolute_path_to_workfolder+skeleton_path+'\n')
    if tex != False:
        for texture in data['dependencies']['textures']:
            if "path" in texture:
                texture_path = texture['path']

                tex_fname = os.path.split(texture_path)[1]
                if rigged == True:
                    tex_new_path = 'd://Download//D2R_dump//rigged//'+jname+'//textures//'+tex_fname
                else:
                    tex_new_path = 'd://Download//D2R_dump//static//'+jname+'//textures//'+tex_fname
                #print (tex_new_path)
                texture_path = texture_path.replace('/', '//')
                if os.path.isfile(absolute_path_to_workfolder+texture_path) == True :
                    os.makedirs(os.path.dirname(tex_new_path), exist_ok=True)
                    shutil.copyfile((absolute_path_to_workfolder+texture_path), tex_new_path)
                else:
                    print('Missing texture '+absolute_path_to_workfolder+texture_path+'\n')
    jfile.close()
