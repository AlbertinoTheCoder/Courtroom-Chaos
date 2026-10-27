import unreal as u,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX False')
for name in ['Oliver','Victor','Bumble','Benny','Milo','Brick']:
 mesh=u.load_asset('/Game/Characters/Rigged/SK_'+name)
 data=mesh.get_editor_property('asset_import_data');data.set_editor_property('import_morph_targets',True)
 t=u.AssetImportTask();t.filename=os.path.join(ROOT,'Art','Exports','SK_'+name+'.fbx');t.destination_path='/Game/Characters/Rigged';t.destination_name='SK_'+name;t.automated=True;t.replace_existing=True;t.save=True
 o=u.FbxImportUI();o.automated_import_should_detect_type=False;o.mesh_type_to_import=u.FBXImportType.FBXIT_SKELETAL_MESH;o.import_mesh=True;o.import_as_skeletal=True;o.import_materials=False;o.import_textures=False;o.import_animations=False;o.create_physics_asset=False;o.skeleton=mesh.skeleton;o.skeletal_mesh_import_data.set_editor_property('import_morph_targets',True);t.options=o
 u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
 targets=[m.get_name() for m in mesh.get_editor_property('morph_targets')]
 assert 'TalkOpen' in targets and 'SmileHide' in targets,(name,targets)
 u.log('MOUTH_IMPORT '+name+' '+str(targets))
import runpy
runpy.run_path(os.path.join(ROOT,'Tools','finalize_cast_materials.py'))
u.EditorAssetLibrary.save_directory('/Game/Characters/Rigged')
u.log('MOUTH_IMPORT_OK')
