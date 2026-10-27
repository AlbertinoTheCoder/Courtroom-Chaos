import unreal as u,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAST=['Oliver','Victor','Bumble','Benny','Milo','Brick']
MOODS=['Idle','Listening','Speaking','Thinking','Confused','Happy','Smug','Angry','Nervous','Shock','Sad','Suspicious','Frustrated','Pointing','Slam','Gavel','LeanForward','LeanBackward','Celebrate','Embarrassed']
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX False')
assets=u.AssetToolsHelpers.get_asset_tools();report={}
world=u.EditorLoadingAndSavingUtils.load_map('/Game/Courtroom/L_Courtroom')
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
for name in CAST:
 task=u.AssetImportTask();task.filename=os.path.join(ROOT,'Art','Exports','SK_'+name+'.fbx');task.destination_path='/Game/Characters/Rigged';task.destination_name='SK_'+name;task.automated=True;task.replace_existing=True;task.save=True
 o=u.FbxImportUI();o.automated_import_should_detect_type=False;o.mesh_type_to_import=u.FBXImportType.FBXIT_SKELETAL_MESH;o.import_mesh=True;o.import_as_skeletal=True;o.import_materials=False;o.import_textures=False;o.import_animations=False;o.create_physics_asset=False;task.options=o
 assets.import_asset_tasks([task]);mesh=u.load_asset('/Game/Characters/Rigged/SK_'+name)
 assert isinstance(mesh,u.SkeletalMesh),'Skeletal mesh import failed: '+name
 for i,slot in enumerate(mesh.materials):
  material=u.load_asset('/Game/Characters/'+str(slot.material_slot_name))
  if material:
   u.MaterialEditingLibrary.set_material_usage(material,u.MaterialUsage.MATUSAGE_SKELETAL_MESH)
   slots=mesh.materials;slots[i].material_interface=material;mesh.materials=slots
 skeleton=mesh.skeleton;assert skeleton,'Skeleton missing'
 imported=[]
 for mood in MOODS:
  clip='AN_'+name+'_'+mood;t=u.AssetImportTask();t.filename=os.path.join(ROOT,'Art','Exports',clip+'.fbx');t.destination_path='/Game/Characters/Animations';t.destination_name=clip;t.automated=True;t.replace_existing=True;t.save=True
  o=u.FbxImportUI();o.automated_import_should_detect_type=False;o.mesh_type_to_import=u.FBXImportType.FBXIT_ANIMATION;o.import_mesh=False;o.import_animations=True;o.skeleton=skeleton;o.import_materials=False;o.import_textures=False;t.options=o;assets.import_asset_tasks([t])
  anim=u.load_asset('/Game/Characters/Animations/'+clip);assert isinstance(anim,u.AnimSequence),'Missing clip '+clip
  imported.append(clip)
 old=[a for a in actors.get_all_level_actors() if a.get_actor_label()==name]
 assert len(old)==1,'Expected one performer '+name
 old=old[0];location=old.get_actor_location();rotation=old.get_actor_rotation();scale=old.get_actor_scale3d()
 new=actors.spawn_actor_from_class(u.SkeletalMeshActor,location,rotation);component=new.skeletal_mesh_component;component.set_skeletal_mesh_asset(mesh);component.set_collision_enabled(u.CollisionEnabled.NO_COLLISION);component.set_mobility(u.ComponentMobility.MOVABLE)
 new.set_actor_scale3d(scale);new.tags=['Performer',name];component.play_animation(u.load_asset('/Game/Characters/Animations/AN_'+name+'_Idle'),True)
 bounds=new.get_actor_bounds(False)
 assert 100<bounds[1].z<200 and 20<bounds[1].x<150, 'Unexpected character scale: '+str(bounds)
 report[name]={'clips':imported,'bounds':str(bounds),'skeleton':skeleton.get_path_name()}
 actors.destroy_actor(old);new.set_actor_label(name)
if not any(a.get_actor_label()=='Defense' for a in actors.get_all_level_actors()):
 camera=actors.spawn_actor_from_class(u.CameraActor,u.Vector(-300,-320,285));camera.set_actor_label('Defense');camera.tags=['Defense'];camera.set_actor_rotation(u.MathLibrary.find_look_at_rotation(u.Vector(-300,-320,285),u.Vector(-300,75,170)),False);camera.camera_component.field_of_view=60
assert u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Courtroom/L_Courtroom')
u.EditorAssetLibrary.save_directory('/Game');open(os.path.join(ROOT,'Saved','RigImport.json'),'w').write(json.dumps(report,indent=2));u.log('RIG_IMPORT_OK '+str(report))

