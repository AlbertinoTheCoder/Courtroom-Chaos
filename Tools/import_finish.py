import unreal as u,os,runpy
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX False')
tasks=[]
for name in ['Courtroom','AnimatedGavel','GoldenGavel','Mustard','ExhibitStage']:
 t=u.AssetImportTask();t.filename=os.path.join(ROOT,'Art','Exports',name+'.fbx');t.destination_path='/Game/Courtroom' if name=='Courtroom' else '/Game/Evidence';t.destination_name='CourtroomShell' if name=='Courtroom' else name;t.automated=True;t.replace_existing=True;t.save=True
 o=u.FbxImportUI();o.import_mesh=True;o.import_as_skeletal=False;o.import_materials=False;o.import_textures=False;o.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;o.static_mesh_import_data.combine_meshes=True;o.static_mesh_import_data.auto_generate_collision=False;t.options=o;tasks.append(t)
u.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
for t in tasks:
 m=u.load_asset(t.destination_path+'/'+t.destination_name);assert isinstance(m,u.StaticMesh),t.destination_name
 for i,s in enumerate(m.static_materials):
  name=str(s.material_slot_name).split('.')[0];mat=u.load_asset('/Game/Courtroom/'+name) or u.load_asset('/Game/Characters/'+name)
  if mat:m.set_material(i,mat)
world=u.EditorLoadingAndSavingUtils.load_map('/Game/Courtroom/L_Courtroom');actors=u.get_editor_subsystem(u.EditorActorSubsystem)
def actor(tag,mesh,location):
 old=[a for a in actors.get_all_level_actors() if a.actor_has_tag(tag)]
 a=old[0] if old else actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(*location));a.set_actor_label(tag);a.tags=[tag];a.static_mesh_component.set_static_mesh(u.load_asset(mesh));a.static_mesh_component.set_mobility(u.ComponentMobility.MOVABLE);a.static_mesh_component.set_collision_enabled(u.CollisionEnabled.NO_COLLISION);a.set_actor_location(u.Vector(*location),False,False);a.set_actor_scale3d(u.Vector(1,-1,1));return a
actor('AnimatedGavel','/Game/Evidence/AnimatedGavel',(35,455,206.5))
actor('EvidenceExhibit','/Game/Evidence/Mustard',(0,-3000,105))
actor('ExhibitStudio','/Game/Evidence/ExhibitStage',(0,-3000,0))
for a in actors.get_all_level_actors():
 if a.actor_has_tag('Bumble'):a.set_actor_location(u.Vector(0,510,48),False,False)
def camera(tag,location,target,fov):
 old=[a for a in actors.get_all_level_actors() if a.actor_has_tag(tag)];a=old[0] if old else actors.spawn_actor_from_class(u.CameraActor,u.Vector(*location));a.set_actor_label(tag);a.tags=[tag];a.set_actor_location(u.Vector(*location),False,False);a.set_actor_rotation(u.MathLibrary.find_look_at_rotation(u.Vector(*location),u.Vector(*target)),False);a.camera_component.field_of_view=fov
camera('Inspect',(0,-3420,245),(-70,-3000,165),40)
camera('Bailiff',(720,-510,285),(720,-120,170),58)
camera('Judge',(0,105,335),(0,510,220),56)
for tag,location,intensity,color in [('Exhibit key',(-130,-3200,340),17000,(255,235,210)),('Exhibit fill',(180,-3160,250),11000,(187,221,255))]:
 old=[a for a in actors.get_all_level_actors() if a.get_actor_label()==tag];a=old[0] if old else actors.spawn_actor_from_class(u.RectLight,u.Vector(*location));a.set_actor_label(tag);a.set_actor_location(u.Vector(*location),False,False);a.set_actor_rotation(u.MathLibrary.find_look_at_rotation(u.Vector(*location),u.Vector(0,-3000,145)),False);c=a.light_component;c.set_editor_property('mobility',u.ComponentMobility.MOVABLE);c.set_editor_property('cast_shadows',False);c.set_editor_property('intensity',intensity);c.set_editor_property('source_width',220);c.set_editor_property('source_height',220);c.set_editor_property('light_color',u.Color(*color));c.set_editor_property('attenuation_radius',1000)
assert u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Courtroom/L_Courtroom')
runpy.run_path(os.path.join(ROOT,'Tools','refine_scene.py'))
runpy.run_path(os.path.join(ROOT,'Tools','create_case.py'))
runpy.run_path(os.path.join(ROOT,'Tools','import_audio.py'))
u.EditorAssetLibrary.save_directory('/Game');u.log('FINISH_CONTENT_OK')
