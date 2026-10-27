"""Shadow-free portrait fills keep the full cast readable across every case."""
import unreal as u
world=u.EditorLoadingAndSavingUtils.load_map('/Game/Courtroom/L_Courtroom');sub=u.get_editor_subsystem(u.EditorActorSubsystem)
for name,location,target,intensity in [('Brick',(650,-340,300),(720,-120,180),12000),('Victor',(380,-170,280),(300,75,180),6000)]:
 label='Portrait / '+name+' fill';found=[a for a in sub.get_all_level_actors() if a.get_actor_label()==label]
 light=found[0] if found else sub.spawn_actor_from_class(u.RectLight,u.Vector(*location))
 light.set_actor_label(label);light.set_actor_location(u.Vector(*location),False,False);light.set_actor_rotation(u.MathLibrary.find_look_at_rotation(u.Vector(*location),u.Vector(*target)),False)
 c=light.light_component;c.set_editor_property('mobility',u.ComponentMobility.MOVABLE);c.set_editor_property('cast_shadows',False);c.set_editor_property('intensity',intensity);c.set_editor_property('attenuation_radius',480);c.set_editor_property('source_width',180);c.set_editor_property('source_height',180)
 c.set_editor_property('light_color',u.Color(255,241,222,255))
assert u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Courtroom/L_Courtroom')
u.log('PORTRAIT_FILL_OK')
