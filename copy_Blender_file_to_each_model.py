import glob
import shutil
import os

models = glob.glob ('d:\\Download\\D2R_test\\items\\_to_export\\**\\*.model', recursive=True)
for model in models:
    modelpath = os.path.split(model)[0]
    #print(modelpath)
    shutil.copyfile('d:\\Download\\New_testfile.blend', modelpath+'\\New_testfile.blend')
