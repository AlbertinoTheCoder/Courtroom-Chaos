import os,runpy
root=os.path.dirname(os.path.abspath(__file__))
for script in ['create_mouth_material.py','import_mouths.py','import_case_cast.py']:
 runpy.run_path(os.path.join(root,script))
print('CLEAN_MOUTHS_IMPORT_OK')
