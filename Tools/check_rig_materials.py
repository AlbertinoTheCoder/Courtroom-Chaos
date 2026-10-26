import unreal as u,os,json
m=u.load_asset('/Game/Characters/Rigged/SK_Milo')
r=[{'slot':str(s.material_slot_name),'material':s.material_interface.get_path_name() if s.material_interface else None} for s in m.materials]
open(os.path.join(u.Paths.project_saved_dir(),'RigMaterials.json'),'w').write(json.dumps(r,indent=2));u.log(str(r))
