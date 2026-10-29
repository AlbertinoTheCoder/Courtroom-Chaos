import os
import unreal as u
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX False')
for name,role in [('Renzo','Benny'),('Pip','Milo'),('Nora','Benny'),('Agnes','Milo')]:
 original=u.load_asset('/Game/Characters/Rigged/SK_'+role)
 previous=u.load_asset('/Game/Characters/Rigged/SK_'+name)
 if previous:previous.get_editor_property('asset_import_data').set_editor_property('import_morph_targets',True)
 task=u.AssetImportTask();task.filename=os.path.join(ROOT,'Art','Exports','SK_'+name+'.fbx');task.destination_path='/Game/Characters/Rigged';task.destination_name='SK_'+name;task.automated=True;task.replace_existing=True;task.save=True
 o=u.FbxImportUI();o.automated_import_should_detect_type=False;o.mesh_type_to_import=u.FBXImportType.FBXIT_SKELETAL_MESH;o.import_mesh=True;o.import_as_skeletal=True;o.import_materials=False;o.import_textures=False;o.import_animations=False;o.create_physics_asset=False;o.skeleton=original.skeleton;o.skeletal_mesh_import_data.set_editor_property('import_morph_targets',True);task.options=o
 u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);mesh=u.load_asset('/Game/Characters/Rigged/SK_'+name);assert mesh.skeleton==original.skeleton,name
 assert {'TalkOpen','SmileHide'}.issubset({m.get_name() for m in mesh.get_editor_property('morph_targets')}),name
 slots=mesh.materials
 for i,slot in enumerate(slots):
  material=u.load_asset('/Game/Characters/'+str(slot.material_slot_name).split('.')[0]) or u.load_asset('/Game/Courtroom/'+str(slot.material_slot_name).split('.')[0]);assert material,str(slot.material_slot_name)
  u.MaterialEditingLibrary.set_material_usage(material,u.MaterialUsage.MATUSAGE_SKELETAL_MESH);u.MaterialEditingLibrary.set_material_usage(material,u.MaterialUsage.MATUSAGE_MORPH_TARGETS)
  u.EditorAssetLibrary.save_loaded_asset(material,False)
  slot.set_editor_property('material_interface',material);slots[i]=slot
 mesh.set_editor_property('materials',slots);assert all(slot.material_interface and 'DefaultMaterial' not in slot.material_interface.get_name() for slot in mesh.materials),name;assert u.EditorAssetLibrary.save_loaded_asset(mesh,False)
u.EditorAssetLibrary.save_directory('/Game/Characters');u.log('CASE_CAST_IMPORT_OK')
