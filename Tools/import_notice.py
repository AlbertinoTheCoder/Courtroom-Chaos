import unreal as u,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX False')
t=u.AssetImportTask();t.filename=os.path.join(ROOT,'Art','Exports','Courtroom.fbx');t.destination_path='/Game/Courtroom';t.destination_name='CourtroomShell';t.automated=True;t.replace_existing=True;t.save=True
o=u.FbxImportUI();o.import_mesh=True;o.import_as_skeletal=False;o.import_materials=False;o.import_textures=False;o.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;o.static_mesh_import_data.combine_meshes=True;o.static_mesh_import_data.auto_generate_collision=False;t.options=o
u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
m=u.load_asset('/Game/Courtroom/CourtroomShell');assert isinstance(m,u.StaticMesh)
for i,s in enumerate(m.static_materials):
 name=str(s.material_slot_name).split('.')[0];mat=u.load_asset('/Game/Courtroom/'+name)
 if mat:m.set_material(i,mat)
assert u.EditorAssetLibrary.save_loaded_asset(m)
u.log('NOTICE_IMPORT_OK')
