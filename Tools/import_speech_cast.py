import runpy,os
root=os.path.dirname(os.path.abspath(__file__))
for script in ['import_case_cast.py','import_extra_cases.py','import_court_audio.py']:
 runpy.run_path(os.path.join(root,script))
print('SPEECH_CAST_IMPORT_OK')
