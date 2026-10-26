import unreal as u,json,os
w=u.EditorLoadingAndSavingUtils.load_map('/Game/Courtroom/L_Courtroom')
report=[]
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
 d={'label':a.get_actor_label(),'class':a.get_class().get_name(),'position':str(a.get_actor_location()),'rotation':str(a.get_actor_rotation())}
 if isinstance(a,u.StaticMeshActor):
  m=a.static_mesh_component.static_mesh;d['mesh']=m.get_path_name() if m else None;d['bounds']=str(m.get_bounds()) if m else None
 report.append(d)
p=os.path.join(u.Paths.project_saved_dir(),'MapInspection.json');open(p,'w').write(json.dumps(report,indent=2));u.log(str(report))
