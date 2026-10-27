import unreal as u, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets=u.AssetToolsHelpers.get_asset_tools()
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX False')
existing=u.load_asset('/Game/Courtroom/Courtroom')
if isinstance(existing,u.StaticMesh):
 u.EditorAssetLibrary.delete_asset('/Game/Courtroom/Courtroom')
tasks=[]
for name in ['Courtroom','Oliver','Victor','Bumble','Benny','Milo','Brick']:
 task=u.AssetImportTask();task.filename=os.path.join(ROOT,'Art','Exports',name+'.fbx');task.destination_path='/Game/Courtroom' if name=='Courtroom' else '/Game/Characters';task.destination_name='CourtroomShell' if name=='Courtroom' else name;task.automated=True;task.replace_existing=True;task.save=True
 options=u.FbxImportUI();options.import_mesh=True;options.import_as_skeletal=False;options.import_materials=True;options.import_textures=False;options.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;options.static_mesh_import_data.combine_meshes=True;options.static_mesh_import_data.generate_lightmap_u_vs=True;options.static_mesh_import_data.auto_generate_collision=True;task.options=options;tasks.append(task)
assets.import_asset_tasks(tasks)
audio=u.AssetImportTask();audio.filename=os.path.join(ROOT,'Art','Exports','Objection.wav');audio.destination_path='/Game/Audio';audio.automated=True;audio.save=True;assets.import_asset_tasks([audio])
world=u.EditorLoadingAndSavingUtils.new_blank_map(False)
assert world, 'Could not create courtroom world'
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
def mesh(name,path,loc,rot=u.Rotator()):
 a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(*loc),rot);a.set_actor_label(name);a.static_mesh_component.set_static_mesh(u.load_asset(path));a.set_actor_scale3d(u.Vector(1,-1,1));return a
room=mesh('Courtroom - Blender architectural collection','/Game/Courtroom/CourtroomShell',(0,0,0))
for name,loc in [('Oliver',(-300,-10,0)),('Victor',(300,-10,0)),('Bumble',(0,535,48)),('Milo',(500,350,0)),('Benny',(-500,80,0)),('Brick',(720,400,0))]:
 a=mesh(name,'/Game/Characters/'+name,loc);a.tags=['Performer'];a.static_mesh_component.set_mobility(u.ComponentMobility.MOVABLE)
def camera(name,loc,target,fov=55):
 a=actors.spawn_actor_from_class(u.CameraActor,u.Vector(*loc));a.set_actor_label(name);a.tags=[name];a.set_actor_rotation(u.MathLibrary.find_look_at_rotation(u.Vector(*loc),u.Vector(*target)),False);a.camera_component.field_of_view=fov
camera('Wide',(100,-1050,520),(0,220,160),62)
camera('Witness',(330,-85,270),(500,350,175),48)
camera('Judge',(0,140,340),(0,530,230),50)
def light(name,loc,rot,intensity,color,size=250):
 a=actors.spawn_actor_from_class(u.RectLight,u.Vector(*loc),u.Rotator(pitch=rot[0],yaw=rot[1],roll=rot[2]));a.set_actor_label(name);c=a.light_component;c.set_editor_property('intensity',intensity);c.set_editor_property('light_color',u.Color(*color));c.set_editor_property('source_width',size);c.set_editor_property('source_height',size);c.set_editor_property('mobility',u.ComponentMobility.MOVABLE)
light('Warm court key',(0,-200,620),(-70,90,0),18000,(255,219,169),500)
light('Judge key',(0,300,570),(-65,90,0),10000,(255,222,178),300)
light('Witness softbox',(500,80,470),(-60,90,0),8000,(255,236,205),250)
light('Cool gallery fill',(-650,-200,450),(-30,0,0),10000,(155,195,255),400)
sky=actors.spawn_actor_from_class(u.SkyLight,u.Vector(0,0,500));sky.light_component.set_editor_property('intensity',.5)
post=actors.spawn_actor_from_class(u.PostProcessVolume,u.Vector());post.set_editor_property('unbound',True)
settings=post.settings;settings.set_editor_property('override_auto_exposure_method',True);settings.set_editor_property('auto_exposure_method',u.AutoExposureMethod.AEM_MANUAL);settings.set_editor_property('override_auto_exposure_bias',True);settings.set_editor_property('auto_exposure_bias',0);post.settings=settings
assert u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Courtroom/L_Courtroom'), 'Map save failed'
u.EditorAssetLibrary.save_directory('/Game')
import runpy
runpy.run_path(os.path.join(ROOT,'Tools','refine_scene.py'))
runpy.run_path(os.path.join(ROOT,'Tools','polish_scene.py'))
runpy.run_path(os.path.join(ROOT,'Tools','import_rigs.py'))
runpy.run_path(os.path.join(ROOT,'Tools','import_finish.py'))
runpy.run_path(os.path.join(ROOT,'Tools','import_case_props.py'))
runpy.run_path(os.path.join(ROOT,'Tools','import_extra_cases.py'))
runpy.run_path(os.path.join(ROOT,'Tools','polish_portraits.py'))
runpy.run_path(os.path.join(ROOT,'Tools','import_court_audio.py'))
u.log('COURTROOM_ASSEMBLY_OK')
