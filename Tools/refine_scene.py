import unreal as u,os,glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
world=u.EditorLoadingAndSavingUtils.load_map('/Game/Courtroom/L_Courtroom')
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
angles={'Warm court key':(-70,90),'Judge key':(-65,90),'Witness softbox':(-60,90),'Cool gallery fill':(-30,0)}
for a in actors.get_all_level_actors():
 if isinstance(a,u.StaticMeshActor):a.set_actor_scale3d(u.Vector(1,-1,1))
 if a.get_actor_label() in angles:
  p,y=angles[a.get_actor_label()];a.set_actor_rotation(u.Rotator(pitch=p,yaw=y,roll=0),False)
tasks=[]
for file in glob.glob(os.path.join(ROOT,'Art','UI','*.png')):
 t=u.AssetImportTask();t.filename=file;t.destination_path='/Game/UI';t.automated=True;t.replace_existing=True;t.save=True;tasks.append(t)
u.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
for t in tasks:
 for path in t.imported_object_paths:
  tex=u.load_asset(path)
  if isinstance(tex,u.Texture2D):
   tex.set_editor_property('lod_group',u.TextureGroup.TEXTUREGROUP_UI);tex.set_editor_property('compression_settings',u.TextureCompressionSettings.TC_EDITOR_ICON);tex.set_editor_property('mip_gen_settings',u.TextureMipGenSettings.TMGS_NO_MIPMAPS)
assert u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Courtroom/L_Courtroom')
u.EditorAssetLibrary.save_directory('/Game');u.log('SCENE_REFINEMENT_OK')
