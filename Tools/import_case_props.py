import unreal as u,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX False')
for name in ['BatteryHotplate','CharityEnvelope']:
 t=u.AssetImportTask();t.filename=os.path.join(ROOT,'Art','Exports',name+'.fbx');t.destination_path='/Game/Evidence';t.destination_name=name;t.automated=True;t.replace_existing=True;t.save=True
 o=u.FbxImportUI();o.import_mesh=True;o.import_as_skeletal=False;o.import_materials=False;o.import_textures=False;o.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;o.static_mesh_import_data.combine_meshes=True;o.static_mesh_import_data.auto_generate_collision=False;t.options=o
 u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);mesh=u.load_asset('/Game/Evidence/'+name);assert isinstance(mesh,u.StaticMesh)
 for i,slot in enumerate(mesh.static_materials):
  material=u.load_asset('/Game/Characters/'+str(slot.material_slot_name).split('.')[0]) or u.load_asset('/Game/Courtroom/'+str(slot.material_slot_name).split('.')[0])
  if material:mesh.set_material(i,material)
 u.EditorAssetLibrary.save_loaded_asset(mesh)
u.log('CASE_PROP_IMPORT_OK')
