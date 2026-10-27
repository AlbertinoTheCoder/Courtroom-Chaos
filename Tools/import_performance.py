import os,runpy
root=os.path.dirname(os.path.abspath(__file__))
for script in ['import_rigs.py','import_court_audio.py']:
 runpy.run_path(os.path.join(root,script))
