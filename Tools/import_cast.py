import unreal as u,os,runpy
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX False')
tasks=[]
for name in ['Oliver','Victor','Bumble','Benny','Milo','Brick']:
 t=u.AssetImportTask();t.filename=os.path.join(ROOT,'Art','Exports',name+'.fbx');t.destination_path='/Game/Characters';t.destination_name=name;t.automated=True;t.replace_existing=True;t.save=True
 o=u.FbxImportUI();o.import_mesh=True;o.import_as_skeletal=False;o.import_materials=False;o.import_textures=False;o.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;o.static_mesh_import_data.combine_meshes=True;o.static_mesh_import_data.auto_generate_collision=False;t.options=o;tasks.append(t)
u.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
for t in tasks:
 mesh=u.load_asset('/Game/Characters/'+t.destination_name)
 assert isinstance(mesh,u.StaticMesh),t.destination_name
 for i,slot in enumerate(mesh.static_materials):
  material=u.load_asset('/Game/Characters/'+str(slot.material_slot_name))
  if material:mesh.set_material(i,material)
runpy.run_path(os.path.join(ROOT,'Tools','polish_scene.py'))
u.EditorAssetLibrary.save_directory('/Game');u.log('CAST_IMPORT_OK')
