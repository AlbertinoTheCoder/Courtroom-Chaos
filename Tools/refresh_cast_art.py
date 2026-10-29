import os,runpy
root=os.path.dirname(os.path.abspath(__file__))
for script in ['import_case_cast.py','import_extra_cases.py']:
 runpy.run_path(os.path.join(root,script))
print('CAST_ART_REFRESH_OK')
