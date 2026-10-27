import unreal as u,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tasks=[]
for name in ['CourtroomShuffle','CourtroomTension','CourtroomChaos','CourtroomMayhem','Objection','UITick','DeskHit','GavelHit','Press','Wrong','Victory','Voice_Oliver','Voice_Victor','Voice_Bumble','Voice_Benny','Voice_Milo','Voice_Brick']:
 t=u.AssetImportTask();t.filename=os.path.join(ROOT,'Art','Exports',name+'.wav');t.destination_path='/Game/Audio';t.automated=True;t.replace_existing=True;t.save=True;tasks.append(t)
u.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
for name in ['CourtroomShuffle','CourtroomTension','CourtroomChaos','CourtroomMayhem']:
 music=u.load_asset('/Game/Audio/'+name);assert isinstance(music,u.SoundWave)
 music.set_editor_property('looping',True);music.set_editor_property('virtualization_mode',u.VirtualizationMode.PLAY_WHEN_SILENT)
u.EditorAssetLibrary.save_directory('/Game/Audio');u.log('AUDIO_IMPORT_OK')
