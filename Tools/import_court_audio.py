"""Import baked speech, amplitude envelopes, and synchronized music stems."""
import json, os, runpy
import unreal as u
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
runpy.run_path(os.path.join(ROOT,'Tools','import_audio.py'))
manifest=json.load(open(os.path.join(ROOT,'Art','VoiceManifest.json'),encoding='utf-8'))
assets=u.AssetToolsHelpers.get_asset_tools()
tasks=[]
for name,clip in manifest['clips'].items():
 t=u.AssetImportTask();t.filename=os.path.join(ROOT,clip['file']);t.destination_path='/Game/Audio/Dialogue';t.destination_name=name;t.automated=True;t.replace_existing=True;t.save=True;tasks.append(t)
assets.import_asset_tasks(tasks)
takes={}
for name,c in manifest['clips'].items():
 sound=u.load_asset('/Game/Audio/Dialogue/'+name)
 assert isinstance(sound,u.SoundWave),name
 assert c['duration']>0 and c['envelope'] and max(c['envelope'])>0,name
 sound.set_editor_property('virtualization_mode',u.VirtualizationMode.PLAY_WHEN_SILENT)
 takes[name]=u.ChaosSpeechTake(speaker=c['speaker'],text=c['text'],sound=sound,duration=c['duration'],envelope_hz=c['envelope_hz'],envelope=c['envelope'])
factory=u.DataAssetFactory();factory.set_editor_property('data_asset_class',u.ChaosAudioData)
data=u.load_asset('/Game/Audio/DA_CourtAudio') or assets.create_asset('DA_CourtAudio','/Game/Audio',u.ChaosAudioData,factory)
data.set_editor_property('speech',{key:u.ChaosSpeechSequence(takes=[takes[name] for name in names]) for key,names in manifest['sequences'].items()})
data.set_editor_property('voice_presets',{name:profile['voice'] for name,profile in manifest['profiles'].items()})
data.set_editor_property('music_layers',[u.load_asset('/Game/Audio/'+name) for name in ['CourtroomShuffle','CourtroomTension','CourtroomChaos','CourtroomMayhem']])
u.EditorAssetLibrary.save_directory('/Game/Audio')
u.log('COURT_AUDIO_IMPORT_OK clips='+str(len(takes)))
