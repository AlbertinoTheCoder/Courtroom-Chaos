import os,runpy
root=os.path.dirname(os.path.abspath(__file__))
for script in ['import_case_props.py','import_extra_cases.py','polish_portraits.py','import_court_audio.py']:
 runpy.run_path(os.path.join(root,script))
print('CASE_EXPANSION_IMPORT_OK')
