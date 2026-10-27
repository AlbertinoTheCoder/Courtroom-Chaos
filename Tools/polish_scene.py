"""Correct clearances, portrait staging and rebuild the imported palette explicitly."""
import unreal as u, math
world=u.EditorLoadingAndSavingUtils.load_map('/Game/Courtroom/L_Courtroom')
sub=u.get_editor_subsystem(u.EditorActorSubsystem)
palette={'wood':'70462F','oak':'A86D43','cream':'F5E4C5','red':'BD4551','gold':'E9B954','blue':'304F78','teal':'64A9A0','ink':'24293A','purple':'744886','skin':'EDAF82','white':'FFF4DC','hair':'33283A','green':'4C7860'}
for folder in ['/Game/Courtroom','/Game/Characters']:
 for name,h in palette.items():
  m=u.load_asset(folder+'/'+name)
  if not isinstance(m,u.Material):continue
  u.MaterialEditingLibrary.delete_all_material_expressions(m)
  c=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector)
  rgb=[int(h[i:i+2],16)/255 for i in (0,2,4)]
  rgb=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
  c.constant=u.LinearColor(*rgb,1)
  u.MaterialEditingLibrary.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
  r=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant);r.r=.38 if name=='gold' else .72
  u.MaterialEditingLibrary.connect_material_property(r,'',u.MaterialProperty.MP_ROUGHNESS)
  metal=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant);metal.r=.45 if name=='gold' else 0
  u.MaterialEditingLibrary.connect_material_property(metal,'',u.MaterialProperty.MP_METALLIC)
  if folder=='/Game/Characters':u.MaterialEditingLibrary.set_material_usage(m,u.MaterialUsage.MATUSAGE_SKELETAL_MESH)
  u.MaterialEditingLibrary.recompile_material(m)
positions={'Bumble':(0,510,48),'Oliver':(-300,75,0),'Victor':(300,75,0),'Milo':(500,420,0),'Brick':(720,-120,0),'Benny':(-520,150,0)}
for a in sub.get_all_level_actors():
 name=a.get_actor_label()
 if name in positions:a.set_actor_location(u.Vector(*positions[name]),False,False)
 if isinstance(a,u.RectLight):
  c=a.light_component;c.set_editor_property('cast_shadows',False)
  c.set_editor_property('intensity',22000);c.set_editor_property('attenuation_radius',2400)
 if isinstance(a,u.SkyLight):
  c=a.light_component;c.set_editor_property('source_type',u.SkyLightSourceType.SLS_SPECIFIED_CUBEMAP);c.set_editor_property('cubemap',u.load_asset('/Engine/MapTemplates/Sky/DaylightAmbientCubemap'));c.set_editor_property('intensity',1.2);c.set_editor_property('mobility',u.ComponentMobility.MOVABLE)
 if isinstance(a,u.PostProcessVolume):
  s=a.settings;s.set_editor_property('auto_exposure_bias',1.4);s.set_editor_property('override_ambient_occlusion_intensity',True);s.set_editor_property('ambient_occlusion_intensity',.25);a.settings=s
 if name=='Witness':
  loc=u.Vector(470,-80,290);target=u.Vector(500,420,170);a.set_actor_location(loc,False,False);a.set_actor_rotation(u.MathLibrary.find_look_at_rotation(loc,target),False);a.camera_component.field_of_view=60
 # A broad, shadow-free front fill keeps eyebrows and eye whites readable.
 if name=='Witness softbox':
  loc=u.Vector(400,160,390);a.set_actor_location(loc,False,False);a.set_actor_rotation(u.MathLibrary.find_look_at_rotation(loc,u.Vector(500,420,180)),False)
# Dialogue shots deliberately isolate the current speaker.
for tag,position,target in [('Client',(-520,-320,285),(-520,150,165)),('Prosecutor',(320,-390,290),(300,75,170))]:
 candidates=[a for a in sub.get_all_level_actors() if a.get_actor_label()==tag]
 a=candidates[0] if candidates else sub.spawn_actor_from_class(u.CameraActor,u.Vector(*position))
 a.set_actor_label(tag);a.tags=[tag];a.set_actor_location(u.Vector(*position),False,False);a.set_actor_rotation(u.MathLibrary.find_look_at_rotation(u.Vector(*position),u.Vector(*target)),False);a.camera_component.field_of_view=60
assert u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Courtroom/L_Courtroom')
u.EditorAssetLibrary.save_directory('/Game');u.log('COURT_POLISH_OK')
