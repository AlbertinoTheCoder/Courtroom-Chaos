import unreal as u,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tasks=[]
for name in ['CourtroomShuffle','UITick','DeskHit','GavelHit','Press','Wrong','Victory','Voice_Oliver','Voice_Victor','Voice_Bumble','Voice_Benny','Voice_Milo','Voice_Brick']:
 t=u.AssetImportTask();t.filename=os.path.join(ROOT,'Art','Exports',name+'.wav');t.destination_path='/Game/Audio';t.automated=True;t.replace_existing=True;t.save=True;tasks.append(t)
u.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
music=u.load_asset('/Game/Audio/CourtroomShuffle');assert isinstance(music,u.SoundWave)
music.set_editor_property('looping',True)
u.EditorAssetLibrary.save_directory('/Game/Audio');u.log('AUDIO_IMPORT_OK')
