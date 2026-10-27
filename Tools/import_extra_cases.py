import json,os
import unreal as u
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));assets=u.AssetToolsHelpers.get_asset_tools()
tasks=[]
names=['Poster_Blackout','Poster_Charity','LifeHeart','LifeEmpty']
sources=[]
for filename in sorted(os.listdir(os.path.join(ROOT,'Art','Cases'))):
 if filename.endswith('.json'):
  c=json.load(open(os.path.join(ROOT,'Art','Cases',filename),encoding='utf-8'));sources.append(c)
  names.extend(c['id']+'_Evidence'+str(i) for i in range(6))
for name in names:
 t=u.AssetImportTask();t.filename=os.path.join(ROOT,'Art','UI',name+'.png');t.destination_path='/Game/UI';t.destination_name=name;t.automated=True;t.replace_existing=True;t.save=True;tasks.append(t)
assets.import_asset_tasks(tasks)
for name in names:
 texture=u.load_asset('/Game/UI/'+name);assert texture,name
 texture.set_editor_property('lod_group',u.TextureGroup.TEXTUREGROUP_UI);texture.set_editor_property('mip_gen_settings',u.TextureMipGenSettings.TMGS_NO_MIPMAPS)
factory=u.DataAssetFactory();factory.set_editor_property('data_asset_class',u.ChaosCaseData)
def line(c):return u.ChaosLine(speaker=c['speaker'],text=c['text'],emotion=c['emotion'])
for c in sources:
 case=u.load_asset('/Game/Cases/'+c['asset']) or assets.create_asset(c['asset'],'/Game/Cases',u.ChaosCaseData,factory)
 case.case_id=c['id'];case.title=c['title'];case.subtitle=c['subtitle']
 for section in ['consultation','opening','verdict']:setattr(case,section,[line(l) for l in c[section]])
 case.evidence=[u.ChaosEvidence(id=e['id'],title=e['title'],category=e['category'],description=e['description'],inspection=e['inspection'],unlock_stage=e['unlock_stage'],illustration=u.load_asset('/Game/UI/'+c['id']+'_Evidence'+str(i)),exhibit=u.load_asset('/Game/Evidence/'+e['mesh']) if e.get('mesh') else None) for i,e in enumerate(c['evidence'])]
 case.stages=[u.ChaosStage(title=s['title'],speaker=s['speaker'],contradiction=s['contradiction'],evidence=s['evidence'],statements=[u.ChaosStatement(text=t['text'],press=t['press'],emotion=t['emotion']) for t in s['statements']],resolution=[line(l) for l in s['resolution']]) for s in c['stages']]
 case.closing_prompt=c['closing_prompt'];case.conclusions=c['conclusions'];case.correct_conclusion=c['correct_conclusion']
 assert u.EditorAssetLibrary.save_loaded_asset(case,False),c['asset']
 u.log('CASE_SAVED '+c['id']+' '+str([(e.title,e.category,e.exhibit.get_name() if e.exhibit else None) for e in case.evidence]))
u.EditorAssetLibrary.save_directory('/Game/UI');u.log('EXTRA_CASE_IMPORT_OK')
