import os
import pathlib

# delete LOD 1 to 4, keep LOD 0
root_dir = pathlib.Path('d:/Download/D2R_test/items/_to_export/_test/')
for file in root_dir.rglob('*.*'):
    if str(file).endswith(('.model', '.texture', '.fbx', '.blend1', 'New_testfile.blend')):
        print(file)
        os.remove(file)
