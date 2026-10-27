"""Physical exhibits for the banquet and donation cases."""
import bpy,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
exec(compile(open(os.path.join(ROOT,'Tools','build_art.py')).read().split("box('Foundation'")[0],__file__,'exec'))
def raised_label(value,position,size,material):
 o=text(value,position,size,material);o.scale.x=-1
 bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for polygon in o.data.polygons:polygon.flip()
 o.data.update()

def finish(name,before):
 objects=list(set(scene.objects)-before);export(name,objects)
 for o in objects:o.hide_set(True)
before=set(scene.objects)
box('Sealed battery cassette',(0,0,.16),(.66,.42,.25),'teal',.035)
box('Battery top flange',(0,0,.29),(.7,.46,.035),'ink',.015)
box('Hot plate housing',(0,0,.36),(.76,.48,.13),'gold',.035)
rod('Heating surface',(0,0,.426),(0,0,.448),.17,'ink')
for r in [.06,.1,.14]:
 bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=.007,location=(0,0,.45));bpy.context.object.data.materials.append(mats['wood'])
for x in [-.25,.25]:rod('Control knob',(x,-.25,.36),(x,-.274,.36),.036,'ink')
raised_label('48 V',(0,-.225,.205),.052,'white')
for x in [-.24,-.08,.08,.24]:box('Charge segment',(x,-.216,.17),(.10,.013,.045),'green',.006)
for x in [-.26,.26]:
 for y in [-.15,.15]:box('Rubber foot',(x,y,.025),(.08,.08,.04),'ink',.01)
finish('BatteryHotplate',before)
before=set(scene.objects)
box('Sealed donation envelope',(0,0,.28),(.79,.055,.50),'cream',.016)
for a,b in [((-.37,-.034,.50),(0,-.039,.26)),((0,-.039,.26),(.37,-.034,.50))]:rod('Envelope fold',a,b,.004,'oak')
rod('Blue tamper seal',(0,-.035,.28),(0,-.052,.28),.075,'blue')
rod('Seal gold rim',(0,-.053,.28),(0,-.057,.28),.059,'gold')
rod('Seal blue centre',(0,-.058,.28),(0,-.062,.28),.050,'blue')
raised_label('C17',(0,-.065,.255),.052,'white')
for x in [-.28,.28]:box('Paper edge',(x,0,.28),(.014,.059,.45),'white',.004)
finish('CharityEnvelope',before)
for o in scene.objects:o.hide_set(False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'Art','Blender','CaseProps.blend'))
print('CASE_PROPS_OK')
