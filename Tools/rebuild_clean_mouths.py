import os
root=os.path.dirname(os.path.abspath(__file__))
source=open(os.path.join(root,'rig_cast.py')).read().replace('for action in actions:','for action in []:')
exec(compile(source,__file__,'exec'))
exec(compile(open(os.path.join(root,'build_case_cast.py')).read(),__file__,'exec'))
print('CLEAN_MOUTHS_BUILD_OK')
