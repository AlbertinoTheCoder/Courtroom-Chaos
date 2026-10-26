import unreal as u,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX False')
t=u.AssetImportTask();t.filename=os.path.join(ROOT,'Art','Exports','Courtroom.fbx');t.destination_path='/Game/Courtroom';t.destination_name='CourtroomShell';t.automated=True;t.replace_existing=True;t.save=True
o=u.FbxImportUI();o.import_mesh=True;o.import_as_skeletal=False;o.import_materials=False;o.import_textures=False;o.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;o.static_mesh_import_data.combine_meshes=True;t.options=o
u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
m=u.load_asset('/Game/Courtroom/CourtroomShell')
bounds=m.get_bounds().box_extent
assert abs(bounds.x-900)<2 and abs(bounds.y-700)<2, str(bounds)
u.log('ROOM_SCALE_VERIFIED '+str(bounds))
for i,slot in enumerate(m.static_materials):
 mat=u.load_asset('/Game/Courtroom/'+str(slot.material_slot_name))
 if mat:m.set_material(i,mat)
task=u.AssetImportTask();task.filename=os.path.join(ROOT,'Art','UI','Objection.png');task.destination_path='/Game/UI';task.automated=True;task.replace_existing=True;task.save=True
u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
u.EditorAssetLibrary.save_directory('/Game');u.log('LETTERING_IMPORT_OK')
